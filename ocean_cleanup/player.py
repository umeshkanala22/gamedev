import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
import random
import time

class Net(pygame.sprite.Sprite):
    def __init__(self, x, y, net_group):
        super().__init__(net_group)

        # Load net image (PNG format)
        self.image = pygame.image.load('assets/player/net2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (95, 30))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.status = "active"

        # Set initial position for net (centered at bottom of submarine)
        self.rect.centerx = x
        self.rect.bottom = y

        self.speed = 5

    def update(self):
        # Move net upwards
        self.rect.y -= self.speed

        # Remove net if it goes off screen
        if self.rect.top < 0.3*SCREEN_HEIGHT-10:
            self.status = "missed"
            self.speed = 0

    def settle_down(self):
        # Settle down the net at the bottom of the screen
        self.rect.y += self.speed
        if self.rect.bottom > SCREEN_HEIGHT:
            self.status = "settled"
            self.speed = 0

    def draw(self, screen):
        # Draw net
        screen.blit(self.image, self.rect)

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__()

        self.image = pygame.image.load('assets/player/spaceship.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()

        self.rect.centerx = -60
        self.rect.bottom = SCREEN_HEIGHT * 0.15

        self.speed = 4
        self.light_range = 200  # Range of light in pixels

        self.all_sprites = all_sprites

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep ship within screen boundaries
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

class Bubble(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()

        # Load bubble image (PNG format)
        self.image = pygame.image.load('assets/player/bubble1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Set initial position for bubble (centered at bottom of submarine)
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 2

    def update(self):
        # Move bubble upwards
        self.rect.y -= self.speed

        # Remove bubble if it goes off screen
        if self.rect.bottom < 0.3*SCREEN_HEIGHT:
            self.kill()

    def draw(self, screen):
        # Draw bubble
        screen.blit(self.image, self.rect)

class Submarine(pygame.sprite.Sprite):
    def __init__(self, all_sprites, net_group, bubble_group):
        super().__init__(all_sprites)

        # Load submarine image (PNG format)
        self.image = pygame.image.load('assets/player/submarine2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 60))
        self.rect = self.image.get_rect()

        # Create a mask for collision detection
        self.mask = pygame.mask.from_surface(self.image)

        # Set initial position for submarine
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10

        self.speed = 5
        self.net_group = net_group
        self.all_sprites = all_sprites
        self.bubble_group = bubble_group

    def fire_net(self):
        # Create a net sprite
        net = Net(self.rect.centerx, self.rect.centery, self.net_group)
        self.net_group.add(net)
        self.all_sprites.add(net)


    def release_bubble(self):
        # Create a bubble sprite
        bubble_size = random.randint(10, 30)
        bubble = Bubble(self.rect.centerx, self.rect.centery, bubble_size)
        self.all_sprites.add(bubble)
        self.bubble_group.add(bubble)
    

    def update(self):
        keys = pygame.key.get_pressed()
        # move submarine left or right with arrow keys or A and D keys
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # Keep submarine within screen boundaries
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(SCREEN_HEIGHT * 0.6, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

    def draw(self, screen):
        # Draw submarine
        screen.blit(self.image, self.rect)