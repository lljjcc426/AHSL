"""Run the bounded Phase A1.5 posterior-risk validation and experiment."""

from __future__ import annotations

import argparse
import itertools
import logging
import time
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np
import pandas as pd
import yaml
from scipy.special import logsumexp

from ahsl.acyclicity import running_intersection_violations
from ahsl.corruption import corrupt_incidence
from ahsl.experiments.a1_runner import (
    Job,
    _derived_seed,
    _fit_primary_trees,
    _jobs,
    _score_splits,
    _split_rows,
    _topology_index,
    _tree_and_data,
)
from ahsl.metrics import recovery_metrics
from ahsl.models.noise_likelihood import node_log_likelihoods
from ahsl.posterior_decoders import (
    ConnectedBayesHamming,
    PosteriorMAPConnected,
    PosteriorMedianUnconstrained,
    posterior_hamming_risk,
)
from ahsl.posterior_marginals import posterior_node_marginals
from ahsl.q_estimation import estimate_q_mle
from ahsl.subtree import enumerate_connected_subtrees, generator_subtree_probability
from ahsl.synthetic import generate_alpha_acyclic_hypergraph
from ahsl.tree_perturbation import tree_edge_disagreement
from ahsl.trees import generate_tree


LOGGER = logging.getLogger("ahsl.a1_5")


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


def _support_posterior(
    tree: nx.Graph,
    observed: np.ndarray,
    p_false_negative: float,
    p_false_positive: float,
    q: float,
) -> tuple[np.ndarray, np.ndarray]:
    log_zero, log_one, _ = node_log_likelihoods(
        observed, p_false_negative, p_false_positive
    )
    masks: list[np.ndarray] = []
    scores: list[np.ndarray] = []
    for support in enumerate_connected_subtrees(tree):
        prior = generator_subtree_probability(tree, support, q)
        if prior == 0.0:
            continue
        mask = np.zeros(tree.number_of_nodes(), dtype=np.int8)
        mask[list(support)] = 1
        selected = mask.astype(bool)
        masks.append(mask)
        scores.append(
            np.log(prior)
            + log_one[:, selected].sum(axis=1)
            + log_zero[:, ~selected].sum(axis=1)
        )
    score_matrix = np.stack(scores, axis=1)
    probabilities = np.exp(
        score_matrix - logsumexp(score_matrix, axis=1, keepdims=True)
    )
    return np.stack(masks), probabilities


def _all_binary_actions(m: int) -> np.ndarray:
    return np.asarray(list(itertools.product([0, 1], repeat=m)), dtype=np.int8)


