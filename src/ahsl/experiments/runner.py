"""End-to-end configuration-driven runner for AHSL Phase A0."""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
import yaml

from ahsl.corruption import corrupt_incidence
from ahsl.experiments.analysis import aggregate_results, paired_statistical_tests
from ahsl.experiments.plotting import generate_plots
from ahsl.experiments.report import write_research_report
from ahsl.metrics import recovery_metrics
from ahsl.models import (
    FixedTreeAHSL,
    NearestConnectedSubtree,
    NoiseAwareMAPSubtree,
    ObservedBaseline,
    SparseUnconstrained,
    UnconstrainedIncidence,
)
from ahsl.reproducibility import set_all_seeds
from ahsl.subtree import (
    enumerate_connected_subtrees,
    enumeration_diagnostic,
    subtree_incidence_matrix,
)
from ahsl.synthetic import generate_alpha_acyclic_hypergraph
from ahsl.trees import generate_tree


LOGGER = logging.getLogger("ahsl.a0")


@dataclass(frozen=True)
class ExperimentJob:
    """One paired synthetic dataset evaluated by every configured model."""

    index: int
    n: int
    m: int
    tree_topology: str
    branch_probability: float
    p_false_positive: float
    p_false_negative: float
    noise_setting: str
    num_observations: int
    seed: int


def _load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    if not isinstance(config, dict):
        raise ValueError("configuration root must be a mapping")
    return config


def _dry_run_config(config: dict[str, Any]) -> dict[str, Any]:
    dry = copy.deepcopy(config)
    dry["experiment_id"] = f"{config['experiment_id']}_dry_run"
    dry["n_values"] = [8]
    dry["m_values"] = [4]
    dry["tree_topologies"] = ["path"]
    dry["branch_probabilities"] = [0.4]
    dry["noise_settings"] = [
        {
            "name": "symmetric_0.20",
            "p_false_positive": 0.2,
            "p_false_negative": 0.2,
        }
    ]
    dry["observation_repetitions"] = [1]
    dry["seeds"] = [0]
    dry["models"]["sparse_lambdas"] = [0.01]
    dry["models"]["epochs"] = 12
    dry["models"]["fixed_tree_epochs"] = 12
    dry["statistics"]["bootstrap_samples"] = 100
    dry["plots"] = {
        "n": 8,
        "m": 4,
        "branch_probability": 0.4,
        "num_observations": 1,
        "sparse_lambda": 0.01,
    }
    return dry


def _build_jobs(config: dict[str, Any]) -> list[ExperimentJob]:
    product = itertools.product(
        config["n_values"],
        config["m_values"],
        config["tree_topologies"],
        config["branch_probabilities"],
        config["noise_settings"],
        config["observation_repetitions"],
        config["seeds"],
    )
    jobs: list[ExperimentJob] = []
    for index, (n, m, topology, branch, noise, repetitions, seed) in enumerate(product):
        jobs.append(
            ExperimentJob(
                index=index,
                n=int(n),
                m=int(m),
                tree_topology=str(topology),
                branch_probability=float(branch),
                p_false_positive=float(noise["p_false_positive"]),
                p_false_negative=float(noise["p_false_negative"]),
                noise_setting=str(noise["name"]),
                num_observations=int(repetitions),
                seed=int(seed),
            )
        )
    return jobs


def _candidate_upper_bound(m: int, topology: str) -> int:
    diagnostic = enumeration_diagnostic(m, topology)
    return diagnostic.get("num_connected_subtrees", diagnostic["search_space"])


def _print_experiment_plan(
    config: dict[str, Any], jobs: list[ExperimentJob], max_runs: int | None
) -> list[ExperimentJob]:
    selected = jobs if max_runs is None else jobs[:max_runs]
    model_fits_per_job = 5 + len(config["models"]["sparse_lambdas"])
    worst_candidates = max(
        _candidate_upper_bound(job.m, job.tree_topology) for job in selected
    )
    worst_search_space = max((1 << job.m) - 1 for job in selected)
    worst_n = max(job.n for job in selected)
    logits_megabytes = worst_n * worst_candidates * 4 / 1024**2
    LOGGER.info("Experiment plan")
    LOGGER.info("  configured dataset cases: %d", len(jobs))
    LOGGER.info("  selected dataset cases: %d", len(selected))
    LOGGER.info("  model fits per case: %d", model_fits_per_job)
    LOGGER.info("  selected model fits: %d", len(selected) * model_fits_per_job)
    LOGGER.info("  worst mask search space: %d", worst_search_space)
    LOGGER.info("  worst candidate-count upper bound: %d", worst_candidates)
    LOGGER.info("  worst FixedTreeAHSL logits estimate: %.2f MiB", logits_megabytes)

    maximum_search_space = int(config["resources"]["max_enumeration_search_space"])
    if worst_search_space > maximum_search_space:
        raise RuntimeError(
            "planned exact enumeration scans "
            f"{worst_search_space} masks, exceeding configured limit {maximum_search_space}; "
            "reduce m explicitly instead of silently dropping a topology"
        )
    return selected


