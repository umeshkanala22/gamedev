import pygame

if __name__ == "__main__":
    image_path = "industry_fix/assets/alien_green/"
    images = ["green__0006_walk_1.png", "green__0007_walk_2.png", "green__0008_walk_3.png", "green__0009_walk_4.png", "green__0010_walk_5.png", "green__0011_walk_6.png"]
    # flip the images to get the right walk states and save them 
    for image in images:
        img = pygame.image.load(image_path + image)
        img = pygame.transform.flip(img, True, False)
        pygame.image.save(img, image_path + "flip_" + image)