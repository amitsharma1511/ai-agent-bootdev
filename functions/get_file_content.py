import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

        #Will be True or False
        valid_target_dir = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read the content of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the file of which content is to be read, relative to the working directory.)",
                },
            },
        },
        "required": ["file_path"]
    },
}


    #Check if the file was larger than the limit. A simple way of doing this is to try to read one more character after reading the initial chunk. If you get an empty string, you know that you already reached the end of the file. If you get a character back, then the file still had more data. In that case, add a message to the contents string to indicate that it was truncated. For example: # After reading the first MAX_CHARS...
    # if f.read(1):