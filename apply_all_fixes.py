#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

# Find the asset_impact_engine.py file
engine_file = None
for root, dirs, files in os.walk("."):
    if "asset_impact_engine.py" in files:
        engine_file = os.path.join(root, "asset_impact_engine.py")
        break

if not engine_file:
    print("Could not find asset_impact_engine.py")
    exit(1)

print(f"Found engine file: {engine_file}")

# Read current content
with open(engine_file, "r", encoding="utf-8") as f:
    content = f.read()

print("Reading file complete")

# Check if fixes are already applied
if "_normalize_score" in content:
    print("_normalize_score already exists, continuing...")

# ============================================================
# Add _get_asset_class if missing
# ============================================================
if "_get_asset_class" not in content:
    print("Adding _get_asset_class method...")
    lines = content.split("\n")
    insert_pos = -1
    for i, line in enumerate(lines):
        if "class AssetImpactEngine" in line:
            insert_pos = i
            break

    if insert_pos != -1:
        for i in range(insert_pos, len(lines)):
            if "def __init__" in lines[i]:
                insert_pos = i + 1
                break

    new_method = '''
    def _get_asset_class(self, asset: str) -> str:
        """Determine asset class from symbol."""
        fx_pairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'AUDUSD', 'NZDUSD']
        commodities = ['XAUUSD', 'XAGUSD', 'WTI', 'BRENT', 'COPPER']
        indices = ['US500', 'US100', 'US30', 'GER40', 'UK100', 'JP225']

        if asset in fx_pairs:
            return 'FX'
        elif asset in commodities:
            return 'Commodity'
        elif asset in indices:
            return 'Index'
        else:
            return 'Unknown'
'''
    if insert_pos != -1:
        lines.insert(insert_pos, new_method)
        content = "\n".join(lines)
        print("Added _get_asset_class")

# ============================================================
# Add _normalize_score if missing
# ============================================================
if "_normalize_score" not in content:
    print("Adding _normalize_score method...")
    lines = content.split("\n")
    insert_pos = -1
    for i, line in enumerate(lines):
        if "def _get_asset_class" in line:
            for j in range(i + 1, len(lines)):
                if lines[j].strip() and lines[j].strip().startswith("def "):
                    insert_pos = j
                    break
            break

    if insert_pos == -1:
        for i, line in enumerate(lines):
            if "def __init__" in line:
                insert_pos = i + 1
                break

    new_method = """
    def _normalize_score(self, raw_score: float, max_score: float = 100.0) -> float:
        if raw_score <= 0:
            return 0.0
        if raw_score >= max_score:
            return max_score
        normalized = (raw_score / max_score) * 100
        return round(normalized, 1)
"""
    if insert_pos != -1:
        lines.insert(insert_pos, new_method)
        content = "\n".join(lines)
        print("Added _normalize_score")

# ============================================================
# Add _analyze_currency_strength
# ============================================================
if "_analyze_currency_strength" not in content:
    print("Adding _analyze_currency_strength method...")
    lines = content.split("\n")
    insert_pos = -1
    for i, line in enumerate(lines):
        if "def _normalize_score" in line:
            for j in range(i + 1, len(lines)):
                if lines[j].strip() and lines[j].strip().startswith("def "):
                    insert_pos = j
                    break
            break

    if insert_pos == -1:
        for i, line in enumerate(lines):
            if "def __init__" in line:
                insert_pos = i + 1
                break

    new_method = """
    def _analyze_currency_strength(self, currency: str, factors: dict) -> dict:
        score = 50.0
        factors_used = 0

        currency_factors = {
            'USD': {'growth': 0.20, 'inflation': 0.15, 'rates': 0.30, 'risk_on': -0.10, 'liquidity': 0.15, 'dollar_strength': 0.10},
            'EUR': {'growth': 0.25, 'inflation': 0.15, 'rates': 0.25, 'risk_on': 0.20, 'liquidity': 0.15},
            'GBP': {'growth': 0.25, 'inflation': 0.15, 'rates': 0.25, 'risk_on': 0.20, 'liquidity': 0.15},
            'JPY': {'growth': -0.20, 'inflation': -0.10, 'rates': -0.20, 'risk_on': -0.30, 'liquidity': 0.20}
        }

        weights = currency_factors.get(currency, {})
        for factor_name, weight in weights.items():
            if factor_name in factors:
                factor_value = factors[factor_name]
                impact = (factor_value - 0.5) * 2
                score += impact * weight * 100
                factors_used += 1

        final_score = max(0, min(100, score))
        confidence = min(100, (factors_used / max(1, len(weights))) * 100)

        return {
            'currency': currency,
            'score': final_score,
            'bias': 'BULLISH' if final_score > 55 else 'BEARISH' if final_score < 45 else 'NEUTRAL',
            'confidence': confidence,
            'factors_used': factors_used
        }
"""
    if insert_pos != -1:
        lines.insert(insert_pos, new_method)
        content = "\n".join(lines)
        print("Added _analyze_currency_strength")

# ============================================================
# Update _analyze_fx_pair
# ============================================================
if "_analyze_fx_pair" in content:
    print("Updating _analyze_fx_pair method...")
    pattern = r"def _analyze_fx_pair\(.*?\).*?(?=\n    def |\Z)"
    replacement = """
    def _analyze_fx_pair(self, pair: str, factors: dict) -> dict:
        base = pair[:3]
        quote = pair[3:6]
        base_analysis = self._analyze_currency_strength(base, factors)
        quote_analysis = self._analyze_currency_strength(quote, factors)
        net_score = base_analysis['score'] - quote_analysis['score'] + 50

        if net_score > 55:
            bias = 'BULLISH'
        elif net_score < 45:
            bias = 'BEARISH'
        else:
            bias = 'NEUTRAL'

        confidence = (base_analysis['confidence'] + quote_analysis['confidence']) / 2
        final_score = self._normalize_score(net_score)

        drivers = [
            {'name': 'Growth Differential', 'direction': 'BULLISH' if factors.get('growth', 0.5) > 0.5 else 'BEARISH', 'score': factors.get('growth', 0.5) * 100},
            {'name': 'Rate Differential', 'direction': 'BULLISH' if factors.get('rate_differential', 0.5) > 0.5 else 'BEARISH', 'score': factors.get('rate_differential', 0.5) * 100},
            {'name': 'Risk Sentiment', 'direction': 'BULLISH' if factors.get('risk_on', 0.5) > 0.5 else 'BEARISH', 'score': factors.get('risk_on', 0.5) * 100}
        ]

        return {
            'asset': pair,
            'asset_class': 'FX',
            'bias': bias,
            'score': final_score,
            'confidence': confidence,
            'base_currency': base_analysis,
            'quote_currency': quote_analysis,
            'drivers': drivers
        }
"""
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    print("Updated _analyze_fx_pair")

# Write the updated content
with open(engine_file, "w", encoding="utf-8") as f:
    f.write(content)

print("=" * 70)
print("All fixes applied successfully!")
print("=" * 70)
