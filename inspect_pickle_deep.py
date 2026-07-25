import pickle
import pickletools
import sys


class GenericObject:
    """A generic object that accepts any attributes and arguments."""

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return f"GenericObject({self._kwargs})"


class CompatUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Map missing classes to our generic object
        return GenericObject


def inspect_pickle(filepath):
    print(f"\n=== Inspecting {filepath} ===")

    # 1. Show pickle opcodes (limited to first 50 lines)
    try:
        with open(filepath, "rb") as f:
            data = f.read()
        print("\n[Pickle Opcodes (first 20)]")
        pickletools.dis(data, out=sys.stdout, memo=None, indentlevel=4, annotate=0)
    except Exception as e:
        print(f"Error disassembling pickle: {e}")

    # 2. Try loading with compatibility
    try:
        with open(filepath, "rb") as f:
            unpickler = CompatUnpickler(f)
            obj = unpickler.load()

        print("\n[Loaded object]")
        print(f"Type: {type(obj)}")

        if isinstance(obj, list):
            print(f"Length: {len(obj)}")
            if len(obj) > 0:
                sample = obj[0]
                print(f"Sample type: {type(sample)}")
                if hasattr(sample, "__dict__"):
                    print(f"Sample attributes: {list(sample.__dict__.keys())}")
                    print(f"Sample: {sample.__dict__}")
                elif isinstance(sample, dict):
                    print(f"Sample keys: {list(sample.keys())}")
                    print(f"Sample: {sample}")
                else:
                    print(f"Sample: {sample}")
        elif isinstance(obj, dict):
            print(f"Keys: {list(obj.keys())}")
        elif hasattr(obj, "__dict__"):
            print(f"Attributes: {list(obj.__dict__.keys())}")
            print(f"Object: {obj.__dict__}")
        else:
            print(f"Data: {obj}")
    except Exception as e:
        print(f"\n[Load error] {e}")


if __name__ == "__main__":
    import glob

    # Inspect a few files
    files = glob.glob("market_price_engine/data/*.pkl")[:5]  # first 5
    for f in files:
        inspect_pickle(f)
