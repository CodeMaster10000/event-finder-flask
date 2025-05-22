#!/usr/bin/env python3
import os
import shutil

def remove_pycache_and_pyc(base_dir: str = "."):
    for root, dirs, files in os.walk(base_dir, topdown=False):
        # remove __pycache__ directories
        if "__pycache__" in dirs:
            cache_dir = os.path.join(root, "__pycache__")
            print(f"Removing directory: {cache_dir}")
            shutil.rmtree(cache_dir)
        # remove .pyc and .pyo files
        for fname in files:
            if fname.endswith((".pyc", ".pyo")):
                file_path = os.path.join(root, fname)
                print(f"Removing file:      {file_path}")
                os.remove(file_path)

if __name__ == "__main__":
    remove_pycache_and_pyc()
    print("Clean up complete.")
