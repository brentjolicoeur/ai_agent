import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

model = 'gemini-2.0-flash-001'
if len(sys.argv) < 2:
    print("Prompt required as command line argument")
    sys.exit(1)
prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
response = client.models.generate_content(model=model, contents=prompt)

print(response.text)
if '--verbose' in sys.argv:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")