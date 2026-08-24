"""Run the bounded classical A0.75 join-tree kill-test."""

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
from ahsl.experiments.a0_75_analysis import write_analysis_outputs
from ahsl.join_tree_estimators import (
    AlternatingTreeIncidenceEstimator,
    BinaryMWST,
    BootstrapStabilityMWST,
    DataAgnosticRandomTree,
    NoiseCorrectedMWST,
    ProfileLikelihoodTreeSearch,
    TrueTreeOracle,
)
from ahsl.metrics import recovery_metrics
from ahsl.models import DPNoiseAwareConnectedMLE
from ahsl.synthetic import generate_alpha_acyclic_hypergraph
from ahsl.tree_perturbation import tree_edge_disagreement
from ahsl.trees import SUPPORTED_TOPOLOGIES, generate_tree


LOGGER = logging.getLogger("ahsl.a0_75")


@dataclass(frozen=True)
class Job:
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


def _derived_seed(base_seed: int, *coordinates: int) -> int:
    sequence = np.random.SeedSequence([base_seed, *coordinates])
    return int(sequence.generate_state(1, dtype=np.uint32)[0])


def _topology_index(topology: str) -> int:
    return SUPPORTED_TOPOLOGIES.index(topology)


def _load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _jobs(config: dict[str, Any]) -> list[Job]:
    product = itertools.product(
        config["n_values"],
        config["m_values"],
        config["tree_topologies"],
        config["branch_probabilities"],
        config["noise_settings"],
        config["observation_repetitions"],
        config["seeds"],
    )
    return [
        Job(
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
        for index, (n, m, topology, branch, noise, repetitions, seed) in enumerate(product)
    ]


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
        job.branch_probability,
        seed=_derived_seed(
            job.seed,
            21,
            job.n,
            job.m,
            topology_index,
            int(round(1000 * job.branch_probability)),
        ),
        simple_hypergraph=True,
    )["incidence"]
    observations = []
    for repetition in range(job.repetitions):
        observations.append(
            corrupt_incidence(
                clean,
                job.p_false_negative,
                job.p_false_positive,
                _derived_seed(
                    job.seed,
                    31,
                    job.n,
                    job.m,
                    topology_index,
                    int(round(1000 * job.branch_probability)),
                    int(round(1000 * job.p_false_positive)),
                    int(round(1000 * job.p_false_negative)),
                    0,
                    repetition,
                ),
            )["corrupted_incidence"]
        )
    stacked = np.stack(observations)
    observed = stacked[0] if job.repetitions == 1 else stacked
    return tree, clean, observed


def _metadata(job: Job) -> dict[str, Any]:
    return {
        "experiment_type": f"a0_75_{'primary' if job.repetitions == 1 else 'r3'}",
        "dataset_id": f"{job.topology}-seed-{job.seed:02d}-R{job.repetitions}",
        "seed": job.seed,
        "n": job.n,
        "m": job.m,
        "tree_topology": job.topology,
        "branch_probability": job.branch_probability,
        "noise_setting": job.noise_name,
        "p_false_positive": job.p_false_positive,
        "p_false_negative": job.p_false_negative,
        "num_observations": job.repetitions,
        "simple_hypergraph": True,
    }


