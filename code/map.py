import pygame 
from settings import *
from player import Player
from sprites import Generic,Interactable
from pytmx.util_pygame import load_pygame
from support import *
class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = CameraGroup()

		self.setup()

	def setup(self):
		tmx_data=load_pygame('/home/silversage22/Desktop/sem4/COP290/game/data/tsx/map.tmx')
		for  layer in ['base','road','water','fence','base2']:
			for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
	
				Generic(
					pos = (x*TILE_SIZE,y*TILE_SIZE),
					surf = surf,
					groups = self.all_sprites,
					z = LAYERS[layer])
				
		for  obj in tmx_data.get_layer_by_name('noninteractable'):
			Generic((obj.x,obj.y),obj.image,self.all_sprites,z=LAYERS['Interactable'])
		for  obj in tmx_data.get_layer_by_name('interactable'):
			Generic((obj.x,obj.y),obj.image,self.all_sprites,z=LAYERS['Interactable'])


		self.player = Player((640,360), self.all_sprites)
	   


	def run(self,dt):
		self.display_surface.fill('black')
		self.all_sprites.custom_draw(self.player)
		self.all_sprites.update(dt)

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		for layer in LAYERS.values():
			for sprite in self.sprites():
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)