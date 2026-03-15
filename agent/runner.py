import io
import contextlib
import traceback

# this version of the runner is used to run python code in a file, 
# and return the output as a string. It also captures any exceptions 
# and returns the traceback as a string. This is useful for running 
# code that may have errors, and we want to see the error message 
# instead of crashing the program. Most importantly, this runner can
# execute from the runtime of an .exe.  Called from runtime.execute_task().

def run_python_file(file_name):

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            code = f.read()

        output_buffer = io.StringIO()

        exec_globals = {}

        with contextlib.redirect_stdout(output_buffer):
            exec(code, exec_globals)

        return output_buffer.getvalue()

    except Exception:
        return traceback.format_exc()