import os
from dotenv import load_dotenv
import logging
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO)
load_dotenv()

# Constants
INPUT_FOLDER = os.getenv('INPUT_FOLDER')
OUTPUT_FOLDER = os.path.join(os.getenv('OUTPUT_FOLDER'), 'text')

# Ensure the output folder exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Get the first .dat file in the media folder and parse it
database_folder = os.path.join(INPUT_FOLDER, 'media')
database_path = None
if os.path.exists(database_folder):
    for file_name in os.listdir(database_folder):
        if file_name.endswith('.dat'):
            database_path = os.path.join(database_folder, file_name)
            break
database = ET.parse(database_path).getroot()

# Check files in the folder
try:
    items = os.listdir(INPUT_FOLDER)
    for index, item in enumerate(items):
        if item in ['.DS_Store', '.disks', 'media']:
            continue
        # if index >= 11:
        #     break
        logging.info(f"\033[1;33m🏁 Starting {index}: {item}\033[0m")
        # Find the game in the database
        rom_node = database.findall(f".//rom[@name=\"{item}\"]")
        game_node = database.findall(f".//rom").index(rom_node[0])
        game = database.findall(".//game")[game_node]
        item_name = game.get('name')
        year_element = game.find('year')
        item_year = year_element.text if year_element is not None else ''
        item_manufacturer = game.find('manufacturer').text
        item_description = game.find('description').text if game.find('description') is not None else ''

        # Create a text file with the game information
        filename, ext = os.path.splitext(item)
        output_file_path = os.path.join(OUTPUT_FOLDER, f"../text/{filename}.txt")
        with open(output_file_path, 'w') as output_file:
            output_file.write(f"{item_name} ")
            if item_year:
                output_file.write(f"({item_year})")
            output_file.write(f"{item_manufacturer}\n")
            if item_description:
                output_file.write(f"___\n\n{item_description}\n")
        logging.info(f"\033[1;32m✅ Done! Created text file.\033[0m")
        
except FileNotFoundError:
    logging.error(f"{INPUT_FOLDER} does not exist.")

except NotADirectoryError:
    logging.error(f"The path {INPUT_FOLDER} is not a directory.")

except PermissionError:
    logging.error(f"Permission denied to access {INPUT_FOLDER}.")
