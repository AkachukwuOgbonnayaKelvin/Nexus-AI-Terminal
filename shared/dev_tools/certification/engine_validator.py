import sys
import importlib
import os

def path_to_module(file_path):
    """Convert a file path to a Python module import path."""
    if file_path.startswith('./'):
        file_path = file_path[2:]
    # Replace path separators with dots
    module = file_path.replace('/', '.').replace('\\', '.')
    if module.endswith('.py'):
        module = module[:-3]
    # Remove leading dot
    if module.startswith('.'):
        module = module[1:]
    # Replace hyphens with underscores (valid Python identifier)
    module = module.replace('-', '_')
    return module

def certify_engine(engine_path):
    print(f"[CERT] Certifying engine: {engine_path}")

    if os.path.exists(engine_path):
        module_name = path_to_module(engine_path)
        print(f"[CERT] Converting path to module: {module_name}")
    else:
        module_name = engine_path.replace('-', '_')  # also replace hyphens

    try:
        module = importlib.import_module(module_name)
        print(f"[CERT] Successfully imported: {module_name}")
    except Exception as e:
        print(f"[CERT] Failed to import module: {e}")
        return False

    required_methods = ["get_currency_strength", "get_all_currencies"]
    for method in required_methods:
        if not hasattr(module, method):
            print(f"[CERT] Missing method: {method}")
            return False
        if not callable(getattr(module, method)):
            print(f"[CERT] Method not callable: {method}")
            return False
        print(f"[CERT] Method {method} exists and is callable")

    print("[CERT] Engine certification passed")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m shared.dev_tools.certification.engine_validator <path_or_module>")
        sys.exit(1)
    target = sys.argv[1]
    success = certify_engine(target)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
