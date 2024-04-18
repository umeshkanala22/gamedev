from PIL import Image
import os

# Define the directory containing the images
image_directory = '/home/silversage22/Desktop/sem4/COP290/game/graphics/craftpix-net-481532-free-medieval-tileset-pixel-art-pack/PNG/Tiles'

# Define the desired size for the images (width, height)
desired_size = (32, 32)  # Example size (300 x 300 pixels)

# Iterate through each image in the directory
for filename in os.listdir(image_directory):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
        # Open the image
        image_path = os.path.join(image_directory, filename)
        image = Image.open(image_path)

        # Resize the image
        resized_image = image.resize(desired_size)

        # Save the resized image (optionally, you can save in a new directory)
        resized_image_path = os.path.join(image_directory, 'resized_' + filename)
        resized_image.save(resized_image_path)

        print(f'Resized {filename} and saved as {resized_image_path}')
