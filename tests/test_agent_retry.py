import sys
from pathlib import Path
import pytest

# Add the parent directory to the system path to allow importing from the agent module
sys.path.append(str(Path(__file__).resolve().parents[1]))

from agent.runner import run_python_file
from agent.runtime import execute_task

def test_execute_task_success(monkeypatch):

    def fake_generate_code(task, error):
        return 'print("success")'

    # Mock the generate_code function to return code that prints "success". 
    # This allows us to test the execute_task function's ability to run code 
    # and handle the output without relying on the actual code generation logic, 
    # which may involve external dependencies or complex behavior.
    monkeypatch.setattr("agent.generate_code", fake_generate_code)

    result = execute_task("test task", attempts=2)

    assert "success" in result


def test_execute_task_failure(monkeypatch):

    def fake_generate_code(task, error):
        return 'raise Exception("boom")'

    # Mock the generate_code function to return code that raises an exception. 
    # This allows us to test the execute_task function's retry logic and error 
    # handling when the generated code fails to execute successfully.
    monkeypatch.setattr("agent.generate_code", fake_generate_code)

    with pytest.raises(RuntimeError):
        execute_task("test task", attempts=2)