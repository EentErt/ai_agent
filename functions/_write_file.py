import os

def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not str(file_abs_path).startswith(str(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    with open(file_abs_path, 'w') as file:
        try:
            file.write(content)
        except Exception:
            file.close()
            return f'Error: Cannot write to file "{file_path}" due to an unexpected error'
    file.close()
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
