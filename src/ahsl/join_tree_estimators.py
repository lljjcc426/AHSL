"""Classical join-tree estimators for the Phase A0.75 kill-test."""

from __future__ import annotations

import time

import networkx as nx
import numpy as np

from ahsl.join_tree_recovery import (
    IntersectionMWSTJoinTree,
    deterministic_maximum_spanning_tree,
)
from ahsl.models import DPNoiseAwareConnectedMLE, NoiseAwareIndependentMLE
from ahsl.trees import generate_tree, validate_labeled_tree


def _edge_set(tree: nx.Graph) -> frozenset[tuple[int, int]]:
    return frozenset(tuple(sorted(edge)) for edge in tree.edges)


def noise_corrected_intersection_weights(
    observed: np.ndarray,
    p_false_negative: float,
    p_false_positive: float,
    delta_threshold: float = 1e-12,
) -> np.ndarray:
    """Estimate off-diagonal clean intersections without clipping."""
    observations = np.asarray(observed, dtype=float)
    if observations.ndim == 2:
        mean_observation = observations
    elif observations.ndim == 3:
        mean_observation = observations.mean(axis=0)
    else:
        raise ValueError("observed must have shape (n,m) or (R,n,m)")
    delta = 1.0 - p_false_negative - p_false_positive
    if abs(delta) < delta_threshold:
        raise ValueError("noise-corrected intersections are undefined when delta is zero")
    corrected = (mean_observation - p_false_positive) / delta
    weights = corrected.T @ corrected
    np.fill_diagonal(weights, 0.0)
    return weights


class BinaryMWST:
    """Intersection MWST from a hard binary incidence estimate."""

    name = "BinaryMWST"

    def __init__(
        self,
        p_false_negative: float,
        p_false_positive: float,
        binary_source: str = "observed",
    ) -> None:
        if binary_source not in {"observed", "independent_mle"}:
            raise ValueError("binary_source must be observed or independent_mle")
        self.p_false_negative = p_false_negative
        self.p_false_positive = p_false_positive
        self.binary_source = binary_source

    def fit(self, observed: np.ndarray) -> "BinaryMWST":
        observations = np.asarray(observed)
        if self.binary_source == "independent_mle":
            binary = NoiseAwareIndependentMLE(
                self.p_false_negative, self.p_false_positive
            ).fit(observations).predict()
        elif observations.ndim == 2:
            binary = observations.astype(np.int8)
        else:
            binary = (observations.mean(axis=0) >= 0.5).astype(np.int8)
        fitted = IntersectionMWSTJoinTree().fit(binary)
        self.binary_incidence_ = binary
        self.tree_ = fitted.predict_tree()
        self.intersection_weights_ = fitted.intersection_weights_
        return self

    def predict_tree(self) -> nx.Graph:
        return self.tree_.copy()


class NoiseCorrectedMWST:
    """MWST from unbiased off-diagonal intersection-weight estimates."""

    name = "NoiseCorrectedMWST"

    def __init__(
        self,
        p_false_negative: float,
        p_false_positive: float,
    ) -> None:
        self.p_false_negative = p_false_negative
        self.p_false_positive = p_false_positive

    def fit(self, observed: np.ndarray) -> "NoiseCorrectedMWST":
        self.intersection_weights_ = noise_corrected_intersection_weights(
            observed,
            self.p_false_negative,
            self.p_false_positive,
        )
        self.tree_ = deterministic_maximum_spanning_tree(self.intersection_weights_)
        return self

    def predict_tree(self) -> nx.Graph:
        return self.tree_.copy()


