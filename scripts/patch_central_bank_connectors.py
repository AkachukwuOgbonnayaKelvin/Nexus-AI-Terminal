#!/usr/bin/env python3
"""Patch all central bank connectors to work without API key (stub mode)."""

from pathlib import Path

ROOT = Path(__file__).parent.parent
PROVIDER_BASE = ROOT / "central_bank_engine" / "providers" / "tier1_primary"

banks = ["federal_reserve", "ecb", "boe", "boj", "snb", "boc", "rba", "rbnz"]

for bank in banks:
    connector_path = PROVIDER_BASE / bank / "connector.py"
    if not connector_path.exists():
        continue
    content = connector_path.read_text(encoding="utf-8")

    # Change _connected = bool(self.api_key) to _connected = True
    content = content.replace("self._connected = bool(self.api_key)", "self._connected = True")

    # Make connect() simply return True
    content = content.replace(
        "    def connect(self) -> bool:\n        return self._connected",
        "    def connect(self) -> bool:\n        return True",
    )

    connector_path.write_text(content, encoding="utf-8")
    print(f"✅ Patched {bank} connector")

print("All connectors patched.")
