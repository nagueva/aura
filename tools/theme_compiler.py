from PIL import Image
import shutil
import os
import re

# Define the default theme directory relative to the location of this file
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')

# Define the resolutions
resolutions = [
    '640x480',
    '720x480',
    '720x576',
    '720x720',
    '1024x768',
    '1280x720'
]

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

def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)  # Deletes the file
        else:
            print(f"⚠️ File not found: {file_path}")
    except Exception as e:
        print(f"❌ Failed to delete {file_path}. Reason: {e}")

def convert_to_bmp(png_path, bmp_path):
    try:
        with Image.open(png_path) as img:
            img = img.convert("RGB")  # Ensure the image is in RGB mode
            img.save(bmp_path, format="BMP")
    except Exception as e:
        print(f"❌ Failed to convert {png_path} to BMP. Reason: {e}")

def resize_image(file_path, percentage):
    """
    Resize an image by a given percentage and overwrite the original file.
    :param file_path: Path to the image to resize.
    :param percentage: Percentage to resize the image (e.g., 47.22 for 47.22%).
    """
    try:
        with Image.open(file_path) as img:
            new_width = int(img.width * (percentage / 100))
            new_height = int(img.height * (percentage / 100))
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Use LANCZOS for high-quality downsampling
            img.save(file_path)  # Overwrite the original file
    except Exception as e:
        print(f"❌ Failed to resize image {file_path}. Reason: {e}")

try:
    # Get all themes
    themes_path = os.path.join(ROOT_DIR, 'theme')
    themes = [name for name in os.listdir(themes_path) if os.path.isdir(os.path.join(themes_path, name))]
    # Clean and copy files
    clean_folder(os.path.join(ROOT_DIR, 'dist'))
    copy_folder(os.path.join(ROOT_DIR, 'theme'), os.path.join(ROOT_DIR, 'dist'))
    # Refine themes
    for theme in themes:
        print(f"🧼 Refining {theme} theme...")
        theme_path = os.path.join(ROOT_DIR, 'dist', theme)
        # Create bootlogo.bmp
        print(f"    🖼️  Creating bootlogo.bmp files")
        for resolution in resolutions:
            png_path = os.path.join(theme_path, f'{resolution}/image/bootlogo.png')
            bmp_path = os.path.join(theme_path, f'{resolution}/image/bootlogo.bmp')
            convert_to_bmp(png_path, bmp_path)
            delete_file(png_path)
        # Resize preview.png
        print(f"    📐 Resizing preview.png files")
        for resolution in resolutions:
            preview_path = os.path.join(theme_path, f'{resolution}/preview.png')
            resize_image(preview_path, 47.25)

except Exception as e:
    print(f"❌ Error: {e}")
else:
    # Delete the default folders
    delete_default_folders(os.path.join(ROOT_DIR, 'dist')) 
    # Celebrate!
    print("🎉 All themes are ready!")