def _validation_case(
    tree: nx.Graph,
    observed: np.ndarray,
    topology: str,
    q: float,
    noise_name: str,
    p_false_negative: float,
    p_false_positive: float,
    repetitions: int,
    seed: int,
    tolerance: float,
) -> dict[str, Any]:
    support_masks, support_probabilities = _support_posterior(
        tree, observed, p_false_negative, p_false_positive, q
    )
    reference_marginals = support_probabilities @ support_masks
    result = posterior_node_marginals(
        tree, observed, p_false_negative, p_false_positive, q
    )
    marginal_errors = np.abs(result.node_marginals - reference_marginals)
    root_error = 0.0
    for root in range(tree.number_of_nodes()):
        rooted = posterior_node_marginals(
            tree, observed, p_false_negative, p_false_positive, q, root=root
        )
        root_error = max(
            root_error,
            float(np.max(np.abs(rooted.node_marginals - result.node_marginals))),
        )

    map_decoder = PosteriorMAPConnected(
        tree, p_false_negative, p_false_positive, q
    ).fit(observed)
    median_decoder = PosteriorMedianUnconstrained().fit(result.node_marginals)
    connected_decoder = ConnectedBayesHamming(tree).fit(result.node_marginals)
    all_actions = _all_binary_actions(tree.number_of_nodes())
    connected_actions = np.asarray(
        [
            action
            for action in all_actions
            if action.any()
            and nx.is_connected(tree.subgraph(np.flatnonzero(action)))
        ]
    )
    map_mismatches = 0
    median_mismatches = 0
    connected_mismatches = 0
    max_action_risk_error = 0.0
    for row in range(len(result.node_marginals)):
        posterior = support_probabilities[row]
        map_prediction = map_decoder.prediction_[row]
        matching = np.equal(support_masks, map_prediction).all(axis=1)
        selected_probability = float(posterior[matching].max()) if matching.any() else 0.0
        if selected_probability < float(posterior.max()) - tolerance:
            map_mismatches += 1

        marginal = result.node_marginals[row : row + 1]
        all_risks = np.asarray(
            [posterior_hamming_risk(action[None, :], marginal)[0] for action in all_actions]
        )
        connected_risks = np.asarray(
            [posterior_hamming_risk(action[None, :], marginal)[0] for action in connected_actions]
        )
        median_risk = median_decoder.row_posterior_risk_[row]
        connected_risk = connected_decoder.row_posterior_risk_[row]
        median_mismatches += int(median_risk > float(all_risks.min()) + tolerance)
        connected_mismatches += int(
            connected_risk > float(connected_risks.min()) + tolerance
        )
        direct_risk = (
            posterior
            @ np.not_equal(
                support_masks, connected_decoder.prediction_[row]
            ).mean(axis=1)
        )
        max_action_risk_error = max(
            max_action_risk_error, abs(float(direct_risk) - connected_risk)
        )

    connected_outputs_valid = all(
        row.any() and nx.is_connected(tree.subgraph(np.flatnonzero(row)))
        for row in connected_decoder.prediction_
    )
    return {
        "topology": topology,
        "q": q,
        "noise": noise_name,
        "repetitions": repetitions,
        "seed": seed,
        "row_comparisons": len(result.node_marginals),
        "marginal_entry_comparisons": int(result.node_marginals.size),
        "max_marginal_absolute_error": float(marginal_errors.max()),
        "marginal_row_mismatches": int(
            np.any(marginal_errors > tolerance, axis=1).sum()
        ),
        "max_posterior_normalization_error": float(
            np.max(np.abs(support_probabilities.sum(axis=1) - 1.0))
        ),
        "max_root_invariance_error": root_error,
        "marginals_in_unit_interval": bool(
            np.all((result.node_marginals >= 0.0) & (result.node_marginals <= 1.0))
        ),
        "map_action_mismatches": map_mismatches,
        "median_action_mismatches": median_mismatches,
        "connected_action_mismatches": connected_mismatches,
        "max_action_risk_error": max_action_risk_error,
        "connected_outputs_valid": connected_outputs_valid,
        "mbr_tie_fraction": float(connected_decoder.row_ties_.mean()),
    }


def _run_validation(config: dict[str, Any]) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    cases = list(
        itertools.product(
            config["tree_topologies"],
            config["branch_probabilities"],
            config["noise_settings"],
            config["repetitions"],
            config["seeds"],
        )
    )
    # The two limiting priors are separate boundary audits.
    cases.extend(
        (topology, q, config["noise_settings"][1], 1, 0)
        for topology, q in itertools.product(config["tree_topologies"], [0.0, 1.0])
    )
    m = int(config["m"])
    rows = int(config["rows_per_case"])
    for index, (topology, q, noise, repetitions, seed) in enumerate(cases, start=1):
        topology_index = _topology_index(str(topology))
        tree = generate_tree(
            m, str(topology), _derived_seed(int(seed), 501, topology_index)
        )
        clean = generate_alpha_acyclic_hypergraph(
            rows,
            m,
            tree,
            float(q),
            seed=_derived_seed(int(seed), 502, topology_index, int(round(100 * float(q)))),
            simple_hypergraph=False,
        )["incidence"]
        draws = [
            corrupt_incidence(
                clean,
                float(noise["p_false_negative"]),
                float(noise["p_false_positive"]),
                _derived_seed(int(seed), 503, topology_index, repeat),
            )["corrupted_incidence"]
            for repeat in range(int(repetitions))
        ]
        observed = draws[0] if int(repetitions) == 1 else np.stack(draws)
        records.append(
            _validation_case(
                tree,
                observed,
                str(topology),
                float(q),
                str(noise["name"]),
                float(noise["p_false_negative"]),
                float(noise["p_false_positive"]),
                int(repetitions),
                int(seed),
                float(config["comparison_tolerance"]),
            )
        )
        if index % 50 == 0:
            LOGGER.info("Validation case %d/%d", index, len(cases))
    return pd.DataFrame.from_records(records)


