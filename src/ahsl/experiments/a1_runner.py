"""Run Phase A1 marginal-likelihood validation and held-out experiments."""

from __future__ import annotations

import argparse
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
from ahsl.experiments.a1_analysis import write_primary_analysis
from ahsl.join_tree_estimators import (
    BinaryMWST,
    BootstrapStabilityMWST,
    DataAgnosticRandomTree,
    NoiseCorrectedMWST,
)
from ahsl.marginal_tree_search import (
    EstimatedQMarginalTree,
    MarginalLikelihoodTreeSearch,
    enumerate_labeled_trees,
    tree_edge_signature,
)
from ahsl.metrics import recovery_metrics
from ahsl.models import DPNoiseAwareConnectedMLE, GeneratorPriorConnectedMAP
from ahsl.models.noise_likelihood import node_log_likelihoods
from ahsl.q_estimation import estimate_q_mle
from ahsl.subtree import (
    enumerate_connected_subtrees,
    generator_subtree_probability,
)
from ahsl.subtree_marginal import (
    brute_force_marginal_log_likelihood,
    marginal_log_likelihood,
    marginal_log_likelihood_from_node_logs,
)
from ahsl.synthetic import generate_alpha_acyclic_hypergraph
from ahsl.tree_perturbation import tree_edge_disagreement
from ahsl.trees import SUPPORTED_TOPOLOGIES, generate_tree


LOGGER = logging.getLogger("ahsl.a1")


@dataclass(frozen=True)
class Job:
    index: int
    n: int
    m: int
    topology: str
    q: float
    p_false_positive: float
    p_false_negative: float
    seed: int


def _derived_seed(base_seed: int, *coordinates: int) -> int:
    sequence = np.random.SeedSequence([base_seed, *coordinates])
    return int(sequence.generate_state(1, dtype=np.uint32)[0])


def _topology_index(topology: str) -> int:
    return SUPPORTED_TOPOLOGIES.index(topology)


def _load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


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


def _jobs(config: dict[str, Any]) -> list[Job]:
    product = itertools.product(
        config["n_values"],
        config["m_values"],
        config["tree_topologies"],
        config["branch_probabilities"],
        config["noise_settings"],
        config["seeds"],
    )
    return [
        Job(
            index=index,
            n=int(n),
            m=int(m),
            topology=str(topology),
            q=float(q),
            p_false_positive=float(noise["p_false_positive"]),
            p_false_negative=float(noise["p_false_negative"]),
            seed=int(seed),
        )
        for index, (n, m, topology, q, noise, seed) in enumerate(product)
    ]


def _tree_and_data(job: Job) -> tuple[nx.Graph, np.ndarray, np.ndarray]:
    topology_index = _topology_index(job.topology)
    tree = generate_tree(
        job.m,
        job.topology,
        _derived_seed(job.seed, 11, job.m, topology_index),
    )
    clean = generate_alpha_acyclic_hypergraph(
        job.n,
        job.m,
        tree,
        job.q,
        seed=_derived_seed(
            job.seed,
            21,
            job.n,
            job.m,
            topology_index,
            int(round(1000 * job.q)),
        ),
        simple_hypergraph=True,
    )["incidence"]
    observed = corrupt_incidence(
        clean,
        job.p_false_negative,
        job.p_false_positive,
        _derived_seed(
            job.seed,
            31,
            job.n,
            job.m,
            topology_index,
            int(round(1000 * job.q)),
            int(round(1000 * job.p_false_positive)),
            int(round(1000 * job.p_false_negative)),
            0,
            0,
        ),
    )["corrupted_incidence"]
    return tree, clean, observed