class BootstrapStabilityMWST:
    """MWST whose weights are bootstrap edge-selection frequencies."""

    name = "BootstrapStabilityMWST"

    def __init__(
        self,
        p_false_negative: float,
        p_false_positive: float,
        num_bootstrap_replicates: int = 100,
        seed: int = 0,
    ) -> None:
        if num_bootstrap_replicates < 1:
            raise ValueError("num_bootstrap_replicates must be positive")
        self.p_false_negative = p_false_negative
        self.p_false_positive = p_false_positive
        self.num_bootstrap_replicates = num_bootstrap_replicates
        self.seed = seed

    def fit(self, observed: np.ndarray) -> "BootstrapStabilityMWST":
        observations = np.asarray(observed)
        if observations.ndim == 2:
            n, m = observations.shape
        elif observations.ndim == 3:
            _, n, m = observations.shape
        else:
            raise ValueError("observed must have shape (n,m) or (R,n,m)")
        rng = np.random.default_rng(self.seed)
        edge_counts = np.zeros((m, m), dtype=float)
        for _ in range(self.num_bootstrap_replicates):
            indices = rng.integers(0, n, size=n)
            sample = observations[indices] if observations.ndim == 2 else observations[:, indices]
            tree = NoiseCorrectedMWST(
                self.p_false_negative, self.p_false_positive
            ).fit(sample).predict_tree()
            for left, right in tree.edges:
                edge_counts[left, right] += 1.0
                edge_counts[right, left] += 1.0
        self.edge_frequencies_ = edge_counts / self.num_bootstrap_replicates
        self.tree_ = deterministic_maximum_spanning_tree(self.edge_frequencies_)
        return self

    def predict_tree(self) -> nx.Graph:
        return self.tree_.copy()


class DataAgnosticRandomTree:
    """A preregistered labeled random tree independent of observations."""

    name = "DataAgnosticRandomTree"

    def __init__(self, m: int, seed: int) -> None:
        self.m = m
        self.seed = seed

    def fit(self, observed: np.ndarray) -> "DataAgnosticRandomTree":
        self.tree_ = generate_tree(self.m, "random", self.seed)
        return self

    def predict_tree(self) -> nx.Graph:
        return self.tree_.copy()


class TrueTreeOracle:
    """Evaluation-only oracle that returns the generating join tree."""

    name = "TrueTreeOracle"

    def __init__(self, tree: nx.Graph) -> None:
        validate_labeled_tree(tree)
        self.tree = tree.copy()

    def fit(self, observed: np.ndarray) -> "TrueTreeOracle":
        self.tree_ = self.tree.copy()
        return self

    def predict_tree(self) -> nx.Graph:
        return self.tree_.copy()


class AlternatingTreeIncidenceEstimator:
    """Alternate exact incidence decoding with deterministic MWST recovery."""

    name = "AlternatingTreeIncidenceEstimator"

    def __init__(
        self,
        p_false_negative: float,
        p_false_positive: float,
        max_iterations: int = 10,
    ) -> None:
        if max_iterations < 1:
            raise ValueError("max_iterations must be positive")
        self.p_false_negative = p_false_negative
        self.p_false_positive = p_false_positive
        self.max_iterations = max_iterations

    def _decode(self, tree: nx.Graph, observed: np.ndarray) -> np.ndarray:
        start = time.perf_counter()
        prediction = DPNoiseAwareConnectedMLE(
            tree, self.p_false_negative, self.p_false_positive
        ).fit(observed).predict()
        self.downstream_dp_runtime_ += time.perf_counter() - start
        self.decoded_trees_.append(tree.copy())
        self.decoded_incidences_.append(prediction.copy())
        return prediction

    def fit(self, observed: np.ndarray) -> "AlternatingTreeIncidenceEstimator":
        self.tree_estimation_runtime_ = 0.0
        self.downstream_dp_runtime_ = 0.0
        self.decoded_trees_: list[nx.Graph] = []
        self.decoded_incidences_: list[np.ndarray] = []

        start = time.perf_counter()
        current_tree = NoiseCorrectedMWST(
            self.p_false_negative, self.p_false_positive
        ).fit(observed).predict_tree()
        self.tree_estimation_runtime_ += time.perf_counter() - start
        self.initial_tree_ = current_tree.copy()
        changes = 0
        converged = False

        for _ in range(self.max_iterations):
            prediction = self._decode(current_tree, observed)
            start = time.perf_counter()
            next_tree = IntersectionMWSTJoinTree().fit(prediction).predict_tree()
            self.tree_estimation_runtime_ += time.perf_counter() - start
            if _edge_set(next_tree) == _edge_set(current_tree):
                converged = True
                break
            current_tree = next_tree
            changes += 1

        if not converged:
            prediction = self._decode(current_tree, observed)

        self.tree_ = current_tree
        self.prediction_ = prediction
        self.num_iterations_ = changes
        self.converged_ = converged
        self.max_iteration_reached_ = not converged
        self.tree_changed_ = changes > 0
        return self

    def predict_tree(self) -> nx.Graph:
        return self.tree_.copy()

    def predict(self) -> np.ndarray:
        return self.prediction_.copy()


