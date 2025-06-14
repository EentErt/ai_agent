from get_file_content import get_file_content
from get_files_info import fet_files_info
from run_python_file import run_pythonfile
from write_file import write_file

def call_function(function_call_part, verbose=false):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f"Calling function: {function_call_part.name}")

    function_dict = {
        "get_file_content": get_file_content,
        "get_files_info": fet_files_info,
        "run_python_file": run_pythonfile,
        "write_file": write_file
    }

    if function_call_part.name not in function_dict:
        