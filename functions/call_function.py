from get_file_content import get_file_content
from get_files_info import get_files_info
from run_python_file import run_python_file
from write_file import write_file
from google import genai
from google.genai import types


def call_function(function_call_part, verbose="false"):
    if verbose == "true":
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f"Calling function: {function_call_part.name}")

    function_dict = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    function_name = function_call_part.name
    function_args = function_call_part.args

    if function_call_part.name not in function_dict:
        return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
    
    if function_name == "get_file_content":
        function_result = get_file_content("../ai_agent", function_args)
    if function_name == "get_files_info":
        function_result = get_files_info('../ai_agent', function_args)
    if function_name == "run_python_file":
        function_result = run_python_file('../ai_agent', function_args)
    if function_name == "write_file":
        function_result = write_file('../ai_agent', function_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
    
    