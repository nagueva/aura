import shutil
import os
import re

# Define the default theme directory relative to the location of this file
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')

# Function to clean a folder
def clean_folder(folder_path):
    folder_name = os.path.basename(folder_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"    🟢 Created /{folder_name} folder!")
    else:
        print(f"🗑️ Cleaning /{folder_name} folder...")
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove the file or link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove the directory and its contents
            except Exception as e:
                print(f'❌ Failed to delete {file_path}. Reason: {e}')
        print(f"    🟢 /dist is now empty!")

# Function to delete the default folders
def delete_default_folders(dist_path):
    for root, dirs, files in os.walk(dist_path):
        for dir_name in dirs:
            if dir_name == 'default':
                default_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(default_path)
                    print(f"🗑️ Deleted default folder for {os.path.basename(root)}.")
                except Exception as e:
                    print(f'❌ Failed to delete {default_path}. Reason: {e}')

# Function to copy all folder files to another folder
def copy_folder(src_folder, dest_folder):
    print(f"👯 Copying theme files...")
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
            print(f'❌ Failed to copy {src_path} to {dest_path}. Reason: {e}')
    print(f"    🟢 Theme files in place!")

# Function to parse a scheme file
def parse_file(file_path):
    result = {}
    current_section = None
    try:
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
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except IOError as e:
        print(f"❌ Error reading file {file_path}: {e}")
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
clean_folder(os.path.join(ROOT_DIR, 'dist'))
copy_folder(os.path.join(ROOT_DIR, 'theme'), os.path.join(ROOT_DIR, 'dist'))

try:
    # Walk through /theme folder and merge scheme files
    for root, dirs, files in os.walk(os.path.join(ROOT_DIR, 'theme')):
        for dir_name in dirs:
            scheme_path = os.path.join(root, dir_name, 'scheme')
            # Check if the scheme folder exists and is a directory
            if os.path.exists(scheme_path) and os.path.isdir(scheme_path):
                # Skip the default scheme
                if dir_name == 'default':
                    continue
                theme_name = os.path.basename(root)
                print(f"🚧 {theme_name} ({dir_name}) starting...")
                # Get all .txt files in the scheme folder
                scheme_files = [f for f in os.listdir(scheme_path) if f.endswith('.txt')]
                # Parse the default.txt file
                default_scheme = os.path.join(ROOT_DIR, 'theme', theme_name, 'default/scheme/default.txt')
                default_data = parse_file(default_scheme)
                # Go over the .txt files and merge them with the default data
                for scheme_file in scheme_files:
                    print(f"    🟡 Creating {scheme_file}")
                    scheme_data = parse_file(os.path.join(scheme_path, scheme_file))
                    merged_data = default_data.copy()
                    for key, value in scheme_data.items():
                        if key in merged_data:
                            if isinstance(merged_data[key], dict) and isinstance(value, dict):
                                merged_data[key].update(value)
                            else:
                                merged_data[key] = value
                        else:
                            merged_data[key] = value
                    # Format the merged data and save it to a file
                    formatted_data = format_to_file(merged_data)
                    output_path = os.path.join(ROOT_DIR, 'dist', theme_name, dir_name, 'scheme', scheme_file)
                    # Create the output folder if it doesn't exist
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    # Create the output file
                    try:
                        with open(output_path, 'w') as file:
                            file.write(formatted_data)
                        print(f"    🟢 Finished {scheme_file}!")
                    except IOError as e:
                        print(f"❌ Error writing file {output_path}: {e}")
                    print(f"✅ {theme_name} ({dir_name}) is ready!")
except Exception as e:
    print(f"❌ Error: {e}")
else:
    # Delete the default folders
    delete_default_folders(os.path.join(ROOT_DIR, 'dist')) 
    # Celebrate!
    print("🎉 All themes are ready!")
