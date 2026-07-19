#!/usr/bin/env python3
"""Parse a CFTC COT file."""

import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from institutional_positioning_engine.parser.cftc_parser import CFTCOTParser


def main():
    file_path = "your_cot_file.txt"  # Replace with your file path
    parser = CFTCOTParser()
    records = parser.parse_file(file_path, report_type="disaggregated")
    print(f"Parsed {len(records)} records")
    if records:
        print("Sample record:")
        for key, value in records[0].items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
