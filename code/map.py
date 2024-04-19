import pygame 
from settings import *
from player import Player
from player2 import Player2
from sprites import Generic,Interactable,nonInteractable,fence,base2,Terrain, Horizontal_Moving_Block,Vertical_Moving_Block, Goal
from pytmx.util_pygame import load_pygame
from support import *
from os.path import join
import sys
class Level:
	def __init__(self,status,tolevel):

		# get the display surface
		self.display_surface = pygame.display.get_surface()
		self.status=status
		self.tolevel=tolevel
		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites=pygame.sprite.Group()

		self.death_sprites = pygame.sprite.Group()

		self.horizontal_moving_blocks = pygame.sprite.Group()
		self.vertical_moving_blocks = pygame.sprite.Group()
		self.haschanged = False
		self.changedto='map'

		self.goal_sprites = pygame.sprite.Group()

		self.game_over = False

		self.clock = pygame.time.Clock()

		# setup
		
		
		self.setup()
		

	def is_game_over(self):
		return self.game_over

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
					Interactable((obj.x-100,obj.y-100),scaled_image,[self.all_sprites,self.collision_sprites],'water')
				else:
				
					scaled_image =pygame.transform.scale(obj.image,(int(obj.width*2),int(obj.height*2))) 
					Interactable((obj.x,obj.y),scaled_image,[self.all_sprites,self.collision_sprites],'level1')
				




			self.players=Player((531,1095), self.all_sprites,self.collision_sprites,self.tolevel)

			

		elif self.status=='level1':

			tmx_data=load_pygame(join('..', 'data', 'tsx', 'level1.tmx'))
			for  layer in ['constantterrrain']:
				for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
					Terrain((x*TILE_SIZE,y*TILE_SIZE), surf, (self.all_sprites, self.collision_sprites))
		
			for x, y, surf in tmx_data.get_layer_by_name('Deathlayer').tiles():
				Terrain((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites,self.collision_sprites, self.death_sprites])

				
			for horizontal_obj in tmx_data.get_layer_by_name('movable_horizontal'):
				if horizontal_obj.name == "stair_1":
					# print(horizontal_obj.x, horizontal_obj.y)
					Horizontal_Moving_Block(
						pos = (horizontal_obj.x, horizontal_obj.y),
						surf = horizontal_obj.image,
						groups = (self.all_sprites, self.collision_sprites, self.horizontal_moving_blocks),
						speed = 1,
						distance_left= 10 * TILE_SIZE,
						distance_right= 12 * TILE_SIZE)	
				elif horizontal_obj.name == "stair_2":
					# print(horizontal_obj.x, horizontal_obj.y)
					Horizontal_Moving_Block(
						pos = (horizontal_obj.x, horizontal_obj.y),
						surf = horizontal_obj.image,
						groups = (self.all_sprites, self.collision_sprites, self.horizontal_moving_blocks),
						speed = 1,
						distance_left= 7 * TILE_SIZE,
						distance_right= 14 * TILE_SIZE)
			
			for vertical_obj in tmx_data.get_layer_by_name('movable_vertical'):
				if vertical_obj.name == "first_stair":
					Vertical_Moving_Block(
						pos = (vertical_obj.x, vertical_obj.y),
						surf = vertical_obj.image,
						groups = (self.all_sprites, self.collision_sprites, self.vertical_moving_blocks),
						speed = 2,
						distance_down = 6 * TILE_SIZE,
						distance_up= 10 * TILE_SIZE
					)
				elif vertical_obj.name == "second_stair":
					Vertical_Moving_Block(
						pos = (vertical_obj.x, vertical_obj.y),
						surf = vertical_obj.image,
						groups = (self.all_sprites, self.collision_sprites, self.vertical_moving_blocks),
						speed = 2,
						distance_down = 4 * TILE_SIZE,
					 distance_up= 13 * TILE_SIZE
					)
				
			for goal in tmx_data.get_layer_by_name('goal'):
				if goal.name == "goal":
					Terrain((goal.x, goal.y), goal.image, [self.all_sprites, self.collision_sprites])
					Goal((goal.x , goal.y), goal.image, [self.all_sprites, self.collision_sprites, self.goal_sprites])
			self.players=Player2((4*TILE_SIZE,0), self.all_sprites,self.collision_sprites, self.death_sprites, self.horizontal_moving_blocks,self.goal_sprites,self.tolevel)
		elif self.status == 'level2':
		
			tmx_data=load_pygame(join('..', 'data', 'tsx', 'level2.tmx'))
			for  layer in ['constantterrrain']:
				for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
					Terrain((x*TILE_SIZE,y*TILE_SIZE), surf, (self.all_sprites, self.collision_sprites))
		
			for x, y, surf in tmx_data.get_layer_by_name('Deathlayer').tiles():
				Terrain((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites,self.collision_sprites, self.death_sprites])

				
			for horizontal_obj in tmx_data.get_layer_by_name('movable_horizontal'):
				if horizontal_obj.name == "step_2":
					Horizontal_Moving_Block(
						pos = (horizontal_obj.x, horizontal_obj.y),
						surf = horizontal_obj.image,
						groups = (self.all_sprites, self.collision_sprites, self.horizontal_moving_blocks),
						speed = 1.5,
						distance_left= 0,
						distance_right= 14 * TILE_SIZE)
				elif horizontal_obj.name == "step_1":
					Horizontal_Moving_Block(
						pos = (horizontal_obj.x, horizontal_obj.y),
						surf = horizontal_obj.image,
						groups = (self.all_sprites, self.collision_sprites, self.horizontal_moving_blocks),
						speed = 1.5,
						distance_left= 3 * TILE_SIZE,
						distance_right= 20 * TILE_SIZE)
				elif horizontal_obj.name == "step_3":
					Horizontal_Moving_Block(
						pos = (horizontal_obj.x, horizontal_obj.y),
						surf = horizontal_obj.image,
						groups = (self.all_sprites, self.collision_sprites, self.horizontal_moving_blocks),
						speed = 1.5,
						distance_left= 1 * TILE_SIZE,
						distance_right= 10 * TILE_SIZE)
			
			for vertical_obj in tmx_data.get_layer_by_name('movable_vertical'):
				if vertical_obj.name == "level":
					Vertical_Moving_Block(
						pos = (vertical_obj.x, vertical_obj.y),
						surf = vertical_obj.image,
						groups = (self.all_sprites, self.collision_sprites, self.vertical_moving_blocks),
						speed = 2,
						distance_down = 8 * TILE_SIZE,
						distance_up= 25 * TILE_SIZE
					)

			for goal in tmx_data.get_layer_by_name('goal'):
				if goal.name == "goal":
					Terrain((goal.x, goal.y), goal.image, [self.all_sprites, self.collision_sprites])
					Goal((goal.x , goal.y), goal.image, [self.all_sprites, self.collision_sprites, self.goal_sprites])
			self.players=Player2((4*TILE_SIZE,0), self.all_sprites,self.collision_sprites, self.death_sprites, self.horizontal_moving_blocks,self.goal_sprites,self.tolevel)

		# elif self.status=='mainmenu':

	def wait_for_key(self):
		waiting = True
		key = None
		while waiting:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					key = pygame.key.get_pressed()
					waiting = False
		
		if key[pygame.K_ESCAPE]:
			pygame.quit()
			sys.exit()


	def show_text_on_screen(self, screen, text, font_size, y_position):
		font = pygame.font.Font(None, font_size)
		text_render = font.render(text, True, (255, 255, 255))
		text_rect = text_render.get_rect(center=(SCREEN_WIDTH // 2, y_position))
		screen.blit(text_render, text_rect)


	def game_over_screen(self, screen):
		screen.fill((0, 0, 0))
		self.show_text_on_screen(screen, "Game Over", 100, SCREEN_HEIGHT // 2)
		self.show_text_on_screen(screen, "Press ESC key to exit", 50, SCREEN_HEIGHT // 2 + 100)
		self.show_text_on_screen(screen, "Press any other key to restart", 50, SCREEN_HEIGHT // 2 + 150)
		pygame.display.flip()
		self.wait_for_key()
		# exit()
  
	def level_complete_scrren(self, screen):
		screen.fill((0, 0, 0))
		self.show_text_on_screen(screen, "Level Complete", 100, SCREEN_HEIGHT // 2)
		self.show_text_on_screen(screen, "Press ESC key to exit", 50, SCREEN_HEIGHT // 2 + 100)
		self.show_text_on_screen(screen, "Press any other key to continue", 50, SCREEN_HEIGHT // 2 + 150)
		pygame.display.flip()
		self.wait_for_key()
		# exit()

	def run(self,dt):
		self.tolevel=self.players.tolevel
		if self.status=='map':
			self.display_surface.fill('black')
			self.all_sprites.custom_draw(self.players,'map')
			self.all_sprites.update(dt)
		elif self.status=='level1':
			self.all_sprites.custom_draw(self.players,'level1')
			self.horizontal_moving_blocks.draw(self.display_surface)
			self.vertical_moving_blocks.draw(self.display_surface)
			self.all_sprites.update(dt)
			# check that player is alive or not
			if self.players.is_dead():
				self.game_over = True
				self.game_over_screen(self.display_surface)
			if self.players.is_goal_reached():
				self.level_complete_scrren(self.display_surface)
				self.players.goal_reached = False
				self.players.levelchanger=True
				self.players.levelchangedto='level2'
		elif self.status=='level2':
			# self.display_surface.fill('black')
			self.all_sprites.custom_draw(self.players,'level2')
			self.horizontal_moving_blocks.draw(self.display_surface)
			self.vertical_moving_blocks.draw(self.display_surface)
			self.all_sprites.update(dt)
			# check that player is alive or not
			if self.players.is_dead():
				self.game_over = True
				self.game_over_screen(self.display_surface)
			if self.players.is_goal_reached():
				self.level_complete_scrren(self.display_surface)
				self.players.goal_reached = False
				self.players.levelchanger=True
				self.players.levelchangedto='map'

		

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