import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Net(pygame.sprite.Sprite):
    def __init__(self, x, y, net_group):
        super().__init__(net_group)

        # Load net image (PNG format)
        self.image = pygame.image.load('player/net.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()

        # Set initial position for net (centered at bottom of boat)
        self.rect.centerx = x
        self.rect.bottom = y

        self.speed = 10


    def update(self):
        # Move net upwards
        self.rect.y -= self.speed

        # Remove net if it goes off screen
        if self.rect.bottom < 0:
            self.kill()

    def draw(self, screen):
        # Draw net
        screen.blit(self.image, self.rect)

class Ship(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__(all_sprites)

        # Load ship image (PNG format)
        self.image = pygame.image.load('player/ship.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 60))
        self.rect = self.image.get_rect()

        # Set initial position for ship (top of water i.e. 20% of screen height)
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT * 0.2

        self.speed = 5
        self.all_sprites = all_sprites

    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep ship within screen boundaries
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

    def draw(self, screen):
        # Draw ship
        screen.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, net_group):
        super().__init__(all_sprites)

        # Load submarine image (PNG format)
        self.image = pygame.image.load('player/submarine.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 60))
        self.rect = self.image.get_rect()

        # Set initial position for submarine
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10

        self.speed = 5
        self.net_group = net_group
        self.all_sprites = all_sprites

    def fire_net(self):
        # Create a net sprite
        net = Net(self.rect.centerx, self.rect.top+10, self.net_group)
        self.net_group.add(net)
        self.all_sprites.add(net)



    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep submarine within screen boundaries
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

    def draw(self, screen):
        # Draw submarine
        screen.blit(self.image, self.rect)