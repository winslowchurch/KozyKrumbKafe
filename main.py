import pygame, sys
from room import Room

# TO DO
# save progress

screen_height = 748
screen_width = 1200

class Game:
	def __init__(self):
		self.create_rooms()
		pygame.display.set_caption('Kozy Krumb Kafe')

	def create_rooms(self):
		self.display_surface = screen
		self.room = Room(screen)

	def run(self):
		self.room.current.draw(self.display_surface, self.room)

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()

pygame.mixer.music.load('assets/kozyTunes.mp3')
pygame.mixer.music.play(-1) 
pygame.mixer.music.set_volume(0.1)

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