import os

def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not str(file_abs_path).startswith(str(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(file_abs_path, 'r') as file:
            content = file.read()
    except Exception:
        file.close()
        return f'Error: Cannot read file "{file_path}" due to an unexpected error'
    file.close()
    if len(content) > 10000:
        content = content[:10000]
        content += f'\n[...File "{file_path}" truncated at 10000 characters]'
    return content