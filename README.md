# AI Coding Agent

A simple autonomous Python agent that:
- Reads a coding task
- Generates Python code using OpenAI
- Executes the code
- Any errors are researched on the Web
- Errors are corrected and tasks are reattempted automatically

## Example
task.txt reads, "Write Python code that generates a random password with 16-characters. Avoid inclusion of the capital letters I and O, and lowercase l, because they can be confused with digits 0 and 1. "

Returns:
Attempt 1
Generating code from LLM...
HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Executing generated Python script...
Execution Result:
6nn99cQX,j]tSFda

Task completed successfully.

## Requires
A .env file that contains your OpenAI API Key. Use format OPENAI_API_KEY={your key here}

## Run

python agent.py task.txt --attempts n

Where task.txt contains the prompt you want run, and n is the number of times you want the prompt re-attempted.
