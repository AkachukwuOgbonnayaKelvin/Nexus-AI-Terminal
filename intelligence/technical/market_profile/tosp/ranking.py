"""
TOSP Ranking – sorts candidates by opportunity score and acceleration.
"""

from ..models import Candidate


def rank_candidates(candidates: list[Candidate]) -> list[Candidate]:
    """
    Sort candidates by opportunity_score descending, then by acceleration descending.

    Returns:
        Sorted list of candidates.
    """
    return sorted(
        candidates, key=lambda c: (c.opportunity_score, c.acceleration), reverse=True
    )
