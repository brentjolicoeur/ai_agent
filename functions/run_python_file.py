import os, subprocess

def run_python_file(working_directory, file_path):

    abs_working = os.path.abspath(working_directory)
    file_from_working = os.path.abspath(os.path.join(abs_working, file_path))

    if os.path.commonpath([abs_working, file_from_working]) != abs_working:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(file_from_working):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            ['python3', file_from_working],
              cwd=abs_working, 
              timeout=30, 
              capture_output=True, 
              text=True
        )
        if not result.stderr and not result.stdout:
            return "No output produced."
        output = []
        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output.append(f"STDERR: {result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        
        return '\n'.join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"