import sys
from pathlib import Path
import pytest

# Add the parent directory to the system path to allow importing from the agent module
sys.path.append(str(Path(__file__).resolve().parents[1]))

from agent.runner import run_python_file

def test_run_python_file_success(tmp_path):

    # Create a temporary Python script that prints "hello world"
    script = tmp_path / "hello.py"

    # Write a simple Python script to the file
    script.write_text(
        'print("hello world")'
    )

    # Run the script using the run_python_file function and capture the output
    result = run_python_file(script)

    # Assert that the output contains "hello world"
    assert "hello world" in result

def test_run_python_file_error(tmp_path):

    # Create a temporary Python script that raises an exception
    script = tmp_path / "error_script.py"

    # Write a Python script that raises an exception to the file
    script.write_text(
        'raise Exception("boom")'
    )

    # Run the script using the run_python_file function and capture the output
    result = run_python_file(script)

    # Assert that the output contains "boom"
    assert "boom" in result