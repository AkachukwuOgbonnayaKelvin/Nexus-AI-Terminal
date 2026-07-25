import pickle


class DummyCallable:
    def __call__(self, *args, **kwargs):
        print(f"Callable called with args={args}, kwargs={kwargs}")
        # Return a dummy list to avoid further errors
        return []


class CompatUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Map any missing class to DummyCallable so it can be called
        return DummyCallable


with open("market_price_engine/data/CL=F_D1.pkl", "rb") as f:
    unpickler = CompatUnpickler(f)
    obj = unpickler.load()

print(f"Loaded object type: {type(obj)}")
print(f"Is callable? {callable(obj)}")

if callable(obj):
    print("Calling the object to get the data...")
    result = obj()
    print(f"Result type: {type(result)}")
    if isinstance(result, list):
        print(f"Result length: {len(result)}")
        if result:
            print(f"First element type: {type(result[0])}")
            if hasattr(result[0], "__dict__"):
                print(f"First element attributes: {list(result[0].__dict__.keys())}")
    else:
        print(f"Result: {result}")
else:
    if hasattr(obj, "__dict__"):
        print(f"Attributes: {list(obj.__dict__.keys())}")
