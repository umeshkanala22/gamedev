import pygame 
from settings import *
from player import Player
from sprites import Generic,Interactable,nonInteractable,fence,base2
from pytmx.util_pygame import load_pygame
from support import *
class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites=pygame.sprite.Group()

		self.setup()

	def setup(self):
		tmx_data=load_pygame('/home/silversage22/Desktop/sem4/COP290/game/data/tsx/map.tmx')
		for x, y, surf in tmx_data.get_layer_by_name('base2').tiles():
			base2((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites,self.collision_sprites])
		for  layer in ['base','road','water']:
			for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
	
				Generic(
					pos = (x*TILE_SIZE,y*TILE_SIZE),
					surf = surf,
					groups = self.all_sprites,
					z = LAYERS[layer])
		for x, y, surf in tmx_data.get_layer_by_name('fence').tiles():
			fence((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites,self.collision_sprites])
	
				
		for  obj in tmx_data.get_layer_by_name('noninteractable'):
			scaled_image =pygame.transform.scale(obj.image,(int(obj.width*4),int(obj.height*4))) 
			nonInteractable((obj.x,obj.y),scaled_image,[self.all_sprites,self.collision_sprites])

			
			
		for  obj in tmx_data.get_layer_by_name('interactable'): 
			if obj.id==902 or obj.id==901:		
				scaled_image =pygame.transform.scale(obj.image,(int(obj.width*4),int(obj.height*4))) 
				Interactable((obj.x-100,obj.y-100),scaled_image,[self.all_sprites,self.collision_sprites])
			else:
				scaled_image =pygame.transform.scale(obj.image,(int(obj.width*2),int(obj.height*2))) 
				Interactable((obj.x,obj.y),scaled_image,[self.all_sprites,self.collision_sprites])


		self.player = Player((531,1095), self.all_sprites,self.collision_sprites)
	   


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