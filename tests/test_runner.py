import sys
from pathlib import Path
import pytest

# Add the parent directory to the system path to allow importing from the agent module
sys.path.append(str(Path(__file__).resolve().parents[1]))

from runner import run_python_file

def test_run_python_file(tmp_path):

    # Create a temporary Python script that prints "hello world"
    script = tmp_path / "test_script.py"

    # Write a simple Python script to the file
    script.write_text(
        'print("hello world")'
    )

    # Run the script using the run_python_file function and capture the output
    result = run_python_file(script)

    # Assert that the output contains "hello world"
    assert "hello world" in result