def _split_rows(
    clean: np.ndarray, observed: np.ndarray, fractions: list[float]
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    train_end = int(round(len(clean) * fractions[0]))
    validation_end = train_end + int(round(len(clean) * fractions[1]))
    return {
        "train": (clean[:train_end], observed[:train_end]),
        "validation": (
            clean[train_end:validation_end],
            observed[train_end:validation_end],
        ),
        "test": (clean[validation_end:], observed[validation_end:]),
    }


def _score_splits(
    tree: nx.Graph,
    q: float,
    splits: dict[str, tuple[np.ndarray, np.ndarray]],
    job: Job,
) -> dict[str, float]:
    return {
        f"{name}_nll_per_row": -marginal_log_likelihood(
            tree,
            observed,
            job.p_false_negative,
            job.p_false_positive,
            q,
        ).log_likelihood
        / len(observed)
        for name, (_, observed) in splits.items()
    }


def _fit_primary_trees(
    job: Job,
    true_tree: nx.Graph,
    train: np.ndarray,
    validation: np.ndarray,
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    specifications: list[tuple[str, Any, str]] = [
        ("GeneratingTreeOracle", None, "true_q"),
        (
            "DataAgnosticRandomTree",
            DataAgnosticRandomTree(
                job.m, _derived_seed(job.seed, 81, _topology_index(job.topology))
            ),
            "true_q",
        ),
        (
            "BinaryMWST",
            BinaryMWST(job.p_false_negative, job.p_false_positive),
            "true_q",
        ),
        (
            "NoiseCorrectedMWST",
            NoiseCorrectedMWST(job.p_false_negative, job.p_false_positive),
            "true_q",
        ),
        (
            "BootstrapStabilityMWST",
            BootstrapStabilityMWST(
                job.p_false_negative,
                job.p_false_positive,
                num_bootstrap_replicates=int(config["bootstrap_replicates"]),
                seed=_derived_seed(job.seed, 91, _topology_index(job.topology)),
            ),
            "true_q",
        ),
        (
            "OracleQMarginalTree",
            MarginalLikelihoodTreeSearch(
                job.p_false_negative,
                job.p_false_positive,
                job.q,
                max_iterations=int(config["tree_search_max_iterations"]),
            ),
            "true_q",
        ),
        (
            "EstimatedQMarginalTree",
            EstimatedQMarginalTree(
                job.p_false_negative,
                job.p_false_positive,
                q_bounds=tuple(config["q_bounds"]),
                max_outer_iterations=int(config["q_tree_outer_iterations"]),
                max_tree_iterations=int(config["tree_search_max_iterations"]),
            ),
            "estimated_q",
        ),
    ]
    fitted: list[dict[str, Any]] = []
    for name, estimator, q_source in specifications:
        start = time.perf_counter()
        if name == "GeneratingTreeOracle":
            tree = true_tree.copy()
            q = job.q
            diagnostics: dict[str, Any] = {}
        elif name == "EstimatedQMarginalTree":
            estimator.fit(train, validation)
            tree = estimator.predict_tree()
            q = estimator.q_
            diagnostics = {
                "num_iterations": estimator.selected_outer_iteration_,
                "evaluated_candidates": estimator.evaluated_candidates_,
                "validation_selected": True,
                "initial_tree": estimator.checkpoints_[0]["tree"],
                "initial_q": estimator.checkpoints_[0]["q"],
            }
        else:
            estimator.fit(train)
            tree = estimator.predict_tree()
            q = job.q
            diagnostics = {}
            if name == "OracleQMarginalTree":
                diagnostics = {
                    "num_iterations": estimator.num_iterations_,
                    "evaluated_candidates": estimator.evaluated_candidates_,
                    "converged": estimator.converged_,
                    "tree_changed": estimator.tree_changed_,
                    "initial_tree": estimator.initial_tree_,
                    "initial_q": job.q,
                    "mean_neighborhood_seconds": float(
                        np.mean(estimator.neighborhood_seconds_)
                    ),
                    "mean_neighborhood_size": float(
                        np.mean(estimator.neighborhood_sizes_)
                    ),
                }
        fitted.append(
            {
                "estimator": name,
                "tree": tree,
                "q": q,
                "q_source": q_source,
                "tree_runtime_seconds": time.perf_counter() - start,
                **diagnostics,
            }
        )
    return fitted


def _primary_record(
    job: Job,
    method: dict[str, Any],
    decoder_name: str,
    prediction: np.ndarray,
    decoder_runtime: float,
    splits: dict[str, tuple[np.ndarray, np.ndarray]],
    true_tree: nx.Graph,
) -> dict[str, Any]:
    tree = method["tree"]
    q = float(method["q"])
    test_clean, test_observed = splits["test"]
    metrics = recovery_metrics(test_clean, prediction, tree, test_observed)
    likelihoods = _score_splits(tree, q, splits, job)
    initial_likelihoods: dict[str, float] = {}
    if "initial_tree" in method:
        initial_likelihoods = _score_splits(
            method["initial_tree"], float(method["initial_q"]), splits, job
        )
    record = {
        "dataset_id": f"{job.topology}-seed-{job.seed:02d}",
        "seed": job.seed,
        "n": job.n,
        "m": job.m,
        "tree_topology": job.topology,
        "true_q": job.q,
        "estimated_q": q,
        "q_absolute_error": abs(q - job.q),
        "q_source": method["q_source"],
        "p_false_positive": job.p_false_positive,
        "p_false_negative": job.p_false_negative,
        "train_rows": len(splits["train"][0]),
        "validation_rows": len(splits["validation"][0]),
        "test_rows": len(test_clean),
        "estimator": method["estimator"],
        "decoder": decoder_name,
        "test_hamming_error": float(metrics["hamming_error"]),
        "test_exact_row_recovery": float(metrics["exact_row_recovery"]),
        "test_clean_f1": float(metrics["clean_f1"]),
        "test_riv": int(metrics["running_intersection_violations"]),
        "valid_clean_test_join_tree": running_intersection_violations(
            test_clean, tree
        )["num_violating_vertices"]
        == 0,
        "tree_edge_disagreement": tree_edge_disagreement(true_tree, tree),
        "tree_runtime_seconds": float(method["tree_runtime_seconds"]),
        "decoder_runtime_seconds": decoder_runtime,
        **likelihoods,
        "num_iterations": method.get("num_iterations", np.nan),
        "evaluated_candidates": method.get("evaluated_candidates", np.nan),
        "converged": method.get("converged", np.nan),
        "tree_changed": method.get("tree_changed", np.nan),
        "validation_selected": method.get("validation_selected", False),
        "mean_neighborhood_seconds": method.get(
            "mean_neighborhood_seconds", np.nan
        ),
        "mean_neighborhood_size": method.get("mean_neighborhood_size", np.nan),
    }
    for split_name in ["train", "validation", "test"]:
        key = f"{split_name}_nll_per_row"
        record[f"{split_name}_nll_gain_vs_initial"] = (
            initial_likelihoods.get(key, np.nan) - likelihoods[key]
        )
    return record


def _run_primary(config: dict[str, Any], jobs: list[Job]) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    for position, job in enumerate(jobs, start=1):
        LOGGER.info(
            "Primary dataset %d/%d: topology=%s seed=%d",
            position,
            len(jobs),
            job.topology,
            job.seed,
        )
        true_tree, clean, observed = _tree_and_data(job)
        splits = _split_rows(clean, observed, list(config["split_fractions"]))
        methods = _fit_primary_trees(
            job,
            true_tree,
            splits["train"][1],
            splits["validation"][1],
            config,
        )
        for method in methods:
            for decoder_name in ["MatchedPrior", "UniformConnectedMLE"]:
                start = time.perf_counter()
                if decoder_name == "MatchedPrior":
                    decoder = GeneratorPriorConnectedMAP(
                        method["tree"],
                        job.p_false_negative,
                        job.p_false_positive,
                        method["q"],
                    )
                else:
                    decoder = DPNoiseAwareConnectedMLE(
                        method["tree"],
                        job.p_false_negative,
                        job.p_false_positive,
                    )
                prediction = decoder.fit(splits["test"][1]).predict()
                records.append(
                    _primary_record(
                        job,
                        method,
                        decoder_name,
                        prediction,
                        time.perf_counter() - start,
                        splits,
                        true_tree,
                    )
                )
    return pd.DataFrame.from_records(records)


def _run_validation(config: dict[str, Any]) -> pd.DataFrame:
    records = []
    tolerance = float(config["comparison_tolerance"])
    for topology, q, noise, repetitions, seed in itertools.product(
        config["tree_topologies"],
        config["branch_probabilities"],
        config["noise_settings"],
        config["observation_repetitions"],
        config["seeds"],
    ):
        m = int(config["m"])
        topology_index = _topology_index(topology)
        tree = generate_tree(m, topology, _derived_seed(seed, 111, topology_index))
        clean = generate_alpha_acyclic_hypergraph(
            int(config["rows_per_case"]),
            m,
            tree,
            float(q),
            seed=_derived_seed(seed, 112, topology_index, int(100 * q)),
        )["incidence"]
        draws = [
            corrupt_incidence(
                clean,
                float(noise["p_false_negative"]),
                float(noise["p_false_positive"]),
                _derived_seed(seed, 113, topology_index, repetition),
            )["corrupted_incidence"]
            for repetition in range(int(repetitions))
        ]
        observed = draws[0] if int(repetitions) == 1 else np.stack(draws)
        exact = marginal_log_likelihood(
            tree,
            observed,
            float(noise["p_false_negative"]),
            float(noise["p_false_positive"]),
            float(q),
        ).row_log_likelihoods
        reference = brute_force_marginal_log_likelihood(
            tree,
            observed,
            float(noise["p_false_negative"]),
            float(noise["p_false_positive"]),
            float(q),
        )
        errors = np.abs(exact - reference)
        prior_mass = sum(
            generator_subtree_probability(tree, support, float(q))
            for support in enumerate_connected_subtrees(tree)
        )
        records.append(
            {
                "topology": topology,
                "q": q,
                "noise": noise["name"],
                "repetitions": repetitions,
                "seed": seed,
                "row_comparisons": len(exact),
                "max_absolute_error": float(errors.max()),
                "mismatches": int((errors > tolerance).sum()),
                "prior_mass_error": abs(prior_mass - 1.0),
            }
        )
    return pd.DataFrame.from_records(records)


def _run_q_identifiability(config: dict[str, Any], jobs: list[Job]) -> pd.DataFrame:
    records = []
    for position, job in enumerate(jobs, start=1):
        LOGGER.info("q diagnostic %d/%d", position, len(jobs))
        tree, _, observed = _tree_and_data(job)
        start = time.perf_counter()
        estimate = estimate_q_mle(
            tree,
            observed,
            job.p_false_negative,
            job.p_false_positive,
            bounds=tuple(config["q_bounds"]),
        )
        records.append(
            {
                "n": job.n,
                "m": job.m,
                "topology": job.topology,
                "seed": job.seed,
                "true_q": job.q,
                "estimated_q": estimate.q,
                "absolute_error": abs(estimate.q - job.q),
                "evaluations": estimate.evaluations,
                "runtime_seconds": time.perf_counter() - start,
            }
        )
    return pd.DataFrame.from_records(records)


def _matched_prediction(
    tree: nx.Graph, observed: np.ndarray, job: Job
) -> np.ndarray:
    return GeneratorPriorConnectedMAP(
        tree,
        job.p_false_negative,
        job.p_false_positive,
        job.q,
    ).fit(observed).predict()


def _run_small_global(config: dict[str, Any], jobs: list[Job]) -> pd.DataFrame:
    records = []
    for position, job in enumerate(jobs, start=1):
        LOGGER.info("Global-search dataset %d/%d", position, len(jobs))
        true_tree, clean, observed = _tree_and_data(job)
        splits = _split_rows(clean, observed, list(config["split_fractions"]))
        train_observed = splits["train"][1]
        local = MarginalLikelihoodTreeSearch(
            job.p_false_negative,
            job.p_false_positive,
            job.q,
            max_iterations=int(config["tree_search_max_iterations"]),
        ).fit(train_observed)
        local_tree = local.predict_tree()
        log_zero, log_one, _ = node_log_likelihoods(
            train_observed, job.p_false_negative, job.p_false_positive
        )
        global_tree = None
        global_score = -np.inf
        global_signature = None
        count = 0
        start = time.perf_counter()
        for candidate in enumerate_labeled_trees(job.m):
            count += 1
            score = marginal_log_likelihood_from_node_logs(
                candidate, log_zero, log_one, job.q
            ).log_likelihood
            signature = tree_edge_signature(candidate)
            if score > global_score + 1e-12 or (
                np.isclose(score, global_score, rtol=1e-12, atol=1e-12)
                and (global_signature is None or signature < global_signature)
            ):
                global_tree = candidate.copy()
                global_score = score
                global_signature = signature
        global_runtime = time.perf_counter() - start
        test_clean, test_observed = splits["test"]
        local_hamming = recovery_metrics(
            test_clean,
            _matched_prediction(local_tree, test_observed, job),
            local_tree,
            test_observed,
        )["hamming_error"]
        global_hamming = recovery_metrics(
            test_clean,
            _matched_prediction(global_tree, test_observed, job),
            global_tree,
            test_observed,
        )["hamming_error"]
        records.append(
            {
                "m": job.m,
                "n": job.n,
                "topology": job.topology,
                "seed": job.seed,
                "num_labeled_trees": count,
                "local_is_global_optimum": tree_edge_signature(local_tree)
                == global_signature,
                "train_objective_gap": global_score - local.log_likelihood_,
                "test_hamming_local": local_hamming,
                "test_hamming_global": global_hamming,
                "test_hamming_gap": local_hamming - global_hamming,
                "local_tree_disagreement": tree_edge_disagreement(
                    true_tree, local_tree
                ),
                "global_tree_disagreement": tree_edge_disagreement(
                    true_tree, global_tree
                ),
                "local_runtime_seconds": local.runtime_seconds_,
                "global_runtime_seconds": global_runtime,
            }
        )
    return pd.DataFrame.from_records(records)


def run(config_path: Path, max_runs: int | None = None) -> None:
    config = _load_config(config_path)
    experiment_type = str(config["experiment_type"])
    result_root = Path("results/a1")
    _configure_logging(result_root / "logs" / f"{experiment_type}.log")
    jobs = _jobs(config) if experiment_type != "a1_validation" else []
    if max_runs is not None:
        jobs = jobs[:max_runs]
    LOGGER.info("Experiment %s; dataset jobs=%d", experiment_type, len(jobs))

    raw_directory = result_root / "raw"
    raw_directory.mkdir(parents=True, exist_ok=True)
    if experiment_type == "a1_validation":
        frame = _run_validation(config)
    elif experiment_type == "a1_primary":
        frame = _run_primary(config, jobs)
    elif experiment_type == "a1_q_identifiability":
        frame = _run_q_identifiability(config, jobs)
    elif experiment_type == "a1_small_global_search":
        frame = _run_small_global(config, jobs)
    else:
        raise ValueError(f"unknown experiment_type: {experiment_type}")

    output = raw_directory / f"{experiment_type}_results.csv"
    frame.to_csv(output, index=False)
    LOGGER.info("Wrote %d rows to %s", len(frame), output)
    if experiment_type == "a1_primary":
        write_primary_analysis(frame, result_root / "aggregated")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--max-runs", type=int)
    args = parser.parse_args()
    run(args.config, args.max_runs)


if __name__ == "__main__":
    main()
