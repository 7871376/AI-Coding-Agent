
import os

def load_task():

    # For simplicity, we read the task from a local file. In an enterprise implementation, this could be an API call or database query.
    file_path = "task.txt"

    if not os.path.exists(file_path):
        raise FileNotFoundError("task.txt was not found in the project directory.")

    with open(file_path, "r") as f:
        task = f.read().strip()

    if not task:
        raise ValueError("task.txt is empty. Please provide a task.")

    return task
