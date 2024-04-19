import os
from PIL import Image

images_path = os.path.join('graphics', 'player')
# there are 4 animations: up, down, left, right
for animation in ['up', 'down', 'left', 'right']:
    animation_path = os.path.join(images_path, animation)
    for image in os.listdir(animation_path):
        image_path = os.path.join(animation_path, image)
        # open image
        img = Image.open(image_path)
        # crop image to 58px * 66px (from center)
        img = img.crop((img.width//2 - 29, img.height//2 - 33, img.width//2 + 29, img.height//2 + 33))
        img.save(image_path)
        