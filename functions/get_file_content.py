import os

def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000
    abs_working = os.path.abspath(working_directory)
    file_from_working = os.path.abspath(os.path.join(abs_working, file_path))

    if os.path.commonpath([abs_working, file_from_working]) != abs_working:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_from_working):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(file_from_working, 'r') as f:
            file_contents = f.read(MAX_CHARS)
            if len(file_contents) < MAX_CHARS:
                return file_contents
            else:
                return f'{file_contents}[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f'Error: {str(e)}'