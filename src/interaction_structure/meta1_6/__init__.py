"""META1.6 fixed-row design for high-order signed-support recovery."""

from .ensemble import RecoveryScenario, make_support_ensemble
from .scoring import KKTScore, score_design
from .search import SearchResult, optimize_rows
from .structure import and_dictionary, partition_terms, structural_diagnostics

__all__ = [
    "KKTScore",
    "RecoveryScenario",
    "SearchResult",
    "and_dictionary",
    "make_support_ensemble",
    "optimize_rows",
    "partition_terms",
    "score_design",
    "structural_diagnostics",
]
