import pygame 
from settings import *
from player import Player
from player2 import Player2
from sprites import Generic,Interactable,nonInteractable,fence,base2,Terrain, Horizontal_Moving_Block,Vertical_Moving_Block
from pytmx.util_pygame import load_pygame
from support import *
from os.path import join
class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()
		self.status='level2'
		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites=pygame.sprite.Group()

		self.horizontal_moving_blocks = pygame.sprite.Group()
		self.vertical_moving_blocks = pygame.sprite.Group()

		# setup
		# self.player = Player((531,1095), self.all_sprites,self.collision_sprites)
		self.player2 = Player2((0,0), self.all_sprites,self.collision_sprites)

		self.setup()

	def setup(self):
		if self.status=='map':
			tmx_data=load_pygame(join('..', 'data', 'tsx', 'map.tmx'))
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

		elif self.status=='level1':
			tmx_data=load_pygame(join('..', 'data', 'tsx', 'level1.tmx'))
			for  layer in ['constantterrrain']:
				for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
					Terrain((x*TILE_SIZE,y*TILE_SIZE), surf, (self.all_sprites, self.collision_sprites))
		
			for x, y, surf in tmx_data.get_layer_by_name('Deathlayer').tiles():
				Terrain((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites,self.collision_sprites])

				
			for horizontal_obj in tmx_data.get_layer_by_name('movable_horizontal'):
				
				Horizontal_Moving_Block(
					pos = (horizontal_obj.x, horizontal_obj.y),
					surf = horizontal_obj.image,
					groups = (self.all_sprites, self.collision_sprites, self.horizontal_moving_blocks),
					speed = 150,
					distance = 15 * TILE_SIZE)
			
			for vertical_obj in tmx_data.get_layer_by_name('movable_vertical'):
				Vertical_Moving_Block(
					pos = (vertical_obj.x, vertical_obj.y),
					surf = vertical_obj.image,
					groups = (self.all_sprites, self.collision_sprites, self.vertical_moving_blocks),
					speed = 150,
					distance = 8 * TILE_SIZE)
				
		elif self.status == 'level2':
			tmx_data=load_pygame(join('..', 'data', 'tsx', 'level2.tmx'))
			for  layer in ['constantterrrain']:
				for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
					Terrain((x*TILE_SIZE,y*TILE_SIZE), surf, (self.all_sprites, self.collision_sprites))
		
			for x, y, surf in tmx_data.get_layer_by_name('Deathlayer').tiles():
				Terrain((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites,self.collision_sprites])

				
			for horizontal_obj in tmx_data.get_layer_by_name('movable_horizontal'):
				# print(horizontal_obj.x,horizontal_obj.y)
				Horizontal_Moving_Block(
					pos = (horizontal_obj.x, horizontal_obj.y),
					surf = horizontal_obj.image,
					groups = (self.all_sprites, self.collision_sprites, self.horizontal_moving_blocks),
					speed = 150,
					distance = 2 * TILE_SIZE)
			
			for vertical_obj in tmx_data.get_layer_by_name('movable_vertical'):
				# if vertical_obj.name == "first_stair":
					Vertical_Moving_Block(
						pos = (vertical_obj.x, vertical_obj.y),
						surf = vertical_obj.image,
						groups = (self.all_sprites, self.collision_sprites, self.vertical_moving_blocks),
						speed = 5,
						distance = 5 * TILE_SIZE)
				


	def run(self,dt,status):
		if status=='map':
			self.display_surface.fill('black')
			self.all_sprites.custom_draw(self.player,'map')
			self.all_sprites.update(dt)
		elif status=='level1':
			self.display_surface.fill('black')
			self.all_sprites.custom_draw(self.player2,'level1')
			self.horizontal_moving_blocks.draw(self.display_surface)
			self.vertical_moving_blocks.draw(self.display_surface)
			self.all_sprites.update(dt)
		elif status=='level2':
			self.display_surface.fill('black')
			self.all_sprites.custom_draw(self.player2,'level2')
			self.horizontal_moving_blocks.draw(self.display_surface)
			self.vertical_moving_blocks.draw(self.display_surface)
			self.all_sprites.update(dt)

		

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player,status):
		if status=='map':
			self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
			self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

			for layer in LAYERS.values():
				for sprite in self.sprites():
					if sprite.z == layer:
						offset_rect = sprite.rect.copy()
						offset_rect.center -= self.offset
						self.display_surface.blit(sprite.image, offset_rect)
		else:
			self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
			self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

			for layer in LAYERS2.values():
				for sprite in self.sprites():
					if sprite.z == layer:
						offset_rect = sprite.rect.copy()
						offset_rect.center -= self.offset
						self.display_surface.blit(sprite.image, offset_rect)