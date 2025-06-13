import os

def get_files_info(working_directory, directory=None):
    working_directory = os.path.abspath(working_directory)
    if directory not in os.listdir(working_directory):
# if str(os.path.abspath(directory)).startswith(str(os.path.abspath(working_directory))):
        return f"Error: Cannot list {directory} as it is outside the permitted working directory"
    path = os.path.join(working_directory, directory)
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'

    dir_list = os.listdir(path)
    dir_list_string = ""

    for item in dir_list:
        file_path = os.path.join(path, item)
        try:
            file_size = os.path.getsize(file_path)
        except OSError:
            return f"Error: Cannot get size for {item}"

        try:
            is_dir = os.path.isdir(file_path)
        except OSError:
            return f"Error: cannot get directory status for {item}"

        dir_list_string += f"{item}: file_size={file_size} bytes, is_dir={is_dir}\n"
    return dir_list_string
    

        