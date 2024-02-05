import pygame
from ui import UI
textColor = (119,43,62,255)

class Room:
    def __init__(self, surface):
        self.ui = UI(surface)
        self.bakeryRoom = Bakery_Room(self.ui)
        self.editRoom = Edit_Room(self.ui)
        self.current = self.editRoom
	
    def update(self, mp):
        self.current.update(self, mp)	

class Bakery_Room:
	def __init__(self, ui):
		self.ui = ui

		self.outside = pygame.image.load('../graphics/outside.png').convert_alpha()
		self.counter = pygame.image.load('../graphics/counter.png').convert()
		self.floor = pygame.image.load('../graphics/floors/whiteCheckered.png').convert_alpha()
		self.walls = pygame.image.load('../graphics/walls/wood.png').convert_alpha()
		self.windows = pygame.image.load('../graphics/windows/blue.png').convert_alpha()
		self.decorations = pygame.image.load('../graphics/decorations.png').convert_alpha()

	def update(self, Room, mp):
		if self.ui.editButton_rect.collidepoint(mp):
			Room.current = Room.editRoom

	def draw(self,surface):
		surface.blit(self.outside,(0,0))
		surface.blit(self.floor,(0,330))
		surface.blit(self.counter,(0,582))
		surface.blit(self.walls, (0,0))
		surface.blit(self.windows, (245,0))
		surface.blit(self.decorations, (0,0))

		self.ui.show_edit()
		self.ui.show_money()

class Edit_Room:
	def __init__(self,ui):
		self.ui = ui
		self.selectedCategory = "walls"
		self.background = pygame.image.load('../graphics/edit/editBackground.png')
		# categories
		self.categoryButton = pygame.image.load('../graphics/edit/categoryButton.png')
		self.selectedCategoryButton = pygame.image.load('../graphics/edit/selectedCategoryButton.png')
		self.categoryButtonRects = [pygame.Rect(x, 80, 182, 74) for x in range(40, 800, 200)]
		# category names
		self.wallsText = self.ui.font.render("Walls", True, textColor)
		self.floorsText = self.ui.font.render("Floors", True, textColor)
		self.windowsText = self.ui.font.render("Windows", True, textColor)
		self.decorText = self.ui.font.render("Decor", True, textColor)

		# category items
		self.itemCard =  pygame.image.load('../graphics/edit/itemCard.png')
		self.selectedItemCard =  pygame.image.load('../graphics/edit/selectedItemCard.png')

		self.wall_options = {'Green': 'green.png', 'Wooden': 'wood.png', 'Blue Striped': 'blueStripe.png', 'Pink Dots': 'pinkPolkaDots.png'}
		self.selected_wall = 'Green'
		self.floor_options = {'White Check': 'whiteCheckered.png', 'Black Check': 'blackCheckered.png'}
		self.selected_floor = 'White Check'
		self.window_options = {'Blue': 'blue.png', 'Pink': 'pink.png'}
		self.selected_window = 'Blue'

		option_width = 209
		option_height = 229
		self.wall_option_rects = [pygame.Rect(x, 180, option_width, option_height) for x in range(40, 840, 220)]

	def update(self, Room, mp):
		if self.ui.closeButton_rect.collidepoint(mp):
			Room.current = Room.bakeryRoom
		else:
			# switch categories
			for button_rect, category in zip(self.categoryButtonRects, ["walls", "floors", "windows", "decor"]):
				if button_rect.collidepoint(mp):
					self.selectedCategory = category

			# switch card selection
			if self.selectedCategory == "walls":
				self.updateCardSelection(self.wall_options, mp, Room)
			elif self.selectedCategory == "floors":
				self.updateCardSelection(self.floor_options, mp, Room)
			elif self.selectedCategory == "windows":
				self.updateCardSelection(self.window_options, mp, Room)

	def updateCardSelection(self, options, mp, Room):
		option_rects = [pygame.Rect(x, 180, 209, 229) for x in range(40, 840, 220)]
		for option_rect, option in zip(option_rects, options.keys()):
			if option_rect.collidepoint(mp):
				if self.selectedCategory == "walls":
					self.selected_wall = option
					Room.bakeryRoom.walls = pygame.image.load(f'../graphics/{self.selectedCategory}/{options[self.selected_wall]}')
				elif self.selectedCategory == "floors":
					self.selected_floor = option
					Room.bakeryRoom.floor = pygame.image.load(f'../graphics/{self.selectedCategory}/{options[self.selected_floor]}')
				elif self.selectedCategory == "windows":
					self.selected_window = option
					Room.bakeryRoom.windows = pygame.image.load(f'../graphics/{self.selectedCategory}/{options[self.selected_window]}')



	def drawCategoryButton(self, surface, text, x, category):
		if (category == self.selectedCategory):
			surface.blit(self.selectedCategoryButton, (x, 92))
			surface.blit(text, (x+10, 99))
		else:
			surface.blit(self.categoryButton, (x, 85))
			surface.blit(text, (x+10, 92))

	def drawItemCards(self, surface, category):
		if self.selectedCategory == "walls":
			itemOptions = self.wall_options
			selectedCard = self.selected_wall
			source_rect = pygame.Rect(20, 0, 163, 104)
		elif self.selectedCategory == "floors":
			itemOptions = self.floor_options
			selectedCard = self.selected_floor
			source_rect = pygame.Rect(200,50, 163, 104)
		elif self.selectedCategory == "windows":
			itemOptions = self.window_options
			selectedCard = self.selected_window
			source_rect = pygame.Rect(1,230, 163, 104)

		x = 40
		y = 180
		for option in itemOptions.keys():
			item_image = pygame.image.load(f'../graphics/{category}/{itemOptions[option]}')

        	# Display item card
			if (selectedCard == option):
				surface.blit(self.selectedItemCard, (x, y))
			else:
				surface.blit(self.itemCard, (x, y))

            # Display a chunk of the item
			surface.blit(item_image, (x + 21, y + 22), source_rect)

			surface.blit(self.ui.smallFont.render("$50", True, textColor), (x + 20, y + 135))
			surface.blit(self.ui.smallFont.render(option, True, textColor), (x + 20, y + 180))
			x += 220 # distance between cards


	def draw(self,surface):
		surface.blit(self.background, (0,0))
		
		self.drawCategoryButton(surface, self.wallsText, 40, "walls")
		self.drawCategoryButton(surface, self.floorsText, 240, "floors")
		self.drawCategoryButton(surface, self.windowsText, 440, "windows")
		self.drawCategoryButton(surface, self.decorText, 640, "decor")

		self.drawItemCards(surface, self.selectedCategory)

		self.ui.show_close()
		self.ui.show_money()