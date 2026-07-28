"""
Profile Score – combines individual analyzer scores into a weighted opportunity score.
"""

from ..config import AnalyzerWeights
from ..models import ProfileDimensionScore


def compute_opportunity_score(
    dimensions: dict[str, ProfileDimensionScore],
    asset_class: str,
    weights: AnalyzerWeights,
) -> float:
    """
    Compute the weighted opportunity score from dimension scores.

    Args:
        dimensions: dict mapping dimension name -> ProfileDimensionScore.
        asset_class: the asset class (e.g., "fx", "index").
        weights: AnalyzerWeights instance.

    Returns:
        Opportunity score (0-1).
    """
    class_weights = weights.get_weights(asset_class)
    total_score = 0.0
    total_weight = 0.0

    for dim, score_obj in dimensions.items():
        w = class_weights.get(dim, 0.0)
        total_score += score_obj.score * w
        total_weight += w

    if total_weight == 0:
        return 0.0

    return total_score / total_weight
