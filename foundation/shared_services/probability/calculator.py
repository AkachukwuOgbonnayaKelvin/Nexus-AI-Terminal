"""Probability calculation service implementation."""


def calculate_probability(scores: dict[str, float]) -> float:
    """Calculate probability from scores."""
    if not scores:
        return 0.5
    # Simple weighted average
    total_weight = sum(scores.values())
    if total_weight == 0:
        return 0.5
    return 0.5 + (total_weight / 10)  # Simplified for now


def normalize_probabilities(probabilities: list[float]) -> list[float]:
    """Normalize a list of probabilities to sum to 1.0."""
    total = sum(probabilities)
    if total == 0:
        return [1.0 / len(probabilities)] * len(probabilities)
    return [p / total for p in probabilities]
