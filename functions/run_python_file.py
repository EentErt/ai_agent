import os
import subprocess

def run_python_file(working_directory, file_path):
    working_directory_abspath = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory_abspath, file_path))
    if not str(file_abs_path).startswith(str(working_directory_abspath)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_abs_path):
        return f'Error: File "{file_path}" not found.'
    if not file_abs_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        output = subprocess.run(["python3", file_path], capture_output=True, cwd=working_directory)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    if output is None:
        return "No output produced"
    output.stdout = f"STDOUT: {output.stdout}"
    output.stderr = f"STDERR: {output.stderr}"
    exit_code = output.returncode
    if exit_code != 0:
        return f"Process exited with code {exit_code}"
    return output
