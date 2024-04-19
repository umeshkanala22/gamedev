import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, z = LAYERS['road']):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
class Interactable(Generic):
	def __init__(self, pos, surf, groups,levelchanger):
		super().__init__(pos,surf,groups)
		self.l=levelchanger
		self.hitbox = self.rect.copy().inflate(-20,-self.rect.height* 0.5)
class nonInteractable(Generic):
	def __init__(self, pos, surf, groups):
		super().__init__(pos,surf,groups)
		self.hitbox = self.rect.copy().inflate(-20,-self.rect.height* 0.5)


class fence(Generic):	
	def __init__(self, pos, surf, groups):
		super().__init__(pos,surf,groups)
		self.hitbox = self.rect.copy()
class base2(Generic):
	def __init__(self, pos, surf, groups):
		super().__init__(pos,surf,groups)
		self.hitbox = self.rect.copy()


class Terrain(Generic):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.image = surf
		self.hitbox= self.rect.copy()
		self.rect = self.image.get_frect(topleft=pos)
		self.mask = pygame.mask.from_surface(self.image)
		self.old_rect = self.rect.copy()

class Horizontal_Moving_Block(Generic):
	def __init__(self, pos, surf, groups,speed,distance_left, distance_right):
		super().__init__(pos, surf, groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.old_rect = self.rect.copy()
		self.speed = speed
		self.distance_left = distance_left
		self.distance_right = distance_right
		self.start_pos = (pos[0] - distance_left, pos[1])
		self.end_pos = (pos[0] + distance_right, pos[1])
		self.direction = 1
	def update(self,dt):
		self.rect.x += self.speed * self.direction
		if self.rect.x < self.start_pos[0]:
			self.rect.x = self.start_pos[0]
			self.direction = 1
		elif self.rect.x > self.end_pos[0]:
			self.rect.x = self.end_pos[0]
			self.direction = -1

	def draw(self,surface):
		surface.blit(self.image,self.rect)

from pygame.sprite import Sprite

class Vertical_Moving_Block(Sprite):
	def __init__(self, pos, surf, groups, speed, distance_down, distance_up):
		super().__init__(groups)
		self.image = surf
		self.z = LAYERS2['movable_vertical']
		self.rect = self.image.get_rect(topleft=pos)
		self.old_rect = self.rect.copy()
		self.speed = speed
		self.distance_down = distance_down
		self.distance_up = distance_up
		self.start_pos = (pos[0], pos[1] + distance_down)
		self.end_pos = (pos[0], pos[1] - distance_up)
		self.direction = 1
	
	def update(self, dt):
		self.rect.y += self.speed * self.direction * dt
		if self.rect.y > self.start_pos[1]:
			self.rect.y = self.start_pos[1]
			self.direction = -1
		elif self.rect.y < self.end_pos[1]:
			self.rect.y = self.end_pos[1]
			self.direction = 1
	
	def draw(self, surface):
		surface.blit(self.image, self.rect)
