"""Deterministic observed-likelihood search over labeled trees."""

from __future__ import annotations

import time

import networkx as nx
import numpy as np

from ahsl.join_tree_estimators import NoiseCorrectedMWST
from ahsl.models.noise_likelihood import node_log_likelihoods
from ahsl.q_estimation import estimate_q_mle
from ahsl.subtree_marginal import (
    marginal_log_likelihood,
    marginal_log_likelihood_from_node_logs,
)
from ahsl.trees import validate_labeled_tree


def tree_edge_signature(tree: nx.Graph) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(tuple(sorted(edge)) for edge in tree.edges))


def single_edge_swap_neighbors(tree: nx.Graph) -> list[nx.Graph]:
    """Enumerate the complete deterministic one-edge-swap neighborhood."""
    validate_labeled_tree(tree)
    candidates: dict[tuple[tuple[int, int], ...], nx.Graph] = {}
    for removed in tree_edge_signature(tree):
        forest = tree.copy()
        forest.remove_edge(*removed)
        components = sorted(
            (sorted(component) for component in nx.connected_components(forest)),
            key=lambda nodes: nodes[0],
        )
        for left in components[0]:
            for right in components[1]:
                added = tuple(sorted((left, right)))
                if added == removed:
                    continue
                candidate = forest.copy()
                candidate.add_edge(*added)
                candidates[tree_edge_signature(candidate)] = candidate
    return [candidates[signature] for signature in sorted(candidates)]


def enumerate_labeled_trees(m: int):
    """Yield every labeled tree on ``range(m)`` in Prüfer-sequence order."""
    if m == 1:
        tree = nx.Graph()
        tree.add_node(0)
        yield tree
        return
    for sequence in np.ndindex(*(m for _ in range(m - 2))):
        yield nx.from_prufer_sequence(list(sequence))


class MarginalLikelihoodTreeSearch:
    """Full-neighborhood best-improvement search at a fixed branch probability."""

    name = "MarginalLikelihoodTreeSearch"

    def __init__(
        self,
        p_false_negative: float,
        p_false_positive: float,
        branch_probability: float,
        max_iterations: int = 10,
    ) -> None:
        self.p_false_negative = p_false_negative
        self.p_false_positive = p_false_positive
        self.branch_probability = branch_probability
        self.max_iterations = max_iterations

    def fit(
        self, observed: np.ndarray, initial_tree: nx.Graph | None = None
    ) -> "MarginalLikelihoodTreeSearch":
        observations = np.asarray(observed)
        if initial_tree is None:
            current_tree = NoiseCorrectedMWST(
                self.p_false_negative, self.p_false_positive
            ).fit(observations).predict_tree()
        else:
            current_tree = initial_tree.copy()
            if validate_labeled_tree(current_tree) != observations.shape[-1]:
                raise ValueError("initial tree size must match observed columns")

        start = time.perf_counter()
        log_zero, log_one, _ = node_log_likelihoods(
            observations, self.p_false_negative, self.p_false_positive
        )
        cache: dict[tuple[tuple[int, int], ...], float] = {}

        def cached_score(tree: nx.Graph) -> float:
            signature = tree_edge_signature(tree)
            if signature not in cache:
                cache[signature] = marginal_log_likelihood_from_node_logs(
                    tree, log_zero, log_one, self.branch_probability
                ).log_likelihood
            return cache[signature]

        current_score = cached_score(current_tree)
        self.initial_log_likelihood_ = current_score
        self.initial_tree_ = current_tree.copy()
        self.objective_history_ = [current_score]
        self.evaluated_candidates_ = 0
        self.neighborhood_sizes_ = []
        self.neighborhood_seconds_ = []
        improvements = 0
        converged = False

        for _ in range(self.max_iterations):
            neighborhood_start = time.perf_counter()
            candidates = single_edge_swap_neighbors(current_tree)
            best_score = current_score
            best_tree = current_tree
            best_signature = tree_edge_signature(current_tree)
            for candidate in candidates:
                score = cached_score(candidate)
                self.evaluated_candidates_ += 1
                signature = tree_edge_signature(candidate)
                if score > best_score + 1e-12 or (
                    np.isclose(score, best_score, rtol=1e-12, atol=1e-12)
                    and best_score > current_score + 1e-12
                    and signature < best_signature
                ):
                    best_score = score
                    best_tree = candidate
                    best_signature = signature
            self.neighborhood_sizes_.append(len(candidates))
            self.neighborhood_seconds_.append(time.perf_counter() - neighborhood_start)
            if best_score <= current_score + 1e-12:
                converged = True
                break
            current_tree = best_tree
            current_score = best_score
            self.objective_history_.append(current_score)
            improvements += 1

        self.tree_ = current_tree
        self.log_likelihood_ = current_score
        self.num_iterations_ = improvements
        self.converged_ = converged
        self.max_iteration_reached_ = not converged
        self.tree_changed_ = tree_edge_signature(current_tree) != tree_edge_signature(
            self.initial_tree_
        )
        self.runtime_seconds_ = time.perf_counter() - start
        return self

    def predict_tree(self) -> nx.Graph:
        return self.tree_.copy()


