"""
TOSP Candidate Selector – applies the six-layer filter and selects the top N candidates.
"""

from typing import Any

from ..models import AssetProfile, Candidate
from ..scoring.ranking import rank_candidates
from .eligibility import apply_tosp_filters


def select_candidates(
    profiles: list[AssetProfile], config: dict[str, Any]
) -> list[Candidate]:
    """
    Apply TOSP filters, rank candidates, and select the top N.

    Returns:
        List of Candidate objects.
    """
    candidates = []

    for profile in profiles:
        # Apply TOSP filters
        passed_filters = apply_tosp_filters(profile, config)
        # For top-N selection, we require at least the first three filters (regime, direction, opportunity)
        # The admission controller is optional for ranking, but we include it.
        if len(passed_filters) < 3:
            continue

        # Create candidate
        candidate = Candidate(
            symbol=profile.symbol,
            asset_class=profile.asset_class,
            profile=profile,
            opportunity_score=profile.opportunity_score * 100,  # convert to 0-100 scale
            acceleration=profile.acceleration,
            lifecycle_state=profile.lifecycle_state,
            data_confidence=profile.data_confidence * 100,
            tosp_filters_passed=passed_filters,
            rank=0,  # will be set after ranking
            reason=f"Passed {len(passed_filters)}/{len(config.get('filter_names', []))} filters",
        )
        candidates.append(candidate)

    # Rank candidates by opportunity score (descending) then acceleration
    ranked = rank_candidates(candidates)
    for idx, cand in enumerate(ranked):
        cand.rank = idx + 1

    # Apply top-N limit
    max_candidates = config.get("max_candidates", 20)
    return ranked[:max_candidates]
