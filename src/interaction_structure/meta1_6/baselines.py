from __future__ import annotations

from .ensemble import RecoveryScenario
from .scoring import dcd_score, score_design


def hils_score(masks: tuple[int, ...], scenarios: list[RecoveryScenario], *, dimension: int = 6, draws: int = 32) -> float:
    """Faithful HILS-style average full signed-model selection probability."""
    return score_design(
        masks,
        scenarios,
        dimension=dimension,
        target_only=False,
        aggregator="mean",
        draws=draws,
        integrate_singular=True,
    ).score


def dcd_baseline_score(masks: tuple[int, ...], scenarios: list[RecoveryScenario], *, dimension: int = 6) -> float:
    """Support-averaged determinant/condition/irrepresentability criterion."""
    return dcd_score(masks, scenarios, dimension=dimension)
