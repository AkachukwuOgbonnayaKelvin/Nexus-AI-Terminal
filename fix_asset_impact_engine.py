#!/usr/bin/env python3
"""
Script to fix the Asset Impact Engine
Run: python fix_asset_impact_engine.py
"""

import os
import sys

# Find the asset_impact_engine.py file
engine_file = None
for root, dirs, files in os.walk("."):
    if "asset_impact_engine.py" in files:
        engine_file = os.path.join(root, "asset_impact_engine.py")
        break

if not engine_file:
    print("❌ Could not find asset_impact_engine.py")
    sys.exit(1)

print(f"✅ Found engine file: {engine_file}")

# Read the current content
with open(engine_file, "r") as f:
    content = f.read()

# Check if the fixes are already applied
if "_normalize_score" in content and "def _normalize_score" in content:
    print("✅ _normalize_score already exists")
else:
    print("⚠️ _normalize_score not found - need to add it")

    # Find where to insert the method
    lines = content.split("\n")

    # Find a good insertion point (after class initialization)
    insert_pos = -1
    for i, line in enumerate(lines):
        if "def __init__" in line and "self." in line:
            # Find the end of __init__ method
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == "" or lines[j].strip().startswith("def "):
                    insert_pos = j
                    break
            break

    if insert_pos == -1:
        print("❌ Could not find insertion point")
        sys.exit(1)

    # Create the new method
    new_method = '''
    def _normalize_score(self, raw_score: float, max_score: float = 100.0) -> float:
        """Normalize score to 0-100 range with proper scaling."""
        if raw_score <= 0:
            return 0.0
        if raw_score >= max_score:
            return max_score
        normalized = (raw_score / max_score) * 100
        return round(normalized, 1)
'''

    # Insert the method
    lines.insert(insert_pos, new_method)
    content = "\n".join(lines)

    # Write the updated content
    with open(engine_file, "w") as f:
        f.write(content)

    print("✅ Added _normalize_score method")

print("=" * 70)
print("Fix complete! Now run the certification test.")
print("=" * 70)