def _median_structure_diagnostics(
    tree: nx.Graph, prediction: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    empty = np.equal(prediction.sum(axis=1), 0)
    connected = np.asarray(
        [
            bool(row.any() and nx.is_connected(tree.subgraph(np.flatnonzero(row))))
            for row in prediction
        ]
    )
    disconnected = ~empty & ~connected
    return empty, connected, disconnected


def _q_tracks(
    method: dict[str, Any],
    train_observed: np.ndarray,
    job: Job,
    q_bounds: tuple[float, float],
) -> list[dict[str, Any]]:
    tracks = [
        {
            "q_mode": "oracle_q",
            "q": job.q,
            "q_fit_split": "oracle",
            "q_runtime_seconds": 0.0,
            "q_evaluations": 0,
        }
    ]
    if method["estimator"] == "EstimatedQMarginalTree":
        tracks.append(
            {
                "q_mode": "estimated_q",
                "q": float(method["q"]),
                "q_fit_split": "frozen_A1_train_validation_selection",
                "q_runtime_seconds": 0.0,
                "q_evaluations": np.nan,
            }
        )
    else:
        start = time.perf_counter()
        estimate = estimate_q_mle(
            method["tree"],
            train_observed,
            job.p_false_negative,
            job.p_false_positive,
            bounds=q_bounds,
        )
        tracks.append(
            {
                "q_mode": "estimated_q",
                "q": estimate.q,
                "q_fit_split": "train_only",
                "q_runtime_seconds": time.perf_counter() - start,
                "q_evaluations": estimate.evaluations,
            }
        )
    return tracks


def _run_primary(
    config: dict[str, Any], jobs: list[Job]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    records: list[dict[str, Any]] = []
    risk_records: list[dict[str, Any]] = []
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
        test_clean, test_observed = splits["test"]
        for method in methods:
            tree = method["tree"]
            for track in _q_tracks(
                method, splits["train"][1], job, tuple(config["q_bounds"])
            ):
                q = float(track["q"])
                posterior_start = time.perf_counter()
                posterior = posterior_node_marginals(
                    tree,
                    test_observed,
                    job.p_false_negative,
                    job.p_false_positive,
                    q,
                )
                posterior_runtime = time.perf_counter() - posterior_start

                median = PosteriorMedianUnconstrained().fit(posterior.node_marginals)
                median_empty, median_connected, median_disconnected = (
                    _median_structure_diagnostics(tree, median.prediction_)
                )
                decoders = [
                    PosteriorMAPConnected(
                        tree,
                        job.p_false_negative,
                        job.p_false_positive,
                        q,
                    ),
                    median,
                    ConnectedBayesHamming(tree),
                ]
                likelihoods = _score_splits(tree, q, splits, job)
                for decoder in decoders:
                    start = time.perf_counter()
                    if isinstance(decoder, PosteriorMAPConnected):
                        decoder.fit(test_observed)
                    elif isinstance(decoder, ConnectedBayesHamming):
                        decoder.fit(posterior.node_marginals)
                    prediction = decoder.predict()
                    decoder_runtime = time.perf_counter() - start
                    row_risk = posterior_hamming_risk(
                        prediction, posterior.node_marginals
                    )
                    actual_row_risk = np.not_equal(prediction, test_clean).mean(axis=1)
                    metrics = recovery_metrics(
                        test_clean, prediction, tree, test_observed
                    )
                    base = {
                        "dataset_id": f"{job.topology}-seed-{job.seed:02d}",
                        "seed": job.seed,
                        "n": job.n,
                        "m": job.m,
                        "tree_topology": job.topology,
                        "true_q": job.q,
                        "used_q": q,
                        "q_absolute_error": abs(q - job.q),
                        "q_mode": track["q_mode"],
                        "q_fit_split": track["q_fit_split"],
                        "q_evaluations": track["q_evaluations"],
                        "p_false_positive": job.p_false_positive,
                        "p_false_negative": job.p_false_negative,
                        "tree_source": method["estimator"],
                        "decoder": decoder.name,
                    }
                    records.append(
                        {
                            **base,
                            "train_rows": len(splits["train"][0]),
                            "validation_rows": len(splits["validation"][0]),
                            "test_rows": len(test_clean),
                            "test_hamming_error": float(metrics["hamming_error"]),
                            "test_exact_row_recovery": float(metrics["exact_row_recovery"]),
                            "test_clean_f1": float(metrics["clean_f1"]),
                            "test_riv": int(metrics["running_intersection_violations"]),
                            "valid_clean_test_join_tree": running_intersection_violations(
                                test_clean, tree
                            )["num_violating_vertices"]
                            == 0,
                            "tree_edge_disagreement": tree_edge_disagreement(true_tree, tree),
                            "posterior_expected_hamming": float(row_risk.mean()),
                            "risk_calibration_gap": float(row_risk.mean() - actual_row_risk.mean()),
                            "risk_row_correlation": float(
                                np.corrcoef(row_risk, actual_row_risk)[0, 1]
                            ),
                            "median_connected_fraction": float(median_connected.mean()),
                            "median_empty_fraction": float(median_empty.mean()),
                            "median_disconnected_fraction": float(median_disconnected.mean()),
                            "decision_tie_fraction": float(decoder.row_ties_.mean()),
                            "tree_runtime_seconds": float(method["tree_runtime_seconds"]),
                            "q_runtime_seconds": float(track["q_runtime_seconds"]),
                            "posterior_runtime_seconds": posterior_runtime,
                            "decoder_runtime_seconds": decoder_runtime,
                            "total_inference_runtime_seconds": posterior_runtime + decoder_runtime,
                            **likelihoods,
                        }
                    )
                    for row_index, (predicted, actual, tied) in enumerate(
                        zip(row_risk, actual_row_risk, decoder.row_ties_)
                    ):
                        risk_records.append(
                            {
                                **base,
                                "test_row": row_index,
                                "posterior_risk": float(predicted),
                                "actual_hamming": float(actual),
                                "calibration_gap": float(predicted - actual),
                                "decision_tied": bool(tied),
                                "median_empty": bool(median_empty[row_index]),
                                "median_connected": bool(median_connected[row_index]),
                                "median_disconnected": bool(median_disconnected[row_index]),
                            }
                        )
    return pd.DataFrame.from_records(records), pd.DataFrame.from_records(risk_records)


def _run_scaling(config: dict[str, Any]) -> pd.DataFrame:
    records = []
    n = int(config["n"])
    seed = int(config["seed"])
    for m in config["m_values"]:
        m = int(m)
        tree = generate_tree(m, str(config["topology"]), _derived_seed(seed, 601, m))
        clean = generate_alpha_acyclic_hypergraph(
            n,
            m,
            tree,
            float(config["branch_probability"]),
            seed=_derived_seed(seed, 602, m),
            simple_hypergraph=False,
        )["incidence"]
        observed = corrupt_incidence(
            clean,
            float(config["p_false_negative"]),
            float(config["p_false_positive"]),
            _derived_seed(seed, 603, m),
        )["corrupted_incidence"]
        start = time.perf_counter()
        posterior_node_marginals(
            tree,
            observed,
            float(config["p_false_negative"]),
            float(config["p_false_positive"]),
            float(config["branch_probability"]),
        )
        elapsed = time.perf_counter() - start
        records.append(
            {
                "n": n,
                "m": m,
                "runtime_seconds": elapsed,
                "microseconds_per_nm": elapsed * 1e6 / (n * m),
            }
        )
    return pd.DataFrame.from_records(records)


def run(config_path: Path, max_runs: int | None = None) -> None:
    config = _load_config(config_path)
    experiment_type = str(config["experiment_type"])
    result_root = Path("results/a1_5")
    _configure_logging(result_root / "logs" / f"{experiment_type}.log")
    raw_directory = result_root / "raw"
    raw_directory.mkdir(parents=True, exist_ok=True)
    if experiment_type == "a1_5_validation":
        frame = _run_validation(config)
        frame.to_csv(raw_directory / "a1_5_validation_results.csv", index=False)
    elif experiment_type == "a1_5_scaling":
        frame = _run_scaling(config)
        frame.to_csv(raw_directory / "a1_5_scaling_results.csv", index=False)
    elif experiment_type == "a1_5_primary":
        jobs = _jobs(config)
        if max_runs is not None:
            jobs = jobs[:max_runs]
        frame, risk_rows = _run_primary(config, jobs)
        frame.to_csv(raw_directory / "a1_5_primary_results.csv", index=False)
        risk_rows.to_csv(raw_directory / "a1_5_risk_rows.csv", index=False)
    else:
        raise ValueError(f"unknown experiment_type: {experiment_type}")
    LOGGER.info("Completed %s with %d aggregate rows", experiment_type, len(frame))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--max-runs", type=int)
    args = parser.parse_args()
    run(args.config, args.max_runs)


if __name__ == "__main__":
    main()
