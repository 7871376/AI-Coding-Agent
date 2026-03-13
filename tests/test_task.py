import sys
from pathlib import Path
import pytest

# Add the parent directory to the system path to allow importing from the agent module
sys.path.append(str(Path(__file__).resolve().parents[1]))

from agent.task import load_task


def test_load_task_success(tmp_path):
    # Create a temporary task file
    task_file = tmp_path / "task.txt"
    task_file.write_text("Write Python code")

    # Load the task
    result = load_task(task_file)

    # Assert that the task is loaded correctly
    assert result == "Write Python code"
    
def test_load_task_file_missing():

    # Test that loading a non-existent file raises a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        load_task("this_file_does_not_exist.txt")

def test_load_task_empty(tmp_path):

    # Create a temporary task file that is empty
    task_file = tmp_path / "task.txt"
    task_file.write_text("")

    # Test that loading an empty file raises a ValueError with the expected message
    with pytest.raises(ValueError, match="Task file is empty. Please provide a task."):
        load_task(task_file)