from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        # double the size of the image
        self.image = surf
        # self.image.fill("white")
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()