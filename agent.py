import code
import os
from dotenv import load_dotenv
from openai import OpenAI
from runner import run_python_file
from task import load_task

load_dotenv()
client = OpenAI()

# Load the task from task.txt. Throw an error if the file is missing or empty. This ensures we have a valid task before proceeding.
try:
    TASK = load_task()
except Exception as e:
    print(f"Error loading task: {e}")
    exit(1)


def generate_code(task, previous_error=None):

    prompt = f"""
Write Python code to complete this task:

{task}

If there was an error previously, fix it.

Previous error:
{previous_error}

Return only Python code.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    code = response.choices[0].message.content

    # Remove markdown code fences if present
    code = code.replace("```python", "").replace("```", "").strip()

    return code

def save_code(code):
    with open("generated_script.py", "w") as f:
        f.write(code)


def main():
    error = None

    for attempt in range(5):

        print(f"\nAttempt {attempt+1}")

        code = generate_code(TASK, error)

        save_code(code)

        result = run_python_file("generated_script.py")

        print("\nExecution Result:\n", result)

        if "Traceback" not in result:
            print("\nSuccess!")
            break

        error = result


if __name__ == "__main__":
    main()