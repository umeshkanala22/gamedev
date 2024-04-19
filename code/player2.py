import pygame
from support import *
from settings import *
from pygame.math import Vector2 as vector
from os.path import join

class Player2(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, death_sprites):
        super().__init__(groups)
        self.import_assets()
        self.status = 'down'
        self.frame_index = 0
        self.life=3
        self.image = self.animations[self.status][self.frame_index]
        self.levelchanger=False
        self.levelchangedto='level1'
		

        #rects

        self.rect = self.image.get_frect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.old_rect = self.rect.copy()
        self.mask = pygame.mask.from_surface(self.image)
        self.z=LAYERS2['constantterrrain']

        self.living = True

        # movement
        self.direction = 0
        # self.speed = 200
        # self.gravity = 1300

        self.counter = 0
        self.vel_y = 0
        self.jumped = False
        # self.jump_height = 800

        # collision
        self.collision_sprites = collision_sprites
        self.death_sprites =death_sprites
        # self.on_surface = {'floor': False, 'left': False, 'right': False}

    def import_assets(self):
        self.animations = {'up': [],'down': [],'left': [],'right': []}
        for animation in self.animations.keys():
            full_path = join(join('..', 'graphics', 'player'),animation)
            self.animations[animation] = import_folder(full_path)
    def animate(self,dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]


    # def input(self):
    #     keys = pygame.key.get_pressed()
    #     input_vector = vector(0,0)
    #     if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    #         input_vector.x += 1
    #         self.status = 'right'
    #     if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    #         input_vector.x -= 1
    #         self.status = 'left'
    #     self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

    #     if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
    #         self.jump = True
    #         self.status = 'down'
    def get_status(self):
        if self.direction.x == 1:
            return 'right'
        elif self.direction.x == -1:
            return 'left'
        else:
            return 'down'
		
		# idle
	
    # def move(self, dt):
    #     # horizontal
    #     self.rect.x += self.direction.x * self.speed * dt
    #     self.collision('horizontal')

    #     # vertical
    #     if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])):
    #         self.direction.y = 0
    #         self.rect.y += self.gravity/10 * dt
    #     else:
    #         self.direction.y += self.gravity / 2 * dt
    #         self.rect.y += self.direction.y * dt
    #         self.direction.y += self.gravity / 2 * dt
    #     self.collision('vertical')

    #     # jump
    #     if self.jump:
    #         if self.on_surface['floor']:
    #             self.direction.y = -self.jump_height
    #         self.jump = False

    # def check_contact(self):
    #     floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
    #     right_rect = pygame.Rect(self.rect.topright + vector(0, self.rect.height/4), (2, self.rect.height/2))
    #     left_rect = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height/4), (2, self.rect.height/2))
    #     collide_rects = [sprite.rect for sprite in self.collision_sprites]
        
    #     # collisions
    #     self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 else False
    #     self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
    #     self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False

    # def collision(self, axis):
    #     for sprite in self.collision_sprites:
    #         if pygame.sprite.collide_rect(self, sprite):
    #             if axis == 'horizontal':
    #                 # left
    #                 if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
    #                     self.rect.left = sprite.rect.right 
    #                 # right
    #                 if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
    #                     self.rect.right = sprite.rect.left
    #             else: # vertical
    #                 # top
    #                 if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
    #                     self.rect.top = sprite.rect.bottom
    #                 # bottom
    #                 if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
    #                     self.rect.bottom = sprite.rect.top
    #                 self.direction.y = 0

    def is_dead(self):
        return not self.living
    
    def update(self, dt):
        self.animate(dt)

        dx = 0
        dy = 0
        walk_cooldown = 5
        
        key = pygame.key.get_pressed()
        if (key[pygame.K_SPACE] or key[pygame.K_w]) and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
        # if key[pygame.K_SPACE] == False:
        #     self.jumped = False
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            dx -= 3
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            dx += 3
            self.counter += 1
            self.direction = 1
        if key[pygame.K_RIGHT] == False and key[pygame.K_LEFT] == False:
            self.counter = 0
            self.frame_index = 0
            if self.direction == 1:
                self.status = 'right'
            if self.direction == -1:
                self.status = 'left'

        

        # add gravity
        self.vel_y += 0.4
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check for collision
        for tile in self.collision_sprites:
            # check collision in x
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check collision in y
            if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # print('collided')
                # check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile.rect.bottom - self.rect.top
                    self.vel_y = 0
                # check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    if tile in self.death_sprites:
                        self.living = False
                    # print('collided')
                    self.jumped = False
                    dy = tile.rect.top - self.rect.bottom
                    self.vel_y = 0


        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        # if self.rect.bottom > SCREEN_HEIGHT:    
        #     self.rect.bottom = SCREEN_HEIGHT
        #     dy = 0

        # screen.blit(self.image, (self.rect.x, self.rect.y))