class EstimatedQMarginalTree:
    """Alternate exact tree search and train-only q MLE; select on validation."""

    name = "EstimatedQMarginalTree"

    def __init__(
        self,
        p_false_negative: float,
        p_false_positive: float,
        q_bounds: tuple[float, float] = (0.02, 0.98),
        max_outer_iterations: int = 3,
        max_tree_iterations: int = 10,
    ) -> None:
        self.p_false_negative = p_false_negative
        self.p_false_positive = p_false_positive
        self.q_bounds = q_bounds
        self.max_outer_iterations = max_outer_iterations
        self.max_tree_iterations = max_tree_iterations

    def fit(
        self, train_observed: np.ndarray, validation_observed: np.ndarray
    ) -> "EstimatedQMarginalTree":
        train = np.asarray(train_observed)
        validation = np.asarray(validation_observed)
        start = time.perf_counter()
        current_tree = NoiseCorrectedMWST(
            self.p_false_negative, self.p_false_positive
        ).fit(train).predict_tree()
        checkpoints: list[dict[str, object]] = []
        total_candidates = 0

        for outer_iteration in range(self.max_outer_iterations + 1):
            q_estimate = estimate_q_mle(
                current_tree,
                train,
                self.p_false_negative,
                self.p_false_positive,
                self.q_bounds,
            )
            validation_score = marginal_log_likelihood(
                current_tree,
                validation,
                self.p_false_negative,
                self.p_false_positive,
                q_estimate.q,
            ).log_likelihood
            checkpoints.append(
                {
                    "outer_iteration": outer_iteration,
                    "tree": current_tree.copy(),
                    "q": q_estimate.q,
                    "train_log_likelihood": q_estimate.log_likelihood,
                    "validation_log_likelihood": validation_score,
                    "q_evaluations": q_estimate.evaluations,
                }
            )
            if outer_iteration == self.max_outer_iterations:
                break
            search = MarginalLikelihoodTreeSearch(
                self.p_false_negative,
                self.p_false_positive,
                q_estimate.q,
                self.max_tree_iterations,
            ).fit(train, initial_tree=current_tree)
            total_candidates += search.evaluated_candidates_
            next_tree = search.predict_tree()
            if tree_edge_signature(next_tree) == tree_edge_signature(current_tree):
                break
            current_tree = next_tree

        best = max(
            checkpoints,
            key=lambda item: (
                float(item["validation_log_likelihood"]),
                -int(item["outer_iteration"]),
            ),
        )
        self.tree_ = best["tree"].copy()
        self.q_ = float(best["q"])
        self.train_log_likelihood_ = float(best["train_log_likelihood"])
        self.validation_log_likelihood_ = float(best["validation_log_likelihood"])
        self.selected_outer_iteration_ = int(best["outer_iteration"])
        self.checkpoints_ = checkpoints
        self.evaluated_candidates_ = total_candidates
        self.runtime_seconds_ = time.perf_counter() - start
        return self

    def predict_tree(self) -> nx.Graph:
        return self.tree_.copy()
