import os
import re
import sys

def update_imports_in_file(filepath):
    """Update import statements to use shared.dev_tools"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace old imports with new ones
    replacements = [
        # QA tools
        (r'from tools\.qa\.', 'from shared.dev_tools.qa.'),
        (r'import tools\.qa', 'import shared.dev_tools.qa'),
        (r'from tests\.certification\.', 'from shared.dev_tools.certification.'),
        (r'import tests\.certification', 'import shared.dev_tools.certification'),
        (r'from tools\.certification\.', 'from shared.dev_tools.certification.'),
        (r'import tools\.certification', 'import shared.dev_tools.certification'),
        # Scripts
        (r'from scripts\.qa_runner', 'from shared.dev_tools.scripts.qa_runner'),
        (r'from scripts\.project_integrity', 'from shared.dev_tools.scripts.project_integrity'),
        # Certification runner
        (r'from scripts\.certify_market_structure', 'from shared.dev_tools.scripts.certify_market_structure'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """Walk through the codebase and update imports"""
    base_path = '.'
    if not os.path.exists(base_path):
        print(f"Error: {base_path} not found")
        return
    
    for root, dirs, files in os.walk(base_path):
        # Skip venv, .git, and shared folders to avoid modifying them twice
        if 'venv' in root or '.git' in root or 'shared' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                update_imports_in_file(filepath)
                print(f"Updated: {filepath}")

if __name__ == '__main__':
    main()
