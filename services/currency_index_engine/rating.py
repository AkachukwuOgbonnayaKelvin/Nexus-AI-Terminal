def compute_rating(overall_score: float) -> str:
    """Convert a score in [-100, 100] to a rating string."""
    if overall_score >= 80:
        return 'STRONG_BUY'
    elif overall_score >= 60:
        return 'BUY'
    elif overall_score >= 20:
        return 'WEAK_BUY'
    elif overall_score >= -20:
        return 'NEUTRAL'
    elif overall_score >= -60:
        return 'WEAK_SELL'
    elif overall_score >= -80:
        return 'SELL'
    else:
        return 'STRONG_SELL'
