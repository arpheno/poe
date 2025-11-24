#!/usr/bin/env python3
"""
Script to check which modules from the poe package are imported by the API.
This helps us determine which files need to be included in the Docker image.
"""

import os
import re
import sys
from pathlib import Path

def find_imports(directory, package_name="poe"):
    """Find all imports from a specific package in Python files."""
    imports = set()
    import_pattern = re.compile(rf"from\s+{package_name}\.(\w+(?:\.\w+)*)\s+import|import\s+{package_name}\.(\w+(?:\.\w+)*)")
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        for match in import_pattern.finditer(content):
                            # Get the first non-None group
                            module = next(filter(None, match.groups()), "")
                            if module:
                                imports.add(module)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}", file=sys.stderr)
    
    return imports

def get_package_structure(directory, package_name="poe"):
    """Get the structure of a package."""
    structure = set()
    base_path = Path(directory) / package_name
    
    if not base_path.exists():
        print(f"Package directory {base_path} does not exist", file=sys.stderr)
        return structure
    
    for root, _, files in os.walk(base_path):
        rel_path = Path(root).relative_to(directory)
        if str(rel_path) != package_name:  # Skip the root package directory
            module_path = str(rel_path).replace(os.path.sep, ".")
            structure.add(module_path)
    
    return structure

def main():
    """Main function."""
    # Find imports in the API package
    api_imports = find_imports("packages/your-api")
    print("Imports from poe package in the API:")
    for imp in sorted(api_imports):
        print(f"- {imp}")
    
    # Get the structure of the poe package
    poe_structure = get_package_structure(".")
    print("\nModules in the poe package:")
    for module in sorted(poe_structure):
        if any(module.startswith(imp) for imp in api_imports):
            print(f"- {module} (USED)")
        else:
            print(f"- {module}")
    
    # Find modules that are imported but not in the structure
    missing = {imp for imp in api_imports if not any(imp == module or module.startswith(imp) for module in poe_structure)}
    if missing:
        print("\nWARNING: The following imports could not be found in the package structure:")
        for imp in sorted(missing):
            print(f"- {imp}")
    
    # Suggest directories to include in Dockerfile
    print("\nDirectories to include in Dockerfile:")
    top_level_modules = {imp.split(".")[0] for imp in api_imports}
    for module in sorted(top_level_modules):
        print(f"COPY poe/{module} /app/poe/{module}/")

if __name__ == "__main__":
    main() 