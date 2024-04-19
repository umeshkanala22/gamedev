import pygame, sys
from settings import *
from map import Level

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption('Sprout land')
		self.clock = pygame.time.Clock()
		self.tolevel='none'
		self.levelmap={
			'map':Level('map',self.tolevel),
			'level1':Level('level1',self.tolevel),
			'level2':Level('level2',self.tolevel)
		}
		self.tolevel='none'
		self.level=self.levelmap['map']


	def run(self):
		while True:
			self.screen.fill('black')
			self.tolevel=self.level.tolevel
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				else:
					if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_ESCAPE:
								pygame.quit()
								sys.exit()
			if self.level.tolevel !='none':
				self.level=self.levelmap[self.level.tolevel]
				self.tolevel='none'							
			
			dt = self.clock.tick() / 1000
			self.level.run(dt)
			print('started running')
			pygame.display.update()


if __name__ == '__main__':
	game = Game()
	game.run()

