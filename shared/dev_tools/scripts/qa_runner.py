import sys
import subprocess
import os

def run_qa(directory="."):
    print(f"[QA] Running QA checks on {directory}")
    success = True

    # Run flake8 (linting)
    result = subprocess.run(["flake8", directory], capture_output=True, text=True)
    if result.returncode != 0:
        print("[QA] Flake8 found issues:")
        print(result.stdout)
        print(result.stderr)
        success = False
    else:
        print("[QA] Flake8 passed")

    # Run pytest
    result = subprocess.run(["pytest", directory, "-q"], capture_output=True, text=True)
    if result.returncode != 0:
        print("[QA] Pytest found failures:")
        print(result.stdout)
        print(result.stderr)
        success = False
    else:
        print("[QA] Pytest passed")

    if success:
        print("[QA] All checks passed")
        return 0
    else:
        print("[QA] Some checks failed")
        return 1

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(run_qa(target))
