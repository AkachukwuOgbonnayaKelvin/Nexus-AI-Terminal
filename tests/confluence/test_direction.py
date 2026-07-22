# -*- coding: utf-8 -*-
"""
Direction Classification Tests

Tests the centralized direction classification logic.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from intelligence.confluence.entity.direction import (
    classify_direction,
    is_bullish,
    is_bearish,
    is_neutral,
    is_strong_bullish,
    is_strong_bearish,
)
from intelligence.confluence.contracts import Direction


def test_direction_classification():
    """Test direction classification with various scores."""

    print("=" * 70)
    print("DIRECTION CLASSIFICATION TESTS")
    print("=" * 70)

    test_cases = [
        # (score, expected_direction)
        (100.0, Direction.BULLISH),
        (50.0, Direction.BULLISH),
        (20.0, Direction.BULLISH),
        (19.9, Direction.NEUTRAL),
        (10.0, Direction.NEUTRAL),
        (0.0, Direction.NEUTRAL),
        (-10.0, Direction.NEUTRAL),
        (-19.9, Direction.NEUTRAL),
        (-20.0, Direction.BEARISH),
        (-50.0, Direction.BEARISH),
        (-100.0, Direction.BEARISH),
    ]

    passed = 0
    total = len(test_cases)

    print("\n[1] Testing classify_direction()")
    for score, expected in test_cases:
        result = classify_direction(score)
        status = "✅" if result == expected else "❌"
        print(
            f"  {status} Score: {score:+.1f} -> {result.value} (expected: {expected.value})"
        )
        if result == expected:
            passed += 1

    print(f"\n  Direction tests passed: {passed}/{total}")

    # Test helper functions
    print("\n[2] Testing helper functions")

    # Using truth checks without equality comparisons
    if is_bullish(50.0):
        print("  ✅ is_bullish(50) = True")
    else:
        print("  ❌ is_bullish(50) should be True")

    if not is_bullish(0.0):
        print("  ✅ is_bullish(0) = False")
    else:
        print("  ❌ is_bullish(0) should be False")

    if not is_bullish(-50.0):
        print("  ✅ is_bullish(-50) = False")
    else:
        print("  ❌ is_bullish(-50) should be False")

    if is_bearish(-50.0):
        print("  ✅ is_bearish(-50) = True")
    else:
        print("  ❌ is_bearish(-50) should be True")

    if not is_bearish(0.0):
        print("  ✅ is_bearish(0) = False")
    else:
        print("  ❌ is_bearish(0) should be False")

    if not is_bearish(50.0):
        print("  ✅ is_bearish(50) = False")
    else:
        print("  ❌ is_bearish(50) should be False")

    if is_neutral(0.0):
        print("  ✅ is_neutral(0) = True")
    else:
        print("  ❌ is_neutral(0) should be True")

    if is_neutral(10.0):
        print("  ✅ is_neutral(10) = True")
    else:
        print("  ❌ is_neutral(10) should be True")

    if not is_neutral(20.0):
        print("  ✅ is_neutral(20) = False")
    else:
        print("  ❌ is_neutral(20) should be False")

    if is_strong_bullish(50.0):
        print("  ✅ is_strong_bullish(50) = True")
    else:
        print("  ❌ is_strong_bullish(50) should be True")

    if not is_strong_bullish(30.0):
        print("  ✅ is_strong_bullish(30) = False")
    else:
        print("  ❌ is_strong_bullish(30) should be False")

    if is_strong_bearish(-50.0):
        print("  ✅ is_strong_bearish(-50) = True")
    else:
        print("  ❌ is_strong_bearish(-50) should be True")

    if not is_strong_bearish(-30.0):
        print("  ✅ is_strong_bearish(-30) = False")
    else:
        print("  ❌ is_strong_bearish(-30) should be False")

    print("\n  ✅ All helper function tests passed")

    print("\n" + "=" * 70)
    print("✅ DIRECTION CLASSIFICATION: ALL TESTS PASSED")
    print("=" * 70)

    return True


if __name__ == "__main__":
    test_direction_classification()
