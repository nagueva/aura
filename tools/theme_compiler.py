# THEME COMPILER: Create /dist folder with merged scheme files
import shutil
import os
import re
from pprint import pprint

# Preparing the environment...

# Define the default theme directory relative to the location of this file
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')

# Function to clean a folder
def clean_folder(folder_path):
    print(f"Cleaning folder...")
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory and its contents
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# Function to copy all folder files to another folder
def copy_folder(src_folder, dest_folder):
    print(f"Copying files...")
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dest_path = os.path.join(dest_folder, item)
        try:
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path)
            else:
                shutil.copy2(src_path, dest_path)
        except Exception as e:
            print(f'Failed to copy {src_path} to {dest_path}. Reason: {e}')

# Function to parse a scheme file
def parse_file(file_path):
    result = {}
    current_section = None
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            section_match = re.match(r'\[(.+)\]', line)
            if section_match:
                current_section = section_match.group(1)
                result[current_section] = {}
            elif '=' in line and current_section:
                key, value = line.split('=', 1)
                result[current_section][key] = value
    return result

# Function to format a dictionary to a file
def format_to_file(data):
    lines = []
    for section, values in data.items():
        lines.append(f'[{section}]')
        for key, value in values.items():
            lines.append(f'{key}={value}')
        lines.append('')  # Add a blank line between sections
    return '\n'.join(lines)

# 3, 2, 1... go!

# Clean and copy files
clean_folder(ROOT_DIR+'dist')
copy_folder(ROOT_DIR+'theme', ROOT_DIR+'dist')

# Walk through /theme folder and merge scheme files
for root, dirs, files in os.walk(ROOT_DIR+'theme'):
    for dir_name in dirs:
        scheme_path = os.path.join(root, dir_name, 'scheme')
        if os.path.exists(scheme_path) and os.path.isdir(scheme_path):
            print(f"Theme: {dir_name}")
            scheme_files = [f for f in os.listdir(scheme_path) if f.endswith('.txt')]
            default_data = parse_file(os.path.join(scheme_path, 'default.txt'))
            for scheme_file in scheme_files:
                if scheme_file != 'default.txt':
                    print(f"Creating {scheme_file}")
                    scheme_data = parse_file(os.path.join(scheme_path, scheme_file))
                    merged_data = {**default_data, **scheme_data}
                    formatted_data = format_to_file(merged_data)
                    with open(os.path.join(ROOT_DIR+'dist', dir_name, f'scheme/{scheme_file}'), 'w') as file:
                        file.write(formatted_data)
                    print(f"✅ Done with {scheme_file}")

# ----------------------------------------------------------------
