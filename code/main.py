import pygame, sys
from room import Room

screen_height = 748
screen_width = 1200

class Game:
	def __init__(self):
		self.create_rooms()

	def create_rooms(self):
		self.display_surface = screen
		# room contents 
		self.room = Room(screen)

	def run(self):
		self.room.current.draw(self.display_surface)

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
	mouse_position = pygame.mouse.get_pos()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			game.room.update(mouse_position)
	
	game.run()
	pygame.display.update()
	clock.tick(60)