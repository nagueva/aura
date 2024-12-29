import os
from dotenv import load_dotenv
from PIL import Image, ImageFilter, ImageDraw, ImageOps
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

# Constants
TARGET_WIDTH = 640
TARGET_HEIGHT = 480
BLUR_RADIUS = 4
BORDER_RADIUS = 4
INPUT_FOLDER = os.getenv('INPUT_FOLDER')
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER')

# Function to open and resize images
def open_and_resize_image(image_path, target_width, target_height, blur_radius=None):
    try:
        with Image.open(image_path).convert("RGBA") as img:
            resize_ratio = max(target_width / img.width, target_height / img.height)
            new_size = (int(img.width * resize_ratio), int(img.height * resize_ratio))
            img.thumbnail(new_size)
            if blur_radius:
                img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            return img
    except IOError as e:
        logging.error(f"Error opening image {image_path}: {e}")
        return None

# Function to add a round border to an image
def add_round_border(img, border_radius):
    # Create a high-resolution mask
    scale_factor = 4  # Increase this factor to improve resolution
    high_res_size = (img.size[0] * scale_factor, img.size[1] * scale_factor)
    mask = Image.new("L", high_res_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), high_res_size], radius=border_radius * scale_factor, fill=255)

    # Resize the mask to the original image size
    mask = mask.resize(img.size, Image.LANCZOS)

    # Apply the mask to the image
    rounded_img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    rounded_img.putalpha(mask)

    return rounded_img

# Function to create the thumbnail
def create_thumbnail(item, folder_path):
    logging.info("🏞️  Creating thumbnail")
    # Extract the filename without the extension
    game, ext = os.path.splitext(item)
    # Skip .dat and .DS_Store files
    if ext == ".dat" or item == ".DS_Store":
        return
    # Image paths
    paths = {
        "box2dfront": os.path.join(folder_path, "media", "box2dfront", f"{game}.png"),
        "screenshot": os.path.join(folder_path, "media", "screenshot", f"{game}.png"),
        # "screenshottitle": os.path.join(folder_path, "media", "screenshottitle", f"{game}.png"),
        "wheel": os.path.join(folder_path, "media", "wheel", f"{game}.png")
    }

    # Open and prepare images
    background = open_and_resize_image(paths["screenshot"], TARGET_WIDTH, TARGET_HEIGHT, BLUR_RADIUS)
    if background.height > 480:
        background_posy = (480 - background.height) // 2
    else:
        background_posy = 0
    if background.width > 640:
        background_posx = (640 - background.width) // 2
    else:
        background_posx = 0

    screenshot = open_and_resize_image(paths["screenshot"], 236, 128)
    if screenshot.height > 128:
        resize_ratio = 128 / screenshot.height
        new_width = int(screenshot.width * resize_ratio)
        screenshot = screenshot.resize((new_width, 128))
    screenshot = add_round_border(screenshot, BORDER_RADIUS)

    box2dfront = open_and_resize_image(paths["box2dfront"], 236, 248)
    # Adjust height of the box2dfront image if it's too big
    if box2dfront.height > 248:
        resize_ratio = 248 / box2dfront.height
        new_width = int(box2dfront.width * resize_ratio)
        box2dfront = box2dfront.resize((new_width, 248))
        box2dfront_posy = 48
    elif box2dfront.width > 236:
        resize_ratio = 236 / box2dfront.width
        new_height = int(box2dfront.height * resize_ratio)
        box2dfront = box2dfront.resize((236, new_height))
        box2dfront_posy = (296 - box2dfront.height)
    else:
        box2dfront_posy = (296 - box2dfront.height)
    box2dfront = add_round_border(box2dfront, BORDER_RADIUS)

    # Create the thumbnail
    with Image.open("./gradient.png") as gradient:
        # Create a new image for the thumbnail
        new_thumbnail = Image.new('RGB', (640, 480))
        # Paste images into the thumbnail
        new_thumbnail.paste(background, (background_posx, background_posy))
        new_thumbnail.paste(gradient, (0, 0), mask=gradient)
        new_thumbnail.paste(box2dfront, (396, box2dfront_posy), mask=box2dfront)
        new_thumbnail.paste(screenshot, (396, 304), mask=screenshot)
        # new_thumbnail.paste(screenshottitle, (384, 342))
        # Save the thumbnail
        new_thumbnail.save(f"{OUTPUT_FOLDER}/{game}.png")
    # Log the process
    logging.info(f"✅ \033[32mDone!\033[0m {index}: {item}")

# Check files in the folder
try:
    items = os.listdir(INPUT_FOLDER)
    for index, item in enumerate(items):
        # if index >= 11:
        #     break
        item_path = os.path.join(INPUT_FOLDER, item)
        if os.path.isfile(item_path):
            logging.info(f"\033[1;33m🏁 Starting {index}: {item}\033[0m")
            create_thumbnail(item, INPUT_FOLDER)

except FileNotFoundError:
    logging.error(f"{item} does not exist.")

except NotADirectoryError:
    logging.error(f"The path {INPUT_FOLDER} is not a directory.")

except PermissionError:
    logging.error(f"Permission denied to access {INPUT_FOLDER}.")
