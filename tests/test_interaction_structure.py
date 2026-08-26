from __future__ import annotations

import numpy as np
import pandas as pd

from interaction_structure.audits import heredity_classification
from interaction_structure.baselines.sparse_regression import fit_lasso_grid
from interaction_structure.datasets.drug import _is_supported_label, _split_agent
from interaction_structure.datasets.microbiome import decode_system
from interaction_structure.estimands.mobius import (
    interaction_dictionary,
    inverse_mobius,
    mobius_transform,
    powerset,
)
from interaction_structure.splits import gene_disjoint_split, overlap_audit, query_pair_disjoint_split
from interaction_structure.uncertainty import SupportLabel, label_from_interval


def test_mobius_exact_recovery_and_inverse_consistency() -> None:
    universe = ("a", "b", "c")
    beta = {subset: 0.0 for subset in powerset(universe)}
    beta[frozenset()] = 1.0
    beta[frozenset({"a"})] = 2.0
    beta[frozenset({"a", "b", "c"})] = -3.0
    values = inverse_mobius(beta, universe)
    recovered = mobius_transform(values, universe)
    assert recovered == beta


def test_additive_function_has_zero_higher_order_coefficients() -> None:
    universe = (0, 1, 2, 3)
    values = {subset: 5.0 + sum(item + 1 for item in subset) for subset in powerset(universe)}
    beta = mobius_transform(values, universe)
    assert all(abs(value) < 1e-12 for subset, value in beta.items() if len(subset) >= 2)


def test_pure_third_order_case() -> None:
    universe = (0, 1, 2)
    values = {subset: float(len(subset) == 3) for subset in powerset(universe)}
    beta = mobius_transform(values, universe)
    assert beta[frozenset(universe)] == 1.0
    assert all(beta[s] == 0.0 for s in powerset(universe) if len(s) < 3)


def test_response_scale_changes_coefficients() -> None:
    universe = (0, 1, 2)
    raw = {subset: float(np.exp(0.2 * len(subset) + (0.5 if len(subset) == 3 else 0))) for subset in powerset(universe)}
    raw_beta = mobius_transform(raw, universe)
    log_beta = mobius_transform({key: np.log(value) for key, value in raw.items()}, universe)
    assert not np.isclose(raw_beta[frozenset(universe)], log_beta[frozenset(universe)])


def test_support_label_thresholding_preserves_uncertainty() -> None:
    assert label_from_interval(0.2, 0.4, minimum_magnitude=0.1) == SupportLabel.STRONG_POSITIVE
    assert label_from_interval(-0.5, -0.2, minimum_magnitude=0.1) == SupportLabel.STRONG_NEGATIVE
    assert label_from_interval(-0.2, 0.3) == SupportLabel.UNCERTAIN_OR_NULL
    assert SupportLabel.UNKNOWN != SupportLabel.UNCERTAIN_OR_NULL


def _triples() -> pd.DataFrame:
    rows = [
        ("a", "b", "c", ("a", "b"), False),
        ("a", "b", "d", ("a", "b"), True),
        ("e", "f", "g", ("e", "f"), False),
        ("h", "i", "j", ("h", "i"), True),
    ]
    frame = pd.DataFrame(rows, columns=["gene_1", "gene_2", "gene_3", "query_pair", "strong_negative_tau"])
    return frame


def test_gene_disjoint_split_and_pair_overlap_accounting() -> None:
    frame = _triples()
    train, test, held = gene_disjoint_split(frame, test_fraction=0.3, seed=2)
    train_genes = set(frame.iloc[train][["gene_1", "gene_2", "gene_3"]].to_numpy().ravel())
    assert train_genes.isdisjoint(held)
    audit = overlap_audit(frame, train, test)
    assert 0.0 <= audit["test_with_any_pair_overlap"] <= 1.0


def test_query_background_split_has_no_query_pair_overlap() -> None:
    frame = _triples()
    train, test = query_pair_disjoint_split(frame, test_fraction=0.5, seed=3)
    assert set(frame.iloc[train]["query_pair"]).isdisjoint(frame.iloc[test]["query_pair"])


def test_drug_identity_is_separate_from_dose_context() -> None:
    assert _split_agent("AMP3") == ("AMP", 3)
    assert tuple(sorted([_split_agent("AMP2"), _split_agent("CPR1")])) == (("AMP", 2), ("CPR", 1))
    labels = pd.Series(["Synergy", "Additive", "Inconclusive"])
    assert _is_supported_label(labels).tolist() == [True, False, False]


def test_full_seven_species_index_has_127_nonempty_subsets() -> None:
    assert len([subset for subset in powerset(range(7)) if subset]) == 127
    assert decode_system("s1234567") == frozenset({"DW039", "DW067", "DW100", "DW102", "DW145", "DW147", "DW155"})


def test_heredity_classification() -> None:
    triple = frozenset({"a", "b", "c"})
    all_parents = {frozenset(pair) for pair in [("a", "b"), ("a", "c"), ("b", "c")]}
    assert heredity_classification(triple, all_parents) == "STRONG_HEREDITY"
    assert heredity_classification(triple, {frozenset({"a", "b"})}) == "WEAK_ONLY"
    assert heredity_classification(triple, set()) == "PURE_NON_HEREDITARY"


def test_dictionary_and_classical_fit_are_deterministic() -> None:
    universe = (0, 1, 2)
    rows = powerset(universe)
    design, terms = interaction_dictionary(rows, universe)
    truth = np.zeros(len(terms))
    truth[terms.index(frozenset())] = 0.5
    truth[terms.index(frozenset({0, 1, 2}))] = 2.0
    response = design @ truth
    first = fit_lasso_grid(design[:6], response[:6], design[6:], response[6:], alphas=(1e-4,), seed=4)
    second = fit_lasso_grid(design[:6], response[:6], design[6:], response[6:], alphas=(1e-4,), seed=4)
    np.testing.assert_allclose(first.coefficients, second.coefficients)
