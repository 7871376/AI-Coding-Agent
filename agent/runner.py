import subprocess
import sys
import shutil
import os

# This function runs a Python file and captures its output. It uses the subprocess module 
# to execute the file with the same Python interpreter that is running the current script. 
# The output is captured and returned as a string. If the execution is successful, the 
# standard output is returned; if there is an error, the standard error is returned instead.
def run_python_file(file_name):
    
     # Detect if running inside PyInstaller bundle
    if getattr(sys, "frozen", False):
        # Try to find system Python
        python = shutil.which("python") or shutil.which("python3")
        if not python:
            raise RuntimeError("No system Python found to execute generated script.")
    else:
        python = sys.executable

    result = subprocess.run(
        [python, file_name],
        capture_output=True,
        text=True,
        timeout=20
    )

    if result.returncode == 0:
        return result.stdout
    else:
        return result.stderr