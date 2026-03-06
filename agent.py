# General import statements and setup
import argparse
import code
import logging
import os

# Import specific methoods and classes from external libraries
from dotenv import load_dotenv
from openai import OpenAI
from runner import run_python_file
from task import load_task

# Set up logging configuration to provide informative messages about the execution of the script. This includes timestamps, log levels, and the message content, which can help with debugging and understanding the flow of the program.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
     handlers=[
        logging.FileHandler("agent.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


#initialize the OpenAI client and load environment variables from a .env file. This allows us to securely manage API keys and other configuration settings needed for the OpenAI API to function properly. The client will be used to interact with the OpenAI API for generating code based on the specified task.
load_dotenv()
client = OpenAI()


# Function to parse command-line arguments. This allows users to specify the task file and the number of attempts when running the script. The default number of attempts is set to 5, but it can be customized by the user.
def parse_arguments():

    parser = argparse.ArgumentParser(
        description="AI Coding Agent that generates and executes Python code."
    )

    # sets a default file for the coding task if the user fails to provide one. This allows the script to run with a predefined task without requiring additional input, while still giving users the flexibility to specify their own task file if desired.
    parser.add_argument(
        "taskfile",
        nargs="?",
        default="task.txt",
        help="Path to the file containing the coding task (default: task.txt)"
    )

    parser.add_argument(
        "--attempts",
        type=int,
        default=5,
        help="Maximum number of attempts the agent should try"
    )

    return parser.parse_args()

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

    for attempt in range(args.attempts):

        logger.info(f"Attempt {attempt+1}")

        logger.info("Generating code from LLM")

        code = generate_code(TASK, error)

        save_code(code)

        logger.info("Executing generated Python script")

        result = run_python_file("generated_script.py")

        logger.info("Execution Result:")
        logger.info(result)

        if "Traceback" not in result:
            logger.info("Task completed successfully.")
            break

        error = result

#call the argument parsing function to get the command-line arguments when the script is executed. This allows the user to specify the task file and the number of attempts when running the script, providing flexibility in how the agent operates.
args = parse_arguments()

# Load the task from the task file (presently, task.txt) Throw an error if the file is missing or empty. This ensures we have a valid task before proceeding.
try:
    TASK = load_task(args.taskfile)
except Exception as e:
    print(f"Error loading task: {e}")
    exit(1)

# If all attempts fail, print a final message indicating that the task could not be completed successfully after multiple attempts. This provides feedback to the user and indicates that further intervention may be needed to address the task.
if __name__ == "__main__":
    main()