def _record(
    estimator: str,
    tree: nx.Graph,
    prediction: np.ndarray,
    clean: np.ndarray,
    observed: np.ndarray,
    true_tree: nx.Graph,
    job: Job,
    tree_runtime: float,
    downstream_runtime: float,
    total_runtime: float,
    **diagnostics: Any,
) -> dict[str, Any]:
    metrics = recovery_metrics(clean, prediction, tree, observed)
    clean_riv = int(
        running_intersection_violations(clean, tree)["num_violating_vertices"]
    )
    return {
        **_metadata(job),
        "estimator": estimator,
        "clean_hamming_error": float(metrics["hamming_error"]),
        "exact_row_recovery": float(metrics["exact_row_recovery"]),
        "clean_f1": float(metrics["clean_f1"]),
        "clean_riv_on_estimated_tree": clean_riv,
        "valid_clean_join_tree": clean_riv == 0,
        "estimated_incidence_riv": int(metrics["running_intersection_violations"]),
        "tree_edge_disagreement": tree_edge_disagreement(true_tree, tree),
        "runtime_seconds": total_runtime,
        "tree_estimation_runtime": tree_runtime,
        "downstream_dp_runtime": downstream_runtime,
        "random_tree_replicate": diagnostics.pop("random_tree_replicate", -1),
        "random_control_role": diagnostics.pop("random_control_role", "not_random"),
        "binary_source": diagnostics.pop("binary_source", "not_binary"),
        "binary_incidence_identical": diagnostics.pop(
            "binary_incidence_identical", np.nan
        ),
        "binary_tree_identical": diagnostics.pop("binary_tree_identical", np.nan),
        "num_iterations": diagnostics.pop("num_iterations", np.nan),
        "converged": diagnostics.pop("converged", np.nan),
        "tree_changed": diagnostics.pop("tree_changed", np.nan),
        "max_iteration_reached": diagnostics.pop(
            "max_iteration_reached", np.nan
        ),
        **diagnostics,
    }


def _tie_diagnostics(
    prediction: np.ndarray,
    row_ties: np.ndarray,
    clean: np.ndarray,
    oracle_prediction: np.ndarray,
    oracle_row_ties: np.ndarray,
) -> dict[str, float]:
    unique = ~(np.asarray(row_ties) | np.asarray(oracle_row_ties))
    estimator_row_error = np.not_equal(clean, prediction).mean(axis=1)
    oracle_row_error = np.not_equal(clean, oracle_prediction).mean(axis=1)
    return {
        "downstream_optimal_tie_fraction": float(np.mean(row_ties)),
        "unique_both_row_fraction": float(unique.mean()),
        "unique_both_estimator_hamming": float(estimator_row_error[unique].mean()),
        "unique_both_oracle_hamming": float(oracle_row_error[unique].mean()),
        "unique_both_hamming_excess": float(
            (estimator_row_error[unique] - oracle_row_error[unique]).mean()
        ),
    }


def _estimate_then_decode(
    estimator: Any,
    clean: np.ndarray,
    observed: np.ndarray,
    true_tree: nx.Graph,
    job: Job,
    oracle_prediction: np.ndarray,
    oracle_row_ties: np.ndarray,
    **diagnostics: Any,
) -> dict[str, Any]:
    total_start = time.perf_counter()
    tree_start = time.perf_counter()
    tree = estimator.fit(observed).predict_tree()
    tree_runtime = time.perf_counter() - tree_start
    dp_start = time.perf_counter()
    downstream_model = DPNoiseAwareConnectedMLE(
        tree, job.p_false_negative, job.p_false_positive
    ).fit(observed)
    prediction = downstream_model.predict()
    downstream_runtime = time.perf_counter() - dp_start
    diagnostics.update(
        _tie_diagnostics(
            prediction,
            downstream_model.row_ties_,
            clean,
            oracle_prediction,
            oracle_row_ties,
        )
    )
    return _record(
        estimator.name,
        tree,
        prediction,
        clean,
        observed,
        true_tree,
        job,
        tree_runtime,
        downstream_runtime,
        time.perf_counter() - total_start,
        **diagnostics,
    )


