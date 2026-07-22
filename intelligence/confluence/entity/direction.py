"""
Phase 4: Global Entity Intelligence - Direction Classification

Centralized direction classification for all entity ratings.
"""

from ..contracts import Direction


def classify_direction(score: float) -> Direction:
    """
    Classify direction from a score.

    Args:
        score: Score from -100 to +100

    Returns:
        Direction: BULLISH, BEARISH, or NEUTRAL
    """
    if score >= 20.0:
        return Direction.BULLISH
    elif score <= -20.0:
        return Direction.BEARISH
    else:
        return Direction.NEUTRAL


def is_bullish(score: float) -> bool:
    """Check if score indicates bullish direction."""
    return classify_direction(score) == Direction.BULLISH


def is_bearish(score: float) -> bool:
    """Check if score indicates bearish direction."""
    return classify_direction(score) == Direction.BEARISH


def is_neutral(score: float) -> bool:
    """Check if score indicates neutral direction."""
    return classify_direction(score) == Direction.NEUTRAL


def get_direction_label(score: float) -> str:
    """Get human-readable direction label."""
    direction = classify_direction(score)
    return direction.value


def direction_strength(score: float) -> float:
    """Get the strength of the direction (0-100)."""
    return abs(score)


def is_strong_bullish(score: float) -> bool:
    """Check if score is strongly bullish (>= 50)."""
    return score >= 50.0


def is_strong_bearish(score: float) -> bool:
    """Check if score is strongly bearish (<= -50)."""
    return score <= -50.0
