import pygame

class UI:
	def __init__(self,surface):
		self.display_surface = surface
		self.font = pygame.font.Font('../graphics/kozy.otf', 60) 
		self.smallFont = pygame.font.Font('../graphics/kozy.otf', 50) 
		# edit button
		self.editButton = pygame.image.load('../graphics/ui/editButton.png')
		self.editButton_rect = pygame.Rect(1135, 10, 54, 54)
		self.hover_editButton = pygame.transform.scale(self.editButton, (60, 60))
		# close button
		self.closeButton = pygame.image.load('../graphics/ui/closeButton.png')
		self.closeButton_rect = pygame.Rect(1135, 10, 54, 54)
		self.hover_closeButton = pygame.transform.scale(self.closeButton, (60, 60))

		self.moneyArea = pygame.image.load('../graphics/ui/moneyArea.png')
		self.moneyText = self.font.render("$452", True, (119,43,62,255))

	def show_edit(self):
		if self.editButton_rect.collidepoint(pygame.mouse.get_pos()):
			self.display_surface.blit(self.hover_editButton,(1132,7))
		else:
			self.display_surface.blit(self.editButton,(1135,10))
	
	def show_close(self):
		if self.closeButton_rect.collidepoint(pygame.mouse.get_pos()):
			self.display_surface.blit(self.hover_closeButton,(1132,7))
		else:
			self.display_surface.blit(self.closeButton,(1135,10))

	def show_money(self):
		self.display_surface.blit(self.moneyArea,(10,10))
		self.display_surface.blit(self.moneyText, (18, 16))
