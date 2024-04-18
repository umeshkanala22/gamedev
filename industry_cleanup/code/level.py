from settings import * 
from sprites import Sprite
from player import Player

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):
        for x,y , surf in tmx_map.get_layer_by_name('constantterrrain').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE), surf, (self.all_sprites, self.collision_sprites))

        for obj in tmx_map.get_layer_by_name('objects'):
            if obj.name == 'player':
                self.Player=Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)


    def run(self, dt):
        self.display_surface.fill('gray')
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.Player)
    
class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def draw(self, Player):
		self.offset.x = Player.rect.centerx - WINDOW_WIDTH / 2
		self.offset.y = Player.rect.centery - WINDOW_HEIGHT / 2

		for layer in Z_LAYERS.values():
			for sprite in self.sprites():
				if sprite.z == Z_LAYERS:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)