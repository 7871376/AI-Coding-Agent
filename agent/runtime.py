DEBUG_MODE = False

# General import statements and setup
import argparse
import code
import logging
import os
from unittest import result

# Import specific methoods and classes from external libraries
from dotenv import load_dotenv
from openai import OpenAI
from agent.runner import run_python_file
from agent.search_tool import search_web
from agent.task import load_task

# Set up logging configuration to provide informative messages about the execution of the script.
# This includes timestamps, log levels, and the message content, which can help with debugging 
# and understanding the flow of the program.
#
# full format: "%(asctime)s | %(levelname)s | %(message)s"
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format="%(message)s",
     handlers=[
        logging.FileHandler("agent.log"),
        logging.StreamHandler()
    ]
)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

if DEBUG_MODE:
    logger.debug(f"DEBUG: AGENT STARTED")

# initialize the OpenAI client and load environment variables from a .env file. 
# This allows us to securely manage API keys and other configuration settings needed 
# for the OpenAI API to function properly. 
# 
# The client will be used to interact with the OpenAI API for generating code based on the specified task.
load_dotenv()
client = OpenAI()

# Function to parse command-line arguments. This allows users to specify the task file 
# and the number of attempts when running the script. The default number of attempts 
# is set to 5, but it can be customized by the user.
def parse_arguments():

    parser = argparse.ArgumentParser(
        description="AI Coding Agent that generates and executes Python code."
    )

    # sets a default file for the coding task if the user fails to provide one. 
    # This allows the script to run with a predefined task without requiring additional input, 
    # while still giving users the flexibility to specify their own task file if desired.
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
    
    # set the prompt for the language model, including the task and any previous error if applicable. 
    # This allows the model to generate code that addresses the task while also correcting 
    # any mistakes from previous attempts.
    # 
    # called from execute_task, which manages the overall process of generating and executing code, 
    # including handling errors and retries.

    # the prompt goes for the next few lines.
    prompt = f"""
You are an AI coding assistant.

You can:
1. Write Python code
2. Search the web for documentation if needed

Task:
{task}

Previous error:
{previous_error}

Return ONLY valid executable Python code.
Do not include explanations.
Do not include markdown.
Do not include backticks.
Do not include comments outside code.
"""
    #debug only
    if DEBUG_MODE:
        logger.debug(f"DEBUG: Prompt for code generation: {prompt}")


     # Call the OpenAI API to generate code based on the prompt. 
     # The model used is "gpt-4o-mini", which is a smaller version of GPT-4 optimized for code generation. 
     # The response is expected to contain the generated Python code.
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    

    # debug only
    if DEBUG_MODE:
        logger.debug(f"DEBUG: API Response: {response}")

    # Extract the generated code from the API response. The code is expected to be in the content 
    # of the first choice returned by the API. This code will then be processed to remove 
    # any markdown formatting before being saved and executed.
    code = extract_code(response.choices[0].message.content)

    # Remove markdown code fences if present
    code = code.replace("```python", "").replace("```", "").strip()

    return code

def extract_code(text: str) -> str:
    # The function is designed to extract Python code from a given text input. 
    # It checks for the presence of markdown code fences (```), and if found, 
    # splits the text accordingly. If the code is specified as Python (```python),
    # it extracts the code following that marker. If no specific language is 
    # indicated, it simply returns the content between the first set of code fences. 
    # If no code fences are present, it returns the original text. 
    # 
    # This function helps ensure that only valid executable Python code is extracted for execution.

    if "```" in text:
        parts = text.split("```")
        for p in parts:
            if "python" in p.lower():
                return p.split("\n", 1)[1]
        return parts[1]
    return text


# Save the generated code to a file named "generated_script.py". This allows us to execute the code 
# in subsequent steps and also keeps a record of the generated code for debugging or review purposes.
def save_code(code):
    with open("generated_script.py", "w") as f:
        f.write(code)

# Execute the generated code and implement retry logic. If the code execution results in an error, 
# the error message is captured and used to generate new code in the next attempt. The process 
# continues until the code executes successfully or the maximum number of attempts is reached, at 
# which point a RuntimeError is raised.
def execute_task(task, attempts):
     
    error = None

    for attempt in range(attempts):

        logger.info(f"INFO: Attempt {attempt+1}")
        code = generate_code(task, error)
        save_code(code)
        result = run_python_file("generated_script.py")

        if "Traceback" not in result:
            return result

        search_results = search_web(result)
        error = result + "\n\nRelevant documentation:\n" + search_results

    raise RuntimeError("Task failed after maximum attempts")


def main():
    
    # call the argument parsing function to get the command-line arguments when the script is executed. 
    # This allows the user to specify the task file and the number of attempts when running the script,
    # providing flexibility in how the agent operates.
    args = parse_arguments()

    # Load the task from the task file (presently, task.txt) Throw an error if the file is missing or empty. 
    # This ensures we have a valid task before proceeding.
    try:
        TASK = load_task(args.taskfile)
    except Exception as e:
        logger.error(f"ERROR: Error loading task: {e}")
        exit(1)

    # Execute the task with the specified number of attempts. If the task is completed successfully,
    # the result is logged. If all attempts fail, an error message is logged indicating that the task
    # could not be completed.
    try:
        result = execute_task(TASK, args.attempts)
        logger.info(result)

    except RuntimeError:
        logger.error("ERROR: Task could not be completed.")


# If all attempts fail, print a final message indicating that the task could not be completed 
# successfully after multiple attempts. This provides feedback to the user and indicates that 
# further intervention may be needed to address the task.
if __name__ == "__main__":
    main()
