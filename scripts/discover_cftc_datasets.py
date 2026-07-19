#!/usr/bin/env python3
"""Discover CFTC PRE dataset IDs."""

import json

import requests


def discover_datasets():
    """Discover available datasets from CFTC PRE API."""
    # The CFTC PRE API uses a catalog endpoint
    catalog_url = "https://publicreporting.cftc.gov/api/catalog/v1"
    try:
        response = requests.get(catalog_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        print("✅ Catalog retrieved successfully")
        print(json.dumps(data, indent=2)[:2000])
        return data
    except Exception as e:
        print(f"❌ Failed to retrieve catalog: {e}")

    # Fallback: Try the datasets endpoint
    datasets_url = "https://publicreporting.cftc.gov/api/datasets/v1"
    try:
        response = requests.get(datasets_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        print("✅ Datasets retrieved successfully")
        # Look for COT-related datasets
        for dataset in data:
            if "cot" in str(dataset).lower() or "commitment" in str(dataset).lower():
                print(f"Found COT dataset: {dataset}")
        return data
    except Exception as e:
        print(f"❌ Failed to retrieve datasets: {e}")

    # If both fail, we'll use the resource endpoint directly
    # The CFTC uses resource IDs like: https://publicreporting.cftc.gov/resource/XXXX-XXXX.json
    # We'll try to find the correct one by listing resources
    resource_url = "https://publicreporting.cftc.gov/api/resource/v1"
    try:
        response = requests.get(resource_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Resources retrieved: {len(data) if data else 0}")
        return data
    except Exception as e:
        print(f"❌ Failed to retrieve resources: {e}")

    return None


if __name__ == "__main__":
    discover_datasets()
