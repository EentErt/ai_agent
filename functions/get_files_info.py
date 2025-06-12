import os

def get_files_info(working_directory, directory=None):
    if directory not in working_directory:
        return f"Error: Cannot list {directory} as it is outside the permitted working directory"
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    dir_list = os.listdir(directory)
    dir_list_string = ""

    for item in dir_list:
        file_name = item
        try:
            file_size = os.path.getsize(item)
        except OSError:
            return f"Error: Cannot get size for {item}"

        try:
            is_dir = os.path.isdir(item)
        except OSError:
            return f"Error: cannot get directory status for {item}"

        dir_list_string += f"{item}: file_size={file_size} bytes, is_dir={is_dir}\n"
    

        