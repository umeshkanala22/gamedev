import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Trash(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load random trash image
        trash_images = ['assets/trash/bottle.png', 'assets/trash/soda.png', 'assets/trash/water_bottle.png']  # Replace with actual image filenames
        self.image = pygame.image.load(random.choice(trash_images)).convert_alpha()

        # Scale the image (optional)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randrange(1, 2)

        self.status = "active"

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom == SCREEN_HEIGHT:
            # self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            # self.rect.y = random.randrange(self.x, self.y)
            self.speed = 0