def _run_job(job: Job, config: dict[str, Any]) -> list[dict[str, Any]]:
    true_tree, clean, observed = _tree_and_data(job)
    oracle_model = DPNoiseAwareConnectedMLE(
        true_tree, job.p_false_negative, job.p_false_positive
    ).fit(observed)
    tie_reference = {
        "oracle_prediction": oracle_model.predict(),
        "oracle_row_ties": oracle_model.row_ties_,
    }
    rows = [
        _estimate_then_decode(
            TrueTreeOracle(true_tree),
            clean,
            observed,
            true_tree,
            job,
            **tie_reference,
        )
    ]
    for replicate in range(int(config["random_tree_replicates"])):
        random_seed = _derived_seed(
            job.seed, 41, job.m, _topology_index(job.topology), replicate
        )
        rows.append(
            _estimate_then_decode(
                DataAgnosticRandomTree(job.m, random_seed),
                clean,
                observed,
                true_tree,
                job,
                **tie_reference,
                random_tree_replicate=replicate,
                random_control_role="primary" if replicate == 0 else "diagnostic",
            )
        )

    binary = BinaryMWST(
        job.p_false_negative, job.p_false_positive, "observed"
    )
    independent_binary = BinaryMWST(
        job.p_false_negative, job.p_false_positive, "independent_mle"
    ).fit(observed)
    binary.fit(observed)
    binary_incidence_identical = np.array_equal(
        binary.binary_incidence_, independent_binary.binary_incidence_
    )
    binary_tree_identical = sorted(binary.predict_tree().edges()) == sorted(
        independent_binary.predict_tree().edges()
    )
    rows.append(
        _estimate_then_decode(
            BinaryMWST(job.p_false_negative, job.p_false_positive, "observed"),
            clean,
            observed,
            true_tree,
            job,
            **tie_reference,
            binary_source="observed",
            binary_incidence_identical=binary_incidence_identical,
            binary_tree_identical=binary_tree_identical,
        )
    )
    rows.append(
        _estimate_then_decode(
            NoiseCorrectedMWST(job.p_false_negative, job.p_false_positive),
            clean,
            observed,
            true_tree,
            job,
            **tie_reference,
        )
    )
    rows.append(
        _estimate_then_decode(
            BootstrapStabilityMWST(
                job.p_false_negative,
                job.p_false_positive,
                int(config["bootstrap_replicates"]),
                _derived_seed(job.seed, 51, _topology_index(job.topology)),
            ),
            clean,
            observed,
            true_tree,
            job,
            **tie_reference,
            bootstrap_replicates=int(config["bootstrap_replicates"]),
        )
    )

    alternating = AlternatingTreeIncidenceEstimator(
        job.p_false_negative,
        job.p_false_positive,
        int(config["alternating_max_iterations"]),
    )
    total_start = time.perf_counter()
    alternating.fit(observed)
    tie_diagnostics = _tie_diagnostics(
        alternating.predict(),
        alternating.row_ties_,
        clean,
        tie_reference["oracle_prediction"],
        tie_reference["oracle_row_ties"],
    )
    rows.append(
        _record(
            alternating.name,
            alternating.predict_tree(),
            alternating.predict(),
            clean,
            observed,
            true_tree,
            job,
            alternating.tree_estimation_runtime_,
            alternating.downstream_dp_runtime_,
            time.perf_counter() - total_start,
            num_iterations=alternating.num_iterations_,
            converged=alternating.converged_,
            tree_changed=alternating.tree_changed_,
            max_iteration_reached=alternating.max_iteration_reached_,
            **tie_diagnostics,
        )
    )
    return rows


