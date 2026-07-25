import pickle
import sys
from datetime import datetime


class DummyOHLCVData:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)
        # If first arg is dict, merge
        if args and isinstance(args[0], dict):
            for k, v in args[0].items():
                setattr(self, k, v)

    def __repr__(self):
        return f"DummyOHLCVData({self.__dict__})"


class CompatUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if "OHLCVData" in name or "OHLCV" in name or "Candle" in name:
            return DummyOHLCVData
        if module.startswith("providers.") or module == "providers.base":
            return DummyOHLCVData
        if module == "__main__.base" and name == "OHLCVData":
            return DummyOHLCVData
        return DummyOHLCVData


def inspect_object(obj, depth=0, max_depth=5, max_items=5):
    indent = "  " * depth
    if depth > max_depth:
        print(f"{indent}... (max depth)")
        return
    typ = type(obj)
    print(f"{indent}Type: {typ}")
    if isinstance(obj, (int, float, str, bool)):
        print(f"{indent}Value: {obj}")
    elif isinstance(obj, datetime):
        print(f"{indent}DateTime: {obj}")
    elif isinstance(obj, list):
        print(f"{indent}Length: {len(obj)}")
        if len(obj) > 0:
            print(f"{indent}First up to {max_items} items:")
            for i, item in enumerate(obj[:max_items]):
                print(f"{indent}  [{i}]:")
                inspect_object(item, depth + 2, max_depth, max_items)
    elif isinstance(obj, dict):
        print(f"{indent}Keys: {list(obj.keys())}")
        for k, v in list(obj.items())[:max_items]:
            print(f"{indent}  {k}:")
            inspect_object(v, depth + 2, max_depth, max_items)
    elif hasattr(obj, "__dict__"):
        attrs = list(obj.__dict__.keys())
        print(f"{indent}Attributes: {attrs}")
        # Show values for first few attrs
        for attr in attrs[:max_items]:
            val = getattr(obj, attr)
            print(f"{indent}  {attr}:", end=" ")
            if isinstance(val, (int, float, str, bool, datetime)):
                print(val)
            else:
                print(f"({type(val)})")
                inspect_object(val, depth + 3, max_depth, max_items)
    else:
        print(f"{indent}Unable to inspect: {obj}")


def main():
    filepath = (
        sys.argv[1] if len(sys.argv) > 1 else "market_price_engine/data/EURUSD_D1.pkl"
    )
    print(f"Inspecting: {filepath}")
    try:
        with open(filepath, "rb") as f:
            unpickler = CompatUnpickler(f)
            obj = unpickler.load()
        print("\n=== ROOT OBJECT ===")
        inspect_object(obj, max_depth=5, max_items=10)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
