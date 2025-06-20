import os
from pathlib import Path

def write_file(working_directory, file_path, content):
    
    abs_working = os.path.abspath(working_directory)
    file_from_working = os.path.abspath(os.path.join(abs_working, file_path))

    if os.path.commonpath([abs_working, file_from_working]) != abs_working:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        if not os.path.exists(file_from_working):
            new_file_path = Path(file_from_working)
            new_file_path.parent.mkdir(parents=True, exist_ok=True)
            new_file_path.touch()
        with open(file_from_working, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {str(e)}'