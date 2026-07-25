import pickle
import sys
from types import SimpleNamespace


class DummyClass:
    """A generic class that can take any attributes."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class CompatUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Map the missing class to our dummy
        if name == "OHLCVData" or name.endswith("OHLCVData"):
            return DummyClass
        # For any other missing class, return SimpleNamespace
        return SimpleNamespace


def inspect_pickle(filepath):
    try:
        with open(filepath, "rb") as f:
            unpickler = CompatUnpickler(f)
            data = unpickler.load()
        print(f"Loaded {filepath}")
        print(f"Type of data: {type(data)}")
        if isinstance(data, list):
            print(f"List length: {len(data)}")
            if len(data) > 0:
                sample = data[0]
                print(f"First element type: {type(sample)}")
                if hasattr(sample, "__dict__"):
                    print(f"Attributes: {list(sample.__dict__.keys())}")
                    print(f"Sample: {sample.__dict__}")
                else:
                    print(f"Sample: {sample}")
        elif isinstance(data, dict):
            print(f"Keys: {list(data.keys())}")
        elif hasattr(data, "__dict__"):
            print(f"Attributes: {list(data.__dict__.keys())}")
            print(f"Sample: {data.__dict__}")
        else:
            print(f"Data: {data}")
    except Exception as e:
        print(f"Error loading {filepath}: {e}")


if __name__ == "__main__":
    # Test with one of the failing files
    test_file = "market_price_engine/data/EURUSD_D1.pkl"
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
    inspect_pickle(test_file)
