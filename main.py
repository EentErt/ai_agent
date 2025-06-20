import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.call_function import call_function

def main():

    system_prompt ="""
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
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

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Reads the contents of the specified file as a string, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file": types.Schema(
                    type=types.Type.STRING,
                    description="The file to get the content from, relative to the working directory.",
                ),
            },
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes the specified python file with optional arguments, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file": types.Schema(
                    type=types.Type.STRING,
                    description="The file to run, relative to the working directory",
                ),
            },
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes or overwrites the specified file, if the file does not exist, creates it, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file": types.Schema(
                    type=types.Type.STRING,
                    description="The file to write, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file."
                )
            },
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("Input requires a prompt as an argument.")
        sys.exit(1)

    loops = 0
    messages = [types.Content(role="user", parts=[types.Part(text=sys.argv[1])])]  
    while loops < 20:

        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        if len(sys.argv) > 2:
            if sys.argv[2] == "--verbose":
                print(f"User prompt: {sys.argv[1]}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        if response.function_calls is not None:
            for item in response.function_calls:
                function_call_result = call_function(item, verbose="true")
                #print(f"-> {function_call_result.parts[0].function_response.response}")
                messages.append(function_call_result)
        else:
            print(response.text)
            break
        if function_call_result.parts[0].function_response.response is None:
            raise Exception("Function call did not return a response.")
        

        loops += 1
        if loops >= 20:
            print("Maximum number of requests reached, exiting.")
            print(response.text)


main()

