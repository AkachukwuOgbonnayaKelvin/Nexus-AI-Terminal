"""
Test that shared dev-tools work correctly
"""
import sys
import os

# Add the current directory to path
sys.path.insert(0, os.getcwd())

print("��� Testing shared dev-tools...")

try:
    from shared.dev_tools.qa import __all__ as qa_all
    print(f"✅ QA tools loaded: {qa_all}")
except Exception as e:
    print(f"❌ QA tools failed: {e}")

try:
    from shared.dev_tools.certification import __all__ as cert_all
    print(f"✅ Certification tools loaded: {cert_all}")
except Exception as e:
    print(f"❌ Certification tools failed: {e}")

try:
    from shared.dev_tools.scripts import qa_runner
    print(f"✅ Scripts loaded: {qa_runner}")
except Exception as e:
    print(f"❌ Scripts failed: {e}")

print("✅ Dev-tools test complete!")
