from PIL import Image, ImageDraw, ImageOps

def add_round_border(input_image_path, output_image_path, border_radius):
    # Open the input image
    img = Image.open(input_image_path).convert("RGBA")

    # Create a mask to create rounded corners
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius=border_radius, fill=255)

    # Apply the mask to the image
    rounded_img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    rounded_img.putalpha(mask)

    # Save the output image
    rounded_img.save(output_image_path, format="PNG")

# Example usage
input_image_path = "../catalogue/Nintendo SNES-SFC/box/Addams Family, The - Pugsley's Scavenger Hunt (USA).png"
output_image_path = "./output.png"
border_radius = 50  # Adjust the radius as needed

add_round_border(input_image_path, output_image_path, border_radius)