def _derived_seed(base_seed: int, *coordinates: int) -> int:
    sequence = np.random.SeedSequence([base_seed, *coordinates])
    return int(sequence.generate_state(1, dtype=np.uint32)[0])


def _observations_for_job(clean: np.ndarray, job: ExperimentJob) -> tuple[np.ndarray, int]:
    observations = []
    flips = 0
    coordinates = [
        job.n,
        job.m,
        int(round(job.branch_probability * 1000)),
        int(round(job.p_false_positive * 1000)),
        int(round(job.p_false_negative * 1000)),
    ]
    for repetition in range(job.num_observations):
        corruption = corrupt_incidence(
            clean,
            job.p_false_negative,
            job.p_false_positive,
            _derived_seed(job.seed, 31, *coordinates, repetition),
        )
        observations.append(corruption["corrupted_incidence"])
        flips += int(corruption["num_flipped"])
    stacked = np.stack(observations)
    return (stacked[0] if job.num_observations == 1 else stacked), flips


def _model_specifications(
    config: dict[str, Any], candidates: np.ndarray, job: ExperimentJob
) -> list[tuple[str, dict[str, Any], Any]]:
    model_config = config["models"]
    recorded_common = {
        "epochs": int(model_config["epochs"]),
        "learning_rate": float(model_config["learning_rate"]),
        "threshold": float(model_config["threshold"]),
    }
    training_common = {**recorded_common, "seed": _derived_seed(job.seed, 51)}
    specifications: list[tuple[str, dict[str, Any], Any]] = [
        ("Observed", {}, ObservedBaseline()),
        (
            "Unconstrained",
            recorded_common,
            UnconstrainedIncidence(**training_common),
        ),
    ]
    for lambda_s in model_config["sparse_lambdas"]:
        recorded_parameters = {**recorded_common, "lambda_s": float(lambda_s)}
        training_parameters = {**training_common, "lambda_s": float(lambda_s)}
        specifications.append(
            (
                "SparseUnconstrained",
                recorded_parameters,
                SparseUnconstrained(**training_parameters),
            )
        )
    specifications.extend(
        [
            ("NearestConnectedSubtree", {}, NearestConnectedSubtree(candidates)),
            (
                "NoiseAwareMAPSubtree",
                {
                    "p_false_negative": job.p_false_negative,
                    "p_false_positive": job.p_false_positive,
                },
                NoiseAwareMAPSubtree(
                    candidates,
                    job.p_false_negative,
                    job.p_false_positive,
                ),
            ),
            (
                "FixedTreeAHSL",
                {
                    "epochs": int(model_config["fixed_tree_epochs"]),
                    "learning_rate": float(model_config["fixed_tree_learning_rate"]),
                    "entropy_weight": float(model_config["entropy_weight"]),
                    "size_weight": float(model_config["size_weight"]),
                },
                FixedTreeAHSL(
                    candidates,
                    epochs=int(model_config["fixed_tree_epochs"]),
                    learning_rate=float(model_config["fixed_tree_learning_rate"]),
                    entropy_weight=float(model_config["entropy_weight"]),
                    size_weight=float(model_config["size_weight"]),
                    seed=_derived_seed(job.seed, 52),
                ),
            ),
        ]
    )
    return specifications