class ProfileLikelihoodTreeSearch:
    """Deterministic best-improvement tree search using exact profile likelihood."""

    name = "ProfileLikelihoodTreeSearch"

    def __init__(
        self,
        p_false_negative: float,
        p_false_positive: float,
        max_iterations: int = 10,
        max_candidates_per_iteration: int = 24,
    ) -> None:
        self.p_false_negative = p_false_negative
        self.p_false_positive = p_false_positive
        self.max_iterations = max_iterations
        self.max_candidates_per_iteration = max_candidates_per_iteration

    def _candidate_trees(
        self,
        tree: nx.Graph,
        proxy_weights: np.ndarray,
    ) -> list[nx.Graph]:
        candidates: list[tuple[float, tuple[tuple[int, int], ...], nx.Graph]] = []
        for removed in sorted(_edge_set(tree)):
            cut_tree = tree.copy()
            cut_tree.remove_edge(*removed)
            components = sorted(
                (sorted(component) for component in nx.connected_components(cut_tree)),
                key=lambda nodes: nodes[0],
            )
            for left in components[0]:
                for right in components[1]:
                    added = tuple(sorted((left, right)))
                    if added == removed:
                        continue
                    candidate = cut_tree.copy()
                    candidate.add_edge(*added)
                    edges = tuple(sorted(_edge_set(candidate)))
                    proxy_score = float(
                        sum(proxy_weights[u, v] for u, v in edges)
                    )
                    candidates.append((proxy_score, edges, candidate))
        candidates.sort(key=lambda item: (-item[0], item[1]))
        return [
            candidate
            for _, _, candidate in candidates[: self.max_candidates_per_iteration]
        ]

    def _profile_score(
        self,
        tree: nx.Graph,
        observed: np.ndarray,
    ) -> tuple[float, np.ndarray]:
        model = DPNoiseAwareConnectedMLE(
            tree, self.p_false_negative, self.p_false_positive
        ).fit(observed)
        return float(model.row_objectives_.sum()), model.predict()

    def fit(self, observed: np.ndarray) -> "ProfileLikelihoodTreeSearch":
        observations = np.asarray(observed)
        m = observations.shape[-1]
        if m > 16:
            raise ValueError("profile-likelihood tree search is limited to m <= 16")
        start = time.perf_counter()
        initializer = NoiseCorrectedMWST(
            self.p_false_negative, self.p_false_positive
        ).fit(observations)
        current_tree = initializer.predict_tree()
        proxy_weights = initializer.intersection_weights_
        current_score, current_prediction = self._profile_score(
            current_tree, observations
        )
        self.initial_profile_objective_ = current_score
        self.initial_tree_ = current_tree.copy()
        self.evaluated_candidates_ = 0
        improvements = 0
        converged = False

        for _ in range(self.max_iterations):
            best_score = current_score
            best_tree = current_tree
            best_prediction = current_prediction
            best_edges = tuple(sorted(_edge_set(current_tree)))
            for candidate in self._candidate_trees(current_tree, proxy_weights):
                score, prediction = self._profile_score(candidate, observations)
                self.evaluated_candidates_ += 1
                edges = tuple(sorted(_edge_set(candidate)))
                if score > best_score + 1e-12 or (
                    np.isclose(score, best_score, rtol=1e-12, atol=1e-12)
                    and best_score > current_score + 1e-12
                    and edges < best_edges
                ):
                    best_score = score
                    best_tree = candidate
                    best_prediction = prediction
                    best_edges = edges
            if best_score <= current_score + 1e-12:
                converged = True
                break
            current_tree = best_tree
            current_score = best_score
            current_prediction = best_prediction
            improvements += 1

        self.tree_estimation_runtime_ = time.perf_counter() - start
        downstream_start = time.perf_counter()
        final_model = DPNoiseAwareConnectedMLE(
            current_tree, self.p_false_negative, self.p_false_positive
        ).fit(observations)
        self.downstream_dp_runtime_ = time.perf_counter() - downstream_start
        self.tree_ = current_tree
        self.prediction_ = final_model.predict()
        self.profile_objective_ = current_score
        self.num_iterations_ = improvements
        self.converged_ = converged
        self.max_iteration_reached_ = not converged
        self.tree_changed_ = improvements > 0
        return self

    def predict_tree(self) -> nx.Graph:
        return self.tree_.copy()

    def predict(self) -> np.ndarray:
        return self.prediction_.copy()
