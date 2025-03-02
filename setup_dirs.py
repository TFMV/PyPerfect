#!/usr/bin/env python3
"""
Setup script to create necessary directories for PyPerfect.
Run this before starting the application for the first time.
"""

import os
from pathlib import Path

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent

# Create necessary directories
directories = [
    BASE_DIR / "db" / "queries",
    BASE_DIR / "db" / "migrations",
    BASE_DIR / "db" / "database",
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

# Create __init__.py files to make directories importable
init_files = [
    BASE_DIR / "db" / "__init__.py",
    BASE_DIR / "db" / "queries" / "__init__.py",
]

for init_file in init_files:
    if not init_file.exists():
        with open(init_file, "w") as f:
            f.write("# Make directory importable\n")
        print(f"Created file: {init_file}")

print("\nDirectory setup complete. You can now run the application.")
