import pygame, sys
from settings import *
from map import Level

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption('Sprout land')
		self.clock = pygame.time.Clock()
		self.level = Level('level2')
		self.changed=False

	def run(self):
		while True:
			# if self.level.status=='level1':
				# print('Starting')
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				else:
					if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_ESCAPE:
								pygame.quit()
								sys.exit()
							
			if self.level.players.levelchanger==True:
					
					self.level.status = self.level.players.levelchangedto
					print(self.level.players.levelchangedto)

					self.level=Level(self.level.players.levelchanger)
					self.changed=True
					print('level has been initiated')
						
			if self.changed==False:
				dt = self.clock.tick() / 1000
				self.level.run(dt)
				pygame.display.update()
			else:
				dt = self.clock.tick() / 1000
				self.level.run(dt)
				print('started running')
				pygame.display.update()


if __name__ == '__main__':
	game = Game()
	game.run()

