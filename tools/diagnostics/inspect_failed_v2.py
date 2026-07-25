import pickle


class CompatObject:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __call__(self, *args, **kwargs):
        print(f"CompatibleObject called with args={args}, kwargs={kwargs}")
        # If the original object is a callable that returns data, we try to return a list of candles.
        # Since we don't know the structure, we return an empty list for now to avoid error.
        return []


class CompatUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Map any missing class to CompatObject
        return CompatObject


with open("market_price_engine/data/CL=F_D1.pkl", "rb") as f:
    unpickler = CompatUnpickler(f)
    obj = unpickler.load()

print(f"Loaded object type: {type(obj)}")
print(f"Is callable? {callable(obj)}")
if hasattr(obj, "__dict__"):
    print(f"Attributes: {list(obj.__dict__.keys())}")

# If it's callable, call it to see what we get
if callable(obj):
    print("Calling the object...")
    result = obj()
    print(f"Result type: {type(result)}")
    if isinstance(result, list):
        print(f"Result length: {len(result)}")
        if result:
            print(f"First element type: {type(result[0])}")
            if hasattr(result[0], "__dict__"):
                print(f"First element attributes: {list(result[0].__dict__.keys())}")
    elif isinstance(result, dict):
        print(f"Result keys: {list(result.keys())}")
    else:
        print(f"Result: {result}")
