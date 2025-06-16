from functions._get_files_info import get_files_info
from functions._get_file_content import get_file_content
from functions._write_file import write_file
from functions._run_python_file import run_python_file

def main():
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))

main()
