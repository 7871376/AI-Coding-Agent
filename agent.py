# General import statements and setup
import code
import os

# Import specific methoods and classes from external libraries
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
    
    #set the prompt for the language model, including the task and any previous error if applicable. This allows the model to generate code that addresses the task while also correcting any mistakes from previous attempts.
    #the prompt goes for the next few lines.
    prompt = f"""
Write Python code to complete this task:

{task}

If there was an error previously, fix it.

Previous error:
{previous_error}

Return only Python code.
"""
     # Call the OpenAI API to generate code based on the prompt. The model used is "gpt-4o-mini", which is a smaller version of GPT-4 optimized for code generation. The response is expected to contain the generated Python code.
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Extract the generated code from the API response. The code is expected to be in the content of the first choice returned by the API. This code will then be processed to remove any markdown formatting before being saved and executed.
    code = response.choices[0].message.content

    # Remove markdown code fences if present
    code = code.replace("```python", "").replace("```", "").strip()

    return code

# Save the generated code to a file named "generated_script.py". This allows us to execute the code in subsequent steps and also keeps a record of the generated code for debugging or review purposes.
def save_code(code):
    with open("generated_script.py", "w") as f:
        f.write(code)

# The main function orchestrates the process of generating code, saving it, and executing it. It allows for up to 5 attempts to generate and execute code successfully. If an error occurs during execution, the error message is captured and passed back to the code generation step to help the model correct its output in subsequent attempts.
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

# If all attempts fail, print a final message indicating that the task could not be completed successfully after multiple attempts. This provides feedback to the user and indicates that further intervention may be needed to address the task.
if __name__ == "__main__":
    main()
