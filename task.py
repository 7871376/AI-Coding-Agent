
import os

def load_task(taskfile):

    # For simplicity, we read the task from a local file. In an enterprise implementation, this could be an API call or database query.
    

    if not os.path.exists(taskfile):
        raise FileNotFoundError("Task file was not found.")

    with open(taskfile, "r") as f:
        task = f.read().strip()

    if not task:
        raise ValueError("Task file is empty. Please provide a task.")

    return task
