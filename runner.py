import subprocess
import sys

def run_python_file(file_name):
    result = subprocess.run(
        [sys.executable, file_name],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return result.stdout
    else:
        return result.stderr