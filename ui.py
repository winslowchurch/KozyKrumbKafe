import pygame
from data import *

class UI:
	def __init__(self,surface):
		self.display_surface = surface
		self.font = pygame.font.Font('assets/kozy.TTF', 55) 
		self.smallFont = pygame.font.Font('assets/kozy.TTF', 45) 
		self.textColor = (119,43,62,255)
		self.moneyCount = 0
		self.inventory = item_inventory

		# edit button
		self.editButton = pygame.image.load('graphics/ui/editButton.png')
		self.editButton_rect = self.getRect(self.editButton, 1135, 10)
		# close button
		self.closeButton = pygame.image.load('graphics/ui/closeButton.png')
		self.closeButton_rect = self.getRect(self.closeButton, 1135, 10)
		# money
		self.moneyArea = pygame.image.load('graphics/ui/moneyArea.png')
		# open / closed signs
		self.openSign = pygame.image.load('graphics/ui/openSign.png')
		self.closedSign = pygame.image.load('graphics/ui/closedSign.png')
		self.sign_rect = self.getRect(self.openSign, 320, 160)
		# categories
		self.categoryButton = pygame.image.load('graphics/ui/categoryButton.png')
		self.selectedCategoryButton = pygame.image.load('graphics/ui/selectedCategoryButton.png')
		self.categoryButton_rects = [pygame.Rect(x, 80, 171, 74) for x in range(40, 1000, 180)]

		self.wall_options = wall_options_list
		self.floor_options = floor_options_list
		self.frame_options = frame_options_list
		self.decor_options = decor_options_list
		self.furniture_options = furniture_options_list
		self.knickKnack_options = knick_knacks_options_list

		# item card
		self.itemCard =  pygame.image.load('graphics/ui/itemCard.png')
		self.selectedItemCard =  pygame.image.load('graphics/ui/selectedItemCard.png')
		self.itemCard_rects = [pygame.Rect(x, 180, 209, 229) for x in range(40, 1000, 225)]
		self.itemCard_rects += [pygame.Rect(x, 450, 209, 229) for x in range(40, 1000, 225)]
		# buy button
		self.buyButton = pygame.image.load('graphics/ui/buyButton.png')
		self.hoverBuyButton = pygame.image.load('graphics/ui/pressedBuyButton.png')
		self.buyButton_rects = [pygame.Rect(x, 320, 85, 35) for x in range(140, 1200, 225)]
		self.buyButton_rects += [pygame.Rect(x, 590, 85, 35) for x in range(140, 1200, 225)]

		# receipt
		self.receipt = pygame.image.load('graphics/ui/receipt.png')
		self.receipt_rect = self.getRect(self.receipt, 100, 300)

		pygame.mixer.init()
		self.click_sound = pygame.mixer.Sound('assets/click.wav')
		self.kaching_sound = pygame.mixer.Sound('assets/kaching.wav')
		self.addToBag_sound = pygame.mixer.Sound('assets/bag.wav')
		self.boop_sound = pygame.mixer.Sound('assets/boop.wav')
		self.error_sound = pygame.mixer.Sound('assets/error.wav')

	def getRect(self, image, x, y):
		return pygame.Rect(x, y, image.get_rect().width, image.get_rect().height)
	
	# x,y are original image coordinates
	def draw_bigger_on_hover(self, surface, image, image_rect, x, y):
		if image_rect.collidepoint(pygame.mouse.get_pos()):
			old_width, old_height = image.get_rect().width, image.get_rect().height
			new_width, new_height = old_width + 10, old_height + 10
			biggerImage = pygame.transform.scale(image, (new_width, new_height))
			new_x = x-((new_width-old_width)/2)
			new_y = y-((new_height-old_height)/2)
			surface.blit(biggerImage, (new_x, new_y))
		else:
			surface.blit(image, (x, y))

	# display wrench button in top right corner, growing on hover
	def show_edit(self):
		self.draw_bigger_on_hover(self.display_surface, self.editButton, self.editButton_rect, 1135, 10)
	
	# display x button in top right corner, growing on hover
	def show_close(self):
		self.draw_bigger_on_hover(self.display_surface, self.closeButton, self.closeButton_rect, 1135, 10)

	#  display players money in top left corner
	def show_money(self):
		x,y = 10, 10
		self.display_surface.blit(self.moneyArea,(x,y))
		moneyString = self.font.render("$" + str(self.moneyCount), True, (119,43,62,255))
		self.display_surface.blit(moneyString, (x+8, y-5))

	# display open/closed sign in window, growing on hover
	def show_window_sign(self, isOpen):
		if (isOpen): 
			result = self.closedSign
		else:
			result = self.openSign
		
		self.draw_bigger_on_hover(self.display_surface, result, self.sign_rect, 320, 160)

	def drawCategoryButton(self, surface, selectedCategory, text, x, category, buttonNum):
		hoveringOverCategory = self.categoryButton_rects[buttonNum].collidepoint(pygame.mouse.get_pos())
		if (category == selectedCategory or hoveringOverCategory):
			surface.blit(self.selectedCategoryButton, (x, 92))
			surface.blit(text, (x+10, 89))
		else:
			surface.blit(self.categoryButton, (x, 85))
			surface.blit(text, (x+10, 82))

	def drawItemCards(self, surface, category, Room):
		px, py = 163, 104
		if category == "walls":
			itemOptions = self.wall_options
			selectedCard = Room.editRoom.selected_wall
			source_rect = pygame.Rect(20, 0, px, py)
		elif category == "floors":
			itemOptions = self.floor_options
			selectedCard = Room.editRoom.selected_floor
			source_rect = pygame.Rect(200,50, px, py)
		elif category == "frames":
			itemOptions = self.frame_options
			selectedCard = Room.editRoom.selected_frame
			source_rect = pygame.Rect(270,233, px, py)
		elif category == "decor":
			itemOptions = self.decor_options
			selectedCard = Room.editRoom.selected_decor
			source_rect = pygame.Rect(970,70, px, py)
		elif category == "furniture":
			itemOptions = self.furniture_options
			selectedCard = Room.editRoom.selected_furniture
			source_rect = pygame.Rect(820,300, px, py)
		elif category == "knickKnacks":
			itemOptions = self.knickKnack_options
			selectedCard = Room.editRoom.selected_knickKnack
			source_rect = pygame.Rect(20,70, px, py)

		x, y, i = 40, 180, 0
		for option in itemOptions.keys():


        	# Display item card
			if (selectedCard == option or self.itemCard_rects[i].collidepoint(pygame.mouse.get_pos())):
				surface.blit(self.selectedItemCard, (x, y))
			else:
				surface.blit(self.itemCard, (x, y))

            # Display a chunk of the item image
			item_image = pygame.image.load(f'graphics/{category}/{itemOptions[option][0]}')
			surface.blit(item_image, (x + 21, y + 22), source_rect)
			
			if option not in self.inventory[category]:
				if self.buyButton_rects[i].collidepoint(pygame.mouse.get_pos()):
					surface.blit(self.hoverBuyButton, (x+100, y+144))
				else: 
					surface.blit(self.buyButton, (x+100, y+140))

			surface.blit(self.smallFont.render('$' + str(itemOptions[option][1]), True, self.textColor), (x + 20, y + 130))
			surface.blit(self.smallFont.render(option, True, self.textColor), (x + 20, y + 175))
			x += 225 # distance between cards
			i += 1
			if x > 1000:
				x = 40
				y = 450

	def handleClickItemCard(self, category, options, mp, Room):
		i = 0
		for option_rect, option in zip(self.itemCard_rects, options.keys()):
			if option_rect.collidepoint(mp):
				img = pygame.image.load(f'graphics/{category}/{options[option][0]}')
				if option not in self.inventory[category]:
					if self.buyButton_rects[i].collidepoint(mp): # buy now
						# can only buy if enough funds
						newMoneyCount = round(self.moneyCount - options[option][1], 2)
						if newMoneyCount >= 0:
							self.inventory[category].append(option)
							self.moneyCount = newMoneyCount
							self.updateItemSelection(category, img, Room, option)
							pygame.mixer.Sound.play(self.boop_sound)
						else: 
							pygame.mixer.Sound.play(self.error_sound)
				else:
					pygame.mixer.Sound.play(self.boop_sound)
					self.updateItemSelection(category, img, Room, option)
			i += 1
			
	def updateItemSelection(self, category, img, Room, option):
		if option == 'None':
			img = None

		if category == "walls":
			Room.editRoom.selected_wall = option
			Room.bakeryRoom.walls = img
		elif category == "floors":
			Room.editRoom.selected_floor = option
			Room.bakeryRoom.floor = img
		elif category == "frames":
			Room.editRoom.selected_frame = option
			Room.bakeryRoom.frames = img
		elif category == "decor":
			Room.editRoom.selected_decor = option
			Room.bakeryRoom.decor = img
		elif category == "furniture":
			Room.editRoom.selected_furniture = option
			Room.bakeryRoom.furniture = img
		elif category == "knickKnacks":
			Room.editRoom.selected_knickKnack = option
			Room.bakeryRoom.knickKnacks = img

	def drawCustomer(self, surface, customer, Order, order_total):
		# customer
		customer_img = pygame.image.load(f'graphics/customers/{customers_list[customer]}').convert_alpha()
		surface.blit(customer_img, (500,45))

		# receipt
		rx, ry = 100, 320
		self.draw_bigger_on_hover(surface, self.receipt, self.receipt_rect, rx, ry)

		# customer name
		surface.blit(self.font.render(customer, True, self.textColor), (rx+15, ry+5))
		# food order
		food_y = 60
		for food in list(Order.keys()):
			surface.blit(self.font.render(str(Order[food]), True, self.textColor), (rx+15, ry+food_y))
			surface.blit(self.font.render(food, True, self.textColor), (rx+45, ry+food_y))
			surface.blit(self.font.render('$' + str(food_and_prices_list[food] * Order[food]), True, self.textColor), (rx+240, ry+food_y))
			food_y += 50
		# total
		total = "$" + str(order_total)
		surface.blit(self.font.render(total, True, self.textColor), (rx+220, ry+275))

	def orderTotal(self, Order):
		total = 0
		for food in Order:
			total = round(total + (food_and_prices_list[food] * Order[food]), 2)
		return total

	