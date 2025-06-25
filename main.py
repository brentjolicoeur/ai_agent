import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

model_name = 'gemini-2.0-flash-001'

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
Format the result in a numbered list when appropriate.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
schema_get_file_contents = types.FunctionDeclaration(
    name="get_file_content",
    description="""Reads contents of a specified file truncating it at a maximum of 10000 characters,
      constrained to the working directory. Returns an appropriate error if the specified file does not exist.""",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory containing the file, relative to the working directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file being read."
            )
        }
    )
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="""Executes a specified python file constrained to the working directory.
        Returns stdout and stderr messages and reports any nonstandard exit codes.""",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory containing the file, relative to the working directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to be executed."
            )
        }
    )
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="""Writes specified content to a specified file, constrained to the working directory.
        Creates the necessary path to the file as well as the file if it does not already exist.
        Returns a successful completion message containing the length of the content written.""",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory containing the file, relative to the working directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to be written.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the specified file."
            )
        }
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_contents,
        schema_run_python_file,
        schema_write_file,
    ]
)

if len(sys.argv) < 2:
    print("Prompt required as command line argument")
    sys.exit(1)
prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
iterations = 1
while iterations <= 20:
    response = client.models.generate_content(
        model=model_name, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt)
    )
    function_calls = response.function_calls
    call_result = None

    for candidate in response.candidates:
        messages.append(candidate.content)
    if response.function_calls:
        for call in function_calls:
            call_result = call_function(call, verbose=('--verbose' in sys.argv))
            
            if not call_result.parts[0].function_response.response:
                raise Exception("Function call failed")
            
            if '--verbose' in sys.argv:
                print(f"-> {call_result.parts[0].function_response.response}")

            messages.append(call_result)
        iterations += 1
    else:
        print(response.text)
        if '--verbose' in sys.argv:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        break