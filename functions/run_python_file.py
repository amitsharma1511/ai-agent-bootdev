import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))

        #Will be True or False
        valid_target_dir = os.path.commonpath([working_directory_abs, absolute_file_path]) == working_directory_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if absolute_file_path[-3:] != ".py":
            # print("FILE ENDING: ", absolute_file_path[-3:])
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_file_path]

        if args:
            command.extend(args)
        
        subp = subprocess.run(command, cwd=working_directory_abs, capture_output=True, text=True, timeout=30)

        if subp.returncode != 0:
            print(f"Process exited with code {subp.returncode}")

        if (not subp.stdout) and (not subp.stderr):
            print("No output produced")

        if subp.stdout:
            return f"STDOUT: {subp.stdout}"
        else:
            return f"STDERR: {subp.stderr}"
        
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a python file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the file of which the python code to be run, relative to the working directory.)",
                },
                "args": {
                    "type": "array",
                    "description": "Optional list of string arguments"
                },
            },
            "required": ["file_path"]
        },
    },
}