def _run_profile_job(job: Job, config: dict[str, Any]) -> dict[str, Any]:
    true_tree, clean, observed = _tree_and_data(job)
    oracle_model = DPNoiseAwareConnectedMLE(
        true_tree, job.p_false_negative, job.p_false_positive
    ).fit(observed)
    estimator = ProfileLikelihoodTreeSearch(
        job.p_false_negative,
        job.p_false_positive,
        int(config["profile_max_iterations"]),
        int(config["profile_max_candidates_per_iteration"]),
    )
    total_start = time.perf_counter()
    estimator.fit(observed)
    tie_diagnostics = _tie_diagnostics(
        estimator.predict(),
        estimator.row_ties_,
        clean,
        oracle_model.predict(),
        oracle_model.row_ties_,
    )
    return _record(
        estimator.name,
        estimator.predict_tree(),
        estimator.predict(),
        clean,
        observed,
        true_tree,
        job,
        estimator.tree_estimation_runtime_,
        estimator.downstream_dp_runtime_,
        time.perf_counter() - total_start,
        num_iterations=estimator.num_iterations_,
        converged=estimator.converged_,
        tree_changed=estimator.tree_changed_,
        max_iteration_reached=estimator.max_iteration_reached_,
        evaluated_profile_candidates=estimator.evaluated_candidates_,
        initial_profile_objective=estimator.initial_profile_objective_,
        final_profile_objective=estimator.profile_objective_,
        profile_candidates_per_iteration=int(
            config["profile_max_candidates_per_iteration"]
        ),
        **tie_diagnostics,
    )


def run(config: dict[str, Any], max_runs: int | None = None) -> pd.DataFrame:
    repository_root = Path(__file__).resolve().parents[3]
    result_root = repository_root / "results/a0_75"
    experiment_type = str(config["experiment_type"])
    _configure_logging(result_root / f"logs/{experiment_type}.log")
    jobs = _jobs(config)
    if max_runs is not None:
        jobs = jobs[:max_runs]
    is_profile = experiment_type == "a0_75_profile_search"
    evaluations = 1 if is_profile else 5 + int(config["random_tree_replicates"])
    LOGGER.info("A0.75 plan: %s", experiment_type)
    LOGGER.info("  dataset cases: %d", len(jobs))
    LOGGER.info("  estimator evaluations: %d", len(jobs) * evaluations)
    if is_profile:
        LOGGER.info(
            "  exact profile candidates per iteration: %d",
            config["profile_max_candidates_per_iteration"],
        )
    else:
        LOGGER.info("  bootstrap replicates per dataset: %d", config["bootstrap_replicates"])
    LOGGER.info("  neural models: 0")
    start = time.perf_counter()
    records: list[dict[str, Any]] = []
    for completed, job in enumerate(jobs, start=1):
        if is_profile:
            records.append(_run_profile_job(job, config))
        else:
            records.extend(_run_job(job, config))
        if completed == 1 or completed % 10 == 0 or completed == len(jobs):
            LOGGER.info("Completed %d/%d datasets", completed, len(jobs))
    raw = pd.DataFrame.from_records(records)
    raw_directory = result_root / "raw"
    raw_directory.mkdir(parents=True, exist_ok=True)
    raw.to_csv(raw_directory / f"{experiment_type}_results.csv", index=False)
    analysis_raw = raw
    analysis_prefix = experiment_type
    if is_profile:
        primary_path = raw_directory / "a0_75_primary_results.csv"
        primary = pd.read_csv(primary_path)
        analysis_raw = pd.concat([primary, raw], ignore_index=True)
        analysis_prefix = "a0_75_primary_with_profile"
        analysis_raw.to_csv(
            raw_directory / "a0_75_primary_with_profile_results.csv", index=False
        )
    gate = write_analysis_outputs(
        analysis_raw, result_root / "aggregated", analysis_prefix
    )
    LOGGER.info("Raw rows: %d", len(raw))
    LOGGER.info("Best classical excess: %.6f", gate.iloc[0]["best_classical_excess"])
    if is_profile:
        LOGGER.info(
            "Profile-likelihood kill-test completed; final decision is %s.",
            gate.iloc[0]["final_decision_code"],
        )
    elif bool(gate.iloc[0]["profile_search_was_triggered"]):
        LOGGER.info("Profile-likelihood kill-test is justified.")
    else:
        LOGGER.info("Profile search is not triggered.")
    LOGGER.info("Finished in %.2f seconds", time.perf_counter() - start)
    return raw


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--max-runs", type=int, default=None)
    arguments = parser.parse_args()
    run(_load_config(arguments.config), arguments.max_runs)


if __name__ == "__main__":
    main()