def _evaluate_job(
    config: dict[str, Any],
    job: ExperimentJob,
    candidate_cache: dict[tuple[int, str, int], tuple[Any, np.ndarray]],
    clean_cache: dict[tuple[int, int, str, float, int], np.ndarray],
) -> list[dict[str, Any]]:
    tree_key = (job.m, job.tree_topology, job.seed)
    if tree_key not in candidate_cache:
        tree = generate_tree(job.m, job.tree_topology, job.seed)
        subtrees = enumerate_connected_subtrees(tree)
        maximum_candidates = int(config["resources"]["max_connected_subtrees"])
        if len(subtrees) > maximum_candidates:
            raise RuntimeError(
                f"{job.tree_topology} tree with m={job.m} has {len(subtrees)} candidates, "
                f"exceeding configured limit {maximum_candidates}; reduce m explicitly"
            )
        candidate_cache[tree_key] = (tree, subtree_incidence_matrix(subtrees, job.m))
    tree, candidates = candidate_cache[tree_key]

    clean_key = (
        job.n,
        job.m,
        job.tree_topology,
        job.branch_probability,
        job.seed,
    )
    if clean_key not in clean_cache:
        synthetic = generate_alpha_acyclic_hypergraph(
            n=job.n,
            m=job.m,
            tree=tree,
            branch_probability=job.branch_probability,
            seed=_derived_seed(
                job.seed,
                21,
                job.n,
                job.m,
                int(round(job.branch_probability * 1000)),
            ),
        )
        clean_cache[clean_key] = synthetic["incidence"]
    clean = clean_cache[clean_key]
    observed, num_flips = _observations_for_job(clean, job)

    rows: list[dict[str, Any]] = []
    experiment_id = f"{config['experiment_id']}-{job.index:05d}"
    for model_name, hyperparameters, model in _model_specifications(
        config, candidates, job
    ):
        start = time.perf_counter()
        model.fit(observed)
        runtime = time.perf_counter() - start
        predicted = model.predict()
        probabilities = model.predict_proba()
        metrics = recovery_metrics(clean, predicted, tree, observed, probabilities)
        categorical_entropy = np.nan
        maximum_subtree_probability = np.nan
        if hasattr(model, "distribution_"):
            distribution = np.asarray(model.distribution_)
            categorical_entropy = float(
                (-(distribution * np.log(np.clip(distribution, 1e-12, 1.0))).sum(axis=1)).mean()
            )
            maximum_subtree_probability = float(distribution.max(axis=1).mean())
        if model_name in {
            "FixedTreeAHSL",
            "NearestConnectedSubtree",
            "NoiseAwareMAPSubtree",
        } and metrics["running_intersection_violations"] != 0:
            raise RuntimeError(f"{model_name} produced a disconnected incidence row")
        rows.append(
            {
                "experiment_id": experiment_id,
                "seed": job.seed,
                "n": job.n,
                "m": job.m,
                "tree_topology": job.tree_topology,
                "branch_probability": job.branch_probability,
                "p_false_positive": job.p_false_positive,
                "p_false_negative": job.p_false_negative,
                "noise_setting": job.noise_setting,
                "num_observations": job.num_observations,
                "model": model_name,
                "hyperparameters": json.dumps(hyperparameters, sort_keys=True),
                "train_loss": float(model.train_loss_),
                **metrics,
                "runtime_seconds": runtime,
                "num_connected_subtrees": int(candidates.shape[0]),
                "num_corrupted_entries": num_flips,
                "mean_predicted_row_size": float(predicted.sum(axis=1).mean()),
                "singleton_prediction_fraction": float((predicted.sum(axis=1) == 1).mean()),
                "mean_categorical_entropy": categorical_entropy,
                "mean_max_subtree_probability": maximum_subtree_probability,
            }
        )
    return rows


def _configure_logging(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    LOGGER.setLevel(logging.INFO)
    LOGGER.handlers.clear()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    LOGGER.addHandler(stream_handler)
    LOGGER.addHandler(file_handler)


def run_experiment(
    config: dict[str, Any], max_runs: int | None = None
) -> dict[str, Path]:
    """Run selected paired datasets and write all required A0 artifacts."""
    repository_root = Path(__file__).resolve().parents[3]
    results_root = repository_root / "results"
    raw_path = results_root / "raw" / "a0_results.csv"
    summary_path = results_root / "aggregated" / "a0_summary.csv"
    tests_path = results_root / "aggregated" / "a0_statistical_tests.csv"
    report_path = results_root / "A0_RESEARCH_REPORT.md"
    log_path = results_root / "logs" / "a0_run.log"
    for directory in (raw_path.parent, summary_path.parent, results_root / "plots"):
        directory.mkdir(parents=True, exist_ok=True)
    _configure_logging(log_path)

    torch.set_num_threads(int(config["resources"]["torch_threads"]))
    set_all_seeds(int(config["seeds"][0]))
    jobs = _print_experiment_plan(config, _build_jobs(config), max_runs)
    candidate_cache: dict[tuple[int, str, int], tuple[Any, np.ndarray]] = {}
    clean_cache: dict[tuple[int, int, str, float, int], np.ndarray] = {}
    records: list[dict[str, Any]] = []
    start = time.perf_counter()
    for completed, job in enumerate(jobs, start=1):
        records.extend(_evaluate_job(config, job, candidate_cache, clean_cache))
        if completed == 1 or completed % 10 == 0 or completed == len(jobs):
            LOGGER.info("Completed %d/%d dataset cases", completed, len(jobs))

    raw = pd.DataFrame.from_records(records)
    raw.to_csv(raw_path, index=False)
    summary = aggregate_results(raw)
    summary.to_csv(summary_path, index=False)
    statistical_tests = paired_statistical_tests(
        raw,
        bootstrap_samples=int(config["statistics"]["bootstrap_samples"]),
        seed=int(config["statistics"]["seed"]),
    )
    statistical_tests.to_csv(tests_path, index=False)
    generate_plots(raw, results_root / "plots", config["plots"])
    write_research_report(raw, statistical_tests, report_path, config)
    LOGGER.info("Finished in %.2f seconds", time.perf_counter() - start)
    LOGGER.info("Raw rows: %d", len(raw))
    return {
        "raw": raw_path,
        "summary": summary_path,
        "statistical_tests": tests_path,
        "report": report_path,
        "log": log_path,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--max-runs",
        type=int,
        default=None,
        help="Cap the number of paired dataset cases after printing the full plan.",
    )
    arguments = parser.parse_args()
    config = _load_config(arguments.config)
    if arguments.dry_run:
        config = _dry_run_config(config)
    run_experiment(config, max_runs=arguments.max_runs)


if __name__ == "__main__":
    main()
