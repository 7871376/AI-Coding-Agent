
from agent.runtime import main

# This file is the entry point for the command-line interface (CLI) of the agent.
# It imports the main function from the runtime module and calls it when executed.

def main_cli():
    main()

# The main_cli function serves as the entry point for the CLI. It calls the main 
# function from the runtime module, which contains the core logic of the agent.

if __name__ == "__main__":
    main_cli()
