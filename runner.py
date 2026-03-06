import subprocess
import sys

# This function runs a Python file and captures its output. It uses the subprocess module to execute the file with the same Python interpreter that is running the current script. The output is captured and returned as a string. If the execution is successful, the standard output is returned; if there is an error, the standard error is returned instead.
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
