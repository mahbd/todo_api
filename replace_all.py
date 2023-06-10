import os
from os.path import join, abspath
import re


def replace_word_in_files(project_name):
    template_name = 'todo_api'
    current_project = os.getcwd()
    for root, dirs, files in os.walk(current_project):
        # skip .git, .idea, .vscode, venv, __pycache__, static
        if '.git' in root or '.idea' in root or '.vscode' in root or 'venv' in root or '__pycache__' in root or 'static' in root:
            continue
        for file in files:
            file_path = join(root, file)
            new_file_path = join(root.replace(template_name, project_name), file)
            with open(file_path, 'r') as f:
                try:
                    content = f.read()
                except UnicodeDecodeError:
                    print(f"UnicodeDecodeError: '{file_path}' file could not be read")
                    continue

            new_content = re.sub(template_name, project_name, content)
            # create directory if not exists
            if not os.path.exists(os.path.dirname(new_file_path)):
                os.makedirs(os.path.dirname(new_file_path))
            with open(new_file_path, 'w+') as f:
                f.write(new_content)

    print(
        f"All occurrences of '{template_name}' have been replaced with '{project_name}' in all files and folder names inside {current_project}")


# Take project name from user
project_name = input("Enter your project name: ")
replace_word_in_files(project_name)
