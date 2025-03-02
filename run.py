#!/usr/bin/env python3
"""
Run script for PyPerfect.
This script sets up directories and starts the application.
"""

import os
import sys
import uvicorn
from pathlib import Path

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent

# Ensure the app directory is in the Python path
sys.path.insert(0, str(BASE_DIR))

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

print("\nDirectory setup complete. Starting the application...\n")

# Start the application
if __name__ == "__main__":
    uvicorn.run("app.app:app", host="127.0.0.1", port=8000, reload=True)
