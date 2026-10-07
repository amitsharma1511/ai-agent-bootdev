import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))

        #Will be True or False
        valid_target_dir = os.path.commonpath([working_directory_abs, target_file_path]) == working_directory_abs

        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
        
        with open(target_file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write content in a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of the file where the content is to be written, relative to the working directory)",
                },
                "content": {
                    "type": "string",
                    "description": "The content to be written to the file"
                },
            },
            "required": ["file_path", "content"]
        },
    },
}