"""
Confidence Score – combines data quality and profile consistency into a confidence measure.
"""

from ..models import AssetProfile


def compute_data_confidence(profile: AssetProfile) -> float:
    """
    Compute data confidence based on quality report and profile consistency.

    Returns:
        Confidence score (0-1).
    """
    quality = profile.data_quality

    # Base from quality status
    if quality.status.value == "pass":
        base_confidence = 0.9
    elif quality.status.value == "partial":
        base_confidence = 0.6
    else:
        base_confidence = 0.1

    # Adjust for bars available
    bar_factor = min(1.0, quality.bars_available / 100.0)  # 100 bars = full confidence

    # Adjust for coverage
    coverage_factor = (
        quality.coverage_percentage if quality.coverage_percentage > 0 else 0.5
    )

    # Adjust for OHLC validity
    if not quality.ohlc_valid:
        base_confidence *= 0.5

    # Combine
    confidence = base_confidence * (0.5 * bar_factor + 0.3 * coverage_factor + 0.2)
    return min(1.0, max(0.0, confidence))
