import os
import subprocess

def run_python_file(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not str(file_abs_path).startswith(str(working_directory)):
        return f"Error: Cannot execute {file_path} as it is outside the permitted working directory"
    if not os.path.isfile(file_abs_path):
        return f'Error: File "{file_path}" not found.'
    if not file_abs_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    subprocess.run([python3, file_abs_path], capture_output=True)