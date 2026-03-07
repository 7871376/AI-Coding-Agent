# AI Coding Agent

A simple autonomous Python agent that:
- Reads a coding task
- Generates Python code using OpenAI
- Executes the code
- Fixes errors automatically

## Example
task.txt reads, "Write Python code that generates a random password with 16-characters. Avoid inclusion of the capital letters I and O, and lowercase l, because they can be confused with digits 0 and 1. "

Returns:
2026-03-06 22:09:01,075 | INFO | Attempt 1
2026-03-06 22:09:01,075 | INFO | Generating code from LLM
2026-03-06 22:09:04,283 | INFO | HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-03-06 22:09:04,293 | INFO | Executing generated Python script
2026-03-06 22:09:04,336 | INFO | Execution Result:
2026-03-06 22:09:04,336 | INFO | x$k2(UXE3FiyFF5]

## Requires
A .env file that contains your Open AI License Key. Use format OPENAI_API_KEY={your key here}

## Run

python agent.py task.txt

Where task.txt contains the prompt you want run.
