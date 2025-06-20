import os

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = "."
    abs_directory = os.path.abspath(directory)
    working_abs_directory = os.path.abspath(working_directory)
    print(working_abs_directory)
    print(abs_directory)
    if not abs_directory.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'        
    
    try:
        contents = os.listdir(abs_directory)
    except Exception as e:
        return f'Error: {str(e)}'

    if not contents:
        return ""
    
    directory_info =[]

    for item in contents:
        item_path = os.path.join(abs_directory, item)
        try:
            file_size = os.path.getsize(item_path)
            is_directory = os.path.isdir(item_path)
        except Exception as e:
            return f'Error: {str(e)}'
        directory_info.append(f"- {item}: file_size={file_size} bytes, is_dir={is_directory}")

    return '\n'.join(directory_info)
