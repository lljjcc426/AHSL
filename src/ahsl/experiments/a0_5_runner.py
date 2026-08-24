"""Configuration-driven staged experiments for AHSL Phase A0.5."""

from __future__ import annotations

import argparse
import copy
import itertools
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np
import pandas as pd
import yaml

from ahsl.acyclicity import running_intersection_violations
from ahsl.corruption import corrupt_incidence
from ahsl.experiments.a0_5_analysis import (
    rebuild_combined_raw,
    write_analysis_outputs,
)
from ahsl.join_tree_recovery import IntersectionMWSTJoinTree
from ahsl.metrics import recovery_metrics
from ahsl.models import (
    DPNearestConnectedSubtree,
    DPNoiseAwareConnectedMLE,
    GeneratorPriorConnectedMAP,
    NoiseAwareIndependentMLE,
    NoiseAwareIndependentNonemptyMLE,
)
from ahsl.models.noise_likelihood import node_log_likelihoods
from ahsl.structural_contamination import contaminate_incidence_rows
from ahsl.subtree import enumerate_connected_subtrees
from ahsl.synthetic import generate_alpha_acyclic_hypergraph
from ahsl.tree_dp import maximum_weight_connected_subtree
from ahsl.tree_perturbation import (
    perturb_tree_by_edge_swaps,
    tree_edge_disagreement,
)
from ahsl.trees import SUPPORTED_TOPOLOGIES, generate_tree


LOGGER = logging.getLogger("ahsl.a0_5")


@dataclass(frozen=True)
class BaseJob:
    index: int
    n: int
    m: int
    topology: str
    branch_probability: float
    noise_name: str
    p_false_positive: float
    p_false_negative: float
    repetitions: int
    seed: int


def _load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    if not isinstance(config, dict):
        raise ValueError("configuration root must be a mapping")
    return config


def _derived_seed(base_seed: int, *coordinates: int) -> int:
    sequence = np.random.SeedSequence([base_seed, *coordinates])
    return int(sequence.generate_state(1, dtype=np.uint32)[0])


def _topology_index(topology: str) -> int:
    return SUPPORTED_TOPOLOGIES.index(topology)


def _build_jobs(config: dict[str, Any]) -> list[BaseJob]:
    product = itertools.product(
        config["n_values"],
        config["m_values"],
        config["tree_topologies"],
        config["branch_probabilities"],
        config["noise_settings"],
        config["observation_repetitions"],
        config["seeds"],
    )
    jobs = []
    for index, (n, m, topology, branch, noise, repetitions, seed) in enumerate(product):
        jobs.append(
            BaseJob(
                index=index,
                n=int(n),
                m=int(m),
                topology=str(topology),
                branch_probability=float(branch),
                noise_name=str(noise["name"]),
                p_false_positive=float(noise["p_false_positive"]),
                p_false_negative=float(noise["p_false_negative"]),
                repetitions=int(repetitions),
                seed=int(seed),
            )
        )
    return jobs


def _dry_run_config(config: dict[str, Any]) -> dict[str, Any]:
    dry = copy.deepcopy(config)
    dry["n_values"] = [10]
    dry["m_values"] = [5]
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
    dry["dry_run"] = True
    if "tree_swaps" in dry:
        dry["tree_swaps"] = [0, 1, "random"]
    if "offclass_probabilities" in dry:
        dry["offclass_probabilities"] = [0.0, 0.2]
    return dry


def _configure_logging(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    LOGGER.setLevel(logging.INFO)
    LOGGER.handlers.clear()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    file_handler = logging.FileHandler(path, mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    LOGGER.addHandler(stream)
    LOGGER.addHandler(file_handler)


def _model_evaluations_per_job(config: dict[str, Any]) -> int:
    experiment_type = config["experiment_type"]
    if experiment_type in {"scaling", "core"}:
        return len(config["models"])
    if experiment_type == "wrong_tree":
        return 3 * len(config["tree_swaps"])
    if experiment_type == "offclass":
        return 3 * len(config["offclass_probabilities"])
    if experiment_type == "a1_gate":
        return 4
    return 0


def _plan(config: dict[str, Any], jobs: list[BaseJob], max_runs: int | None) -> list[BaseJob]:
    selected = jobs if max_runs is None else jobs[:max_runs]
    brute_force = bool(config["resources"]["brute_force_enabled"])
    experiment_type = config["experiment_type"]
    if experiment_type == "validation":
        if not brute_force:
            raise ValueError("validation must enable brute-force oracle checks")
        if max(config["m_values"]) > 12:
            raise ValueError("validation brute force is limited to m <= 12")
    elif brute_force:
        raise ValueError("brute-force enumeration must be disabled outside validation")
    LOGGER.info("A0.5 experiment plan: %s", experiment_type)
    LOGGER.info("  number of dataset cases: %d", len(selected))
    LOGGER.info(
        "  number of model evaluations: %d",
        len(selected) * _model_evaluations_per_job(config),
    )
    LOGGER.info("  largest n: %d", max(job.n for job in selected))
    LOGGER.info("  largest m: %d", max(job.m for job in selected))
    LOGGER.info("  estimated runtime class: %s", config["resources"]["runtime_class"])
    LOGGER.info("  brute-force enumeration enabled: %s", brute_force)
    return selected


def _tree_for_job(job: BaseJob) -> nx.Graph:
    return generate_tree(
        job.m,
        job.topology,
        _derived_seed(job.seed, 11, job.m, _topology_index(job.topology)),
    )


def _clean_for_job(
    job: BaseJob, tree: nx.Graph, simple_hypergraph: bool = False
) -> dict[str, Any]:
    return generate_alpha_acyclic_hypergraph(
        job.n,
        job.m,
        tree,
        job.branch_probability,
        seed=_derived_seed(
            job.seed,
            21,
            job.n,
            job.m,
            _topology_index(job.topology),
            int(round(1000 * job.branch_probability)),
        ),
        simple_hypergraph=simple_hypergraph,
    )


def _observations(clean: np.ndarray, job: BaseJob, extra_coordinate: int = 0) -> np.ndarray:
    observations = []
    for repetition in range(job.repetitions):
        result = corrupt_incidence(
            clean,
            job.p_false_negative,
            job.p_false_positive,
            _derived_seed(
                job.seed,
                31,
                job.n,
                job.m,
                _topology_index(job.topology),
                int(round(1000 * job.branch_probability)),
                int(round(1000 * job.p_false_positive)),
                int(round(1000 * job.p_false_negative)),
                extra_coordinate,
                repetition,
            ),
        )
        observations.append(result["corrupted_incidence"])
    stacked = np.stack(observations)
    return stacked[0] if job.repetitions == 1 else stacked


def _base_metadata(
    experiment_type: str,
    experiment_id: str,
    job: BaseJob,
    simple_hypergraph: bool,
    tree_source: str,
    disagreement: float,
    offclass_fraction: float,
    clean_riv: int,
    requested_tree_swaps: float = 0.0,
    requested_offclass_fraction: float = 0.0,
) -> dict[str, Any]:
    return {
        "experiment_type": experiment_type,
        "experiment_id": experiment_id,
        "seed": job.seed,
        "n": job.n,
        "m": job.m,
        "tree_topology": job.topology,
        "branch_probability": job.branch_probability,
        "noise_setting": job.noise_name,
        "p_false_positive": job.p_false_positive,
        "p_false_negative": job.p_false_negative,
        "num_observations": job.repetitions,
        "simple_hypergraph": simple_hypergraph,
        "tree_source": tree_source,
        "tree_edge_disagreement": disagreement,
        "requested_tree_swaps": requested_tree_swaps,
        "requested_offclass_fraction": requested_offclass_fraction,
        "offclass_fraction": offclass_fraction,
        "clean_riv": clean_riv,
    }


def _fit_record(
    model: Any,
    clean: np.ndarray,
    observed: np.ndarray,
    metric_tree: nx.Graph,
    metadata: dict[str, Any],
    setup_seconds: float = 0.0,
    estimated_tree_clean_riv: float = np.nan,
    estimated_incidence_riv: float = np.nan,
) -> dict[str, Any]:
    start = time.perf_counter()
    model.fit(observed)
    runtime = setup_seconds + time.perf_counter() - start
    prediction = model.predict()
    metrics = recovery_metrics(clean, prediction, metric_tree, observed)
    n, m = clean.shape
    return {
        **metadata,
        "model": model.name,
        "predicted_riv": int(metrics["running_intersection_violations"]),
        "clean_hamming_error": float(metrics["hamming_error"]),
        "clean_precision": float(metrics["clean_precision"]),
        "clean_recall": float(metrics["clean_recall"]),
        "clean_f1": float(metrics["clean_f1"]),
        "exact_row_recovery": float(metrics["exact_row_recovery"]),
        "mean_symmetric_difference": float(metrics["mean_symmetric_difference"]),
        "average_hyperedge_jaccard": float(metrics["average_hyperedge_jaccard"]),
        "average_hyperedge_f1": float(metrics["average_hyperedge_f1"]),
        "clean_density": float(metrics["clean_density"]),
        "predicted_density": float(metrics["predicted_density"]),
        "runtime_seconds": runtime,
        "runtime_per_row": runtime / n,
        "runtime_per_nm": runtime / (n * m),
        "optimal_tie_fraction": float(
            getattr(model, "optimal_tie_fraction_", np.nan)
        ),
        "mean_selected_subtree_size": float(
            np.mean(getattr(model, "selected_sizes_", prediction.sum(axis=1)))
        ),
        "objective_value": float(
            np.mean(getattr(model, "row_objectives_", np.full(n, np.nan)))
        ),
        "estimated_tree_clean_riv": estimated_tree_clean_riv,
        "estimated_incidence_riv": estimated_incidence_riv,
    }


def _make_model(name: str, job: BaseJob, tree: nx.Graph) -> Any | None:
    if name == "NoiseAwareIndependentMLE":
        return NoiseAwareIndependentMLE(
            job.p_false_negative, job.p_false_positive
        )
    if name == "NoiseAwareIndependentNonemptyMLE":
        return NoiseAwareIndependentNonemptyMLE(
            job.p_false_negative, job.p_false_positive
        )
    if name == "DPNearestConnectedSubtree":
        return DPNearestConnectedSubtree(tree)
    if name == "DPNoiseAwareConnectedMLE":
        return DPNoiseAwareConnectedMLE(
            tree, job.p_false_negative, job.p_false_positive
        )
    if name == "GeneratorPriorConnectedMAP":
        if job.p_false_negative in {0.0, 1.0} or job.p_false_positive in {0.0, 1.0}:
            return None
        return GeneratorPriorConnectedMAP(
            tree,
            job.p_false_negative,
            job.p_false_positive,
            job.branch_probability,
        )
    raise ValueError(f"unsupported A0.5 model: {name}")


def _run_standard(config: dict[str, Any], jobs: list[BaseJob]) -> list[dict[str, Any]]:
    experiment_type = config["experiment_type"]
    rows: list[dict[str, Any]] = []
    for completed, job in enumerate(jobs, start=1):
        tree = _tree_for_job(job)
        sample = _clean_for_job(job, tree)
        clean = sample["incidence"]
        observed = _observations(clean, job)
        experiment_id = f"a0_5_{experiment_type}-{job.index:06d}"
        metadata = _base_metadata(
            experiment_type,
            experiment_id,
            job,
            False,
            "true_tree",
            0.0,
            0.0,
            0,
        )
        for model_name in config["models"]:
            model = _make_model(model_name, job, tree)
            if model is not None:
                rows.append(_fit_record(model, clean, observed, tree, metadata))
        if completed == 1 or completed % 100 == 0 or completed == len(jobs):
            LOGGER.info("Completed %d/%d dataset cases", completed, len(jobs))
    return rows


def _run_wrong_tree(config: dict[str, Any], jobs: list[BaseJob]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for completed, job in enumerate(jobs, start=1):
        true_tree = _tree_for_job(job)
        clean = _clean_for_job(job, true_tree)["incidence"]
        observed = _observations(clean, job)
        for variant_index, requested in enumerate(config["tree_swaps"]):
            if requested == "random":
                model_tree = generate_tree(
                    job.m,
                    "random",
                    _derived_seed(job.seed, 71, job.m, _topology_index(job.topology)),
                )
                source = "independent_random"
                requested_value = -1.0
            else:
                requested_value = float(requested)
                model_tree = perturb_tree_by_edge_swaps(
                    true_tree,
                    int(requested),
                    _derived_seed(job.seed, 72, int(requested), job.m),
                )
                source = "true_tree" if int(requested) == 0 else f"swaps_{requested}"
            disagreement = tree_edge_disagreement(true_tree, model_tree)
            experiment_id = f"a0_5_wrong_tree-{job.index:06d}-{variant_index:02d}"
            metadata = _base_metadata(
                "wrong_tree",
                experiment_id,
                job,
                False,
                source,
                disagreement,
                0.0,
                0,
                requested_tree_swaps=requested_value,
            )
            independent = NoiseAwareIndependentNonemptyMLE(
                job.p_false_negative, job.p_false_positive
            )
            rows.append(_fit_record(independent, clean, observed, true_tree, metadata))
            connected = DPNoiseAwareConnectedMLE(
                model_tree, job.p_false_negative, job.p_false_positive
            )
            rows.append(_fit_record(connected, clean, observed, model_tree, metadata))
            true_model = DPNoiseAwareConnectedMLE(
                true_tree, job.p_false_negative, job.p_false_positive
            )
            true_row = _fit_record(true_model, clean, observed, true_tree, metadata)
            true_row["model"] = "DPNoiseAwareConnectedMLETrueTree"
            rows.append(true_row)
        if completed == 1 or completed % 20 == 0 or completed == len(jobs):
            LOGGER.info("Completed %d/%d base datasets", completed, len(jobs))
    return rows


def _run_offclass(config: dict[str, Any], jobs: list[BaseJob]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for completed, job in enumerate(jobs, start=1):
        tree = _tree_for_job(job)
        original = _clean_for_job(job, tree)["incidence"]
        for epsilon_index, epsilon in enumerate(config["offclass_probabilities"]):
            contamination = contaminate_incidence_rows(
                original,
                tree,
                float(epsilon),
                _derived_seed(job.seed, 81, epsilon_index, job.m),
            )
            clean = contamination["incidence"]
            observed = _observations(clean, job, extra_coordinate=epsilon_index + 1)
            experiment_id = f"a0_5_offclass-{job.index:06d}-{epsilon_index:02d}"
            metadata = _base_metadata(
                "offclass",
                experiment_id,
                job,
                False,
                "true_tree",
                0.0,
                float(contamination["offclass_fraction"]),
                int(contamination["clean_riv"]),
                requested_offclass_fraction=float(epsilon),
            )
            for name in (
                "NoiseAwareIndependentMLE",
                "NoiseAwareIndependentNonemptyMLE",
                "DPNoiseAwareConnectedMLE",
            ):
                model = _make_model(name, job, tree)
                rows.append(_fit_record(model, clean, observed, tree, metadata))
        if completed == 1 or completed % 20 == 0 or completed == len(jobs):
            LOGGER.info("Completed %d/%d base datasets", completed, len(jobs))
    return rows


def _run_a1_gate(config: dict[str, Any], jobs: list[BaseJob]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for completed, job in enumerate(jobs, start=1):
        true_tree = _tree_for_job(job)
        sample = _clean_for_job(job, true_tree, simple_hypergraph=True)
        clean = sample["incidence"]
        observed = _observations(clean, job)
        observation_array = np.asarray(observed)
        majority = (
            observation_array
            if observation_array.ndim == 2
            else (observation_array.mean(axis=0) >= 0.5).astype(np.int8)
        )
        independent_model = NoiseAwareIndependentMLE(
            job.p_false_negative, job.p_false_positive
        ).fit(observed)
        sources = {
            "observed_majority": np.asarray(majority, dtype=np.int8),
            "independent_mle": independent_model.predict(),
            "clean_oracle": clean,
        }
        for source_index, (source, incidence_estimate) in enumerate(sources.items()):
            start = time.perf_counter()
            estimated_tree = (
                IntersectionMWSTJoinTree().fit(incidence_estimate).predict_tree()
            )
            tree_runtime = time.perf_counter() - start
            disagreement = tree_edge_disagreement(true_tree, estimated_tree)
            clean_tree_riv = running_intersection_violations(clean, estimated_tree)[
                "num_violating_vertices"
            ]
            estimated_incidence_riv = running_intersection_violations(
                incidence_estimate, estimated_tree
            )["num_violating_vertices"]
            experiment_id = f"a0_5_a1_gate-{job.index:06d}-{source_index:02d}"
            metadata = _base_metadata(
                "a1_gate",
                experiment_id,
                job,
                True,
                source,
                disagreement,
                0.0,
                0,
            )
            model = DPNoiseAwareConnectedMLE(
                estimated_tree, job.p_false_negative, job.p_false_positive
            )
            model.name = "MWST+DPNoiseAwareConnectedMLE"
            rows.append(
                _fit_record(
                    model,
                    clean,
                    observed,
                    estimated_tree,
                    metadata,
                    setup_seconds=tree_runtime,
                    estimated_tree_clean_riv=float(clean_tree_riv),
                    estimated_incidence_riv=float(estimated_incidence_riv),
                )
            )
        reference_id = f"a0_5_a1_gate-{job.index:06d}-true"
        reference_metadata = _base_metadata(
            "a1_gate",
            reference_id,
            job,
            True,
            "true_tree",
            0.0,
            0.0,
            0,
        )
        reference = DPNoiseAwareConnectedMLE(
            true_tree, job.p_false_negative, job.p_false_positive
        )
        reference.name = "TrueTree+DPNoiseAwareConnectedMLE"
        rows.append(
            _fit_record(
                reference,
                clean,
                observed,
                true_tree,
                reference_metadata,
                estimated_tree_clean_riv=0.0,
                estimated_incidence_riv=0.0,
            )
        )
        if completed == 1 or completed % 20 == 0 or completed == len(jobs):
            LOGGER.info("Completed %d/%d A1-gate datasets", completed, len(jobs))
    return rows


def _canonical_brute(
    candidates: list[frozenset[int]], scores: np.ndarray
) -> tuple[float, frozenset[int], bool]:
    best = float(np.max(scores))
    indices = np.flatnonzero(np.isclose(scores, best, rtol=1e-12, atol=1e-12))
    optima = [candidates[index] for index in indices]
    chosen = min(optima, key=lambda nodes: (len(nodes), tuple(sorted(nodes))))
    return best, chosen, len(optima) > 1


def _run_validation(config: dict[str, Any]) -> pd.DataFrame:
    records = []
    per_topology = int(config["comparisons_per_topology"])
    for topology in config["tree_topologies"]:
        counts = {
            category: {
                "comparisons": 0,
                "objective_mismatches": 0,
                "unique_prediction_mismatches": 0,
            }
            for category in ("generic_weights", "hamming", "noise_likelihood")
        }
        for seed in range(per_topology):
            m = int(config["m_values"][seed % len(config["m_values"])])
            tree = generate_tree(m, topology, seed)
            candidates = enumerate_connected_subtrees(tree)
            rng = np.random.default_rng(seed + 9000)

            weights = rng.integers(-3, 4, size=m).astype(float)
            scores = np.array([weights[list(nodes)].sum() for nodes in candidates])
            best, expected, tied = _canonical_brute(candidates, scores)
            result = maximum_weight_connected_subtree(tree, weights)
            category = counts["generic_weights"]
            category["comparisons"] += 1
            category["objective_mismatches"] += int(
                not np.isclose(result["objective"], best)
            )
            category["unique_prediction_mismatches"] += int(
                not tied and result["selected_nodes"] != expected
            )

            observed = rng.integers(0, 2, size=(3, 1, m), dtype=np.int8)
            hamming_model = DPNearestConnectedSubtree(tree).fit(observed)
            masks = np.zeros((len(candidates), m), dtype=np.int8)
            for index, nodes in enumerate(candidates):
                masks[index, list(nodes)] = 1
            hamming_scores = -np.not_equal(
                masks[:, None, :], observed[:, 0, :][None, :, :]
            ).sum(axis=(1, 2)).astype(float)
            best, expected, tied = _canonical_brute(candidates, hamming_scores)
            category = counts["hamming"]
            category["comparisons"] += 1
            category["objective_mismatches"] += int(
                not np.isclose(hamming_model.row_objectives_[0], best + observed.sum())
            )
            predicted = frozenset(np.flatnonzero(hamming_model.predict()[0]))
            category["unique_prediction_mismatches"] += int(
                not tied and predicted != expected
            )

            p_false_negative, p_false_positive = (
                (0.0, 0.0),
                (0.0, 0.2),
                (0.2, 0.0),
                (0.2, 0.2),
            )[seed % 4]
            truth = np.zeros((1, m), dtype=np.int8)
            truth[0, list(candidates[int(rng.integers(len(candidates)))])] = 1
            noisy = []
            for repetition in range(3):
                noisy.append(
                    corrupt_incidence(
                        truth,
                        p_false_negative,
                        p_false_positive,
                        _derived_seed(seed, 91, repetition),
                    )["corrupted_incidence"]
                )
            noisy_array = np.stack(noisy)
            likelihood_model = DPNoiseAwareConnectedMLE(
                tree, p_false_negative, p_false_positive
            ).fit(noisy_array)
            log_zero, log_one, _ = node_log_likelihoods(
                noisy_array, p_false_negative, p_false_positive
            )
            likelihood_scores = []
            for nodes in candidates:
                selected = np.zeros(m, dtype=bool)
                selected[list(nodes)] = True
                likelihood_scores.append(
                    log_one[0, selected].sum() + log_zero[0, ~selected].sum()
                )
            best, expected, tied = _canonical_brute(
                candidates, np.asarray(likelihood_scores)
            )
            category = counts["noise_likelihood"]
            category["comparisons"] += 1
            category["objective_mismatches"] += int(
                not np.isclose(likelihood_model.row_objectives_[0], best)
            )
            predicted = frozenset(np.flatnonzero(likelihood_model.predict()[0]))
            category["unique_prediction_mismatches"] += int(
                not tied and predicted != expected
            )
        for category, values in counts.items():
            records.append({"tree_topology": topology, "category": category, **values})
    return pd.DataFrame.from_records(records)


def run(config: dict[str, Any], max_runs: int | None = None) -> None:
    repository_root = Path(__file__).resolve().parents[3]
    results_root = repository_root / "results" / "a0_5"
    raw_directory = results_root / "raw"
    aggregate_directory = results_root / "aggregated"
    log_directory = results_root / "logs"
    raw_directory.mkdir(parents=True, exist_ok=True)
    aggregate_directory.mkdir(parents=True, exist_ok=True)
    experiment_type = config["experiment_type"]
    _configure_logging(log_directory / f"a0_5_{experiment_type}.log")

    jobs = _plan(config, _build_jobs(config), max_runs)
    start = time.perf_counter()
    if experiment_type == "validation":
        validation = _run_validation(config)
        validation.to_csv(
            aggregate_directory / "a0_5_dp_validation.csv", index=False
        )
        LOGGER.info("Validation comparisons: %d", validation["comparisons"].sum())
        LOGGER.info(
            "Objective mismatches: %d",
            validation["objective_mismatches"].sum(),
        )
        LOGGER.info(
            "Unique-solution prediction mismatches: %d",
            validation["unique_prediction_mismatches"].sum(),
        )
        return
    if experiment_type in {"scaling", "core"}:
        records = _run_standard(config, jobs)
    elif experiment_type == "wrong_tree":
        records = _run_wrong_tree(config, jobs)
    elif experiment_type == "offclass":
        records = _run_offclass(config, jobs)
    elif experiment_type == "a1_gate":
        records = _run_a1_gate(config, jobs)
    else:
        raise ValueError(f"unsupported experiment_type: {experiment_type}")
    raw = pd.DataFrame.from_records(records)
    suffix = "_dry_run" if config.get("dry_run", False) else ""
    raw.to_csv(raw_directory / f"a0_5_{experiment_type}{suffix}_results.csv", index=False)
    if not config.get("dry_run", False):
        combined = rebuild_combined_raw(raw_directory)
        write_analysis_outputs(combined, aggregate_directory)
    LOGGER.info("Raw rows: %d", len(raw))
    LOGGER.info("Finished in %.2f seconds", time.perf_counter() - start)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-runs", type=int, default=None)
    arguments = parser.parse_args()
    config = _load_config(arguments.config)
    if arguments.dry_run:
        config = _dry_run_config(config)
    run(config, arguments.max_runs)


if __name__ == "__main__":
    main()

