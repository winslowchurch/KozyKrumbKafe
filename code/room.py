import pygame, random
from ui import UI
from data import *

class Room:
	def __init__(self, surface):
		self.ui = UI(surface)
		self.isBakeryOpen = False

		self.titleRoom = Title_Room(self.ui)
		self.bakeryRoom = Bakery_Room(self.ui)
		self.editRoom = Edit_Room(self.ui)
		self.kitchenRoom = Kitchen_Room(self.ui)
		self.current = self.titleRoom # initial room
		
	# each Room has an update function
	def update(self, clickedCoordinates): 
		self.current.update(self, clickedCoordinates)

class Title_Room:
	def __init__(self, ui):
		self.ui = ui
		self.background = pygame.image.load('../graphics/other/titleBackground.png')
		self.startButton = pygame.image.load('../graphics/ui/categoryButton.png')
		self.startButton_rect = ui.getRect(self.startButton, 509, 563)
		self.hover_startButton = pygame.image.load('../graphics/ui/selectedCategoryButton.png')
		self.startText = self.ui.font.render("Start", True, (255,255,255))

	def update(self, Room, mp):
		# takes user to bakery
		if self.startButton_rect.collidepoint(mp):
			Room.current = Room.bakeryRoom # change rooms
			pygame.mixer.Sound.play(self.ui.click_sound) # play sound

	def draw(self,surface, Room):
		surface.blit(self.background,(0,0))
		# start button
		if self.startButton_rect.collidepoint(pygame.mouse.get_pos()):
			surface.blit(self.hover_startButton,(509,570))
			surface.blit(self.startText, (555, 564))
		else: 
			surface.blit(self.startButton,(509,565))
			surface.blit(self.startText, (555, 559))

class Bakery_Room:
	def __init__(self, ui):
		self.ui = ui
		# initial bakery decor
		self.outside = pygame.image.load('../graphics/other/outside.png').convert_alpha()
		self.counter = pygame.image.load('../graphics/other/counter.png').convert()
		self.floor = pygame.image.load('../graphics/floors/whiteCheckered.png').convert_alpha()
		self.walls = pygame.image.load('../graphics/walls/green.png').convert_alpha()
		self.frames = pygame.image.load('../graphics/frames/blue.png').convert_alpha()
		self.basics = pygame.image.load('../graphics/other/basics.png').convert_alpha()
		self.decor = None
		self.furniture = None
		self.knickKnacks = None

		self.customer = None
		self.customer_order = None
		self.order_total = None

	def update(self, Room, mp):
		# edit button
		if self.ui.editButton_rect.collidepoint(mp):
			Room.current = Room.editRoom # switch rooms
			pygame.mixer.Sound.play(self.ui.click_sound)
		# open sign
		elif self.ui.sign_rect.collidepoint(mp):
			Room.isBakeryOpen = not Room.isBakeryOpen # flip sign
			pygame.mixer.Sound.play(self.ui.boop_sound)
			if Room.isBakeryOpen and not self.customer:
				self.addCustomer()
		# clicks receipt
		elif (Room.isBakeryOpen or self.customer) and self.ui.receipt_rect.collidepoint(mp):
			Room.current = Room.kitchenRoom
			pygame.mixer.Sound.play(self.ui.boop_sound)

	def addCustomer(self):
		# randomly select customer
		self.customer = random.choice(list(customers_list))
		# randomize food order 
		order_items = random.sample(list(food_and_prices_list.keys()), random.randint(1, 3))
		order_dict = {}
		for item in order_items:
			order_dict[item] = random.randint(1, 2)
		self.customer_order = order_dict
		
		# save order total
		self.order_total = self.ui.orderTotal(self.customer_order)

	def giveOrderToCustomer(self, givenOrder, Room):
		if self.ordersMatch(self.customer_order, givenOrder):
			self.ui.moneyCount = round(self.ui.moneyCount + self.order_total, 2)
			pygame.mixer.Sound.play(self.ui.kaching_sound)
		
		Room.kitchenRoom.orderForCustomer = []
		Room.kitchenRoom.orderBag = order_bag_imgs[0]
		if Room.isBakeryOpen:
			self.addCustomer()
		else:
			self.customer = None

	# returns true if the customer was given at least what they ordered
	def ordersMatch(self, correctOrder, givenOrder):
		count_dict = {}
		for item in givenOrder:
			if item in count_dict:
				count_dict[item] += 1		
			else:
				count_dict[item] = 1

		for key, value in correctOrder.items():
			if key not in count_dict or count_dict[key] < value:
				return False
		return True

	def draw(self,surface, Room):
		surface.blit(self.outside,(0,0))
		surface.blit(self.floor,(0,330))
		surface.blit(self.counter,(0,582))
		surface.blit(self.walls, (0,0))
		surface.blit(self.frames, (245,0))
		if (self.decor): surface.blit(self.decor, (0,0))
		if (self.furniture): surface.blit(self.furniture, (0,0))
		if (self.knickKnacks): surface.blit(self.knickKnacks, (0, 420))
		surface.blit(self.basics, (0,0))

		self.ui.show_edit()
		self.ui.show_money()
		self.ui.show_window_sign(Room.isBakeryOpen)

		if Room.isBakeryOpen or self.customer:
			self.ui.drawCustomer(surface, self.customer, self.customer_order, self.order_total)

class Edit_Room:
	def __init__(self,ui):
		self.ui = ui
		self.selectedCategory = "walls"
		self.background = pygame.image.load('../graphics/ui/editBackground.png')
		
		# current selections
		self.selected_wall = 'Green'
		self.selected_floor = 'White Check'
		self.selected_frame = 'Blue'
		self.selected_decor = None
		self.selected_furniture = None
		self.selected_knickKnack = None

	def update(self, Room, mp):
		# close editor
		if self.ui.closeButton_rect.collidepoint(mp):
			Room.current = Room.bakeryRoom
			pygame.mixer.Sound.play(self.ui.click_sound)
		else:
			# switch categories
			for button_rect, category in zip(self.ui.categoryButton_rects, store_categories):
				if button_rect.collidepoint(mp):
					pygame.mixer.Sound.play(self.ui.boop_sound)
					self.selectedCategory = category

			# switch card selection
			if self.selectedCategory == "walls":
				self.ui.handleClickItemCard(self.selectedCategory, self.ui.wall_options, mp, Room)
			elif self.selectedCategory == "floors":
				self.ui.handleClickItemCard(self.selectedCategory, self.ui.floor_options, mp, Room)
			elif self.selectedCategory == "frames":
				self.ui.handleClickItemCard(self.selectedCategory, self.ui.frame_options, mp, Room)
			elif self.selectedCategory == "decor":
				self.ui.handleClickItemCard(self.selectedCategory, self.ui.decor_options, mp, Room)
			elif self.selectedCategory == "furniture":
				self.ui.handleClickItemCard(self.selectedCategory, self.ui.furniture_options, mp, Room)
			elif self.selectedCategory == "knickKnacks":				
				self.ui.handleClickItemCard(self.selectedCategory, self.ui.knickKnack_options, mp, Room)


	def draw(self,surface, Room):
		surface.blit(self.background, (0,0))
		
		for idx, category in enumerate(store_categories):
			button_x = 40 + idx * 180 # 200 is distance between each start pos of category
			cText = self.ui.font.render(category.capitalize(), True, self.ui.textColor)
			self.ui.drawCategoryButton(surface, self.selectedCategory, cText, button_x, category, idx)

		self.ui.drawItemCards(surface, self.selectedCategory, Room)

		self.ui.show_close()
		self.ui.show_money()

# Actual game part **
class Kitchen_Room:
	def __init__(self, ui):
		self.ui = ui
		self.background = pygame.image.load('../graphics/kitchen/background.png')
		self.cinnamonRolls = pygame.image.load('../graphics/kitchen/cinnamonRolls.png')
		self.cinnamonRolls_rect = self.ui.getRect(self.cinnamonRolls, 765, 200)
		self.cupcakes = pygame.image.load('../graphics/kitchen/cupcakes.png')
		self.cupcakes_rect = self.ui.getRect(self.cupcakes, 130, 420)
		self.baguettes = pygame.image.load('../graphics/kitchen/baguette.png')
		self.baguettes_rect = self.ui.getRect(self.baguettes, 860, 340)
		self.bananaBread = pygame.image.load('../graphics/kitchen/bananaBread.png')
		self.bananaBread_rect = self.ui.getRect(self.bananaBread, 970, 460)
		self.rolls = pygame.image.load('../graphics/kitchen/rolls.png')
		self.rolls_rect = self.ui.getRect(self.rolls, 700, 430)
		self.berryMuffins = pygame.image.load('../graphics/kitchen/berryMuffins.png')
		self.berryMuffins_rect = self.ui.getRect(self.berryMuffins, 270, 390)
		self.donuts = pygame.image.load('../graphics/kitchen/donuts.png')
		self.donuts_rect = self.ui.getRect(self.donuts, 305, 235)
		self.cookies = pygame.image.load('../graphics/kitchen/cookies.png')
		self.cookies_rect = self.ui.getRect(self.cookies, 1050, 350)
		self.pretzels = pygame.image.load('../graphics/kitchen/pretzel.png')
		self.pretzels_rect = self.ui.getRect(self.pretzels, 1030, 215)
		self.cake = pygame.image.load('../graphics/kitchen/cake.png')
		self.cake_rects = self.ui.getRect(self.cake, 285, 530)
		self.velvetMuffins = pygame.image.load('../graphics/kitchen/velvetMuffins.png')
		self.velvetMuffins_rects = self.ui.getRect(self.velvetMuffins, 390, 340)
		self.eclairs = pygame.image.load('../graphics/kitchen/eclairs.png')
		self.eclairs_rect = self.ui.getRect(self.eclairs, 320, 295)
		self.pie = pygame.image.load('../graphics/kitchen/pie.png')
		self.pie_rect = self.ui.getRect(self.pie, 135, 590)
		self.croissant = pygame.image.load('../graphics/kitchen/croissant.png')
		self.croissant_rect = self.ui.getRect(self.croissant, 710, 330)

		self.orderBag = order_bag_imgs[0]
		self.orderBag_rect = self.ui.getRect(self.orderBag, 50, 265)

		self.orderForCustomer = []

	def draw(self, surface, Room):
		surface.blit(self.background, (0,0))
		# counter items
		self.ui.draw_bigger_on_hover(surface, self.orderBag, self.orderBag_rect, 50, 265)
		self.ui.draw_bigger_on_hover(surface, self.cupcakes, self.cupcakes_rect, 130, 420)
		self.ui.draw_bigger_on_hover(surface, self.berryMuffins, self.berryMuffins_rect, 270, 390)
		self.ui.draw_bigger_on_hover(surface, self.donuts, self.donuts_rect, 305, 235)
		self.ui.draw_bigger_on_hover(surface, self.cake, self.cake_rects, 285, 530)
		self.ui.draw_bigger_on_hover(surface, self.velvetMuffins, self.velvetMuffins_rects, 390, 340)
		self.ui.draw_bigger_on_hover(surface, self.eclairs, self.eclairs_rect, 320, 295)
		self.ui.draw_bigger_on_hover(surface, self.pie, self.pie_rect, 135, 590)

		# shelf items
		self.ui.draw_bigger_on_hover(surface, self.cinnamonRolls, self.cinnamonRolls_rect, 765, 200)
		self.ui.draw_bigger_on_hover(surface, self.pretzels, self.pretzels_rect, 1030, 215)
		self.ui.draw_bigger_on_hover(surface, self.croissant, self.croissant_rect, 710, 330)
		self.ui.draw_bigger_on_hover(surface, self.baguettes, self.baguettes_rect, 860, 340)
		self.ui.draw_bigger_on_hover(surface, self.cookies, self.cookies_rect, 1050, 350)
		self.ui.draw_bigger_on_hover(surface, self.rolls, self.rolls_rect, 700, 430)
		self.ui.draw_bigger_on_hover(surface, self.bananaBread, self.bananaBread_rect, 970, 460)

		self.ui.show_money()

	def addToBag(self, Food):
		pygame.mixer.Sound.play(self.ui.addToBag_sound)
		self.ui.moneyCount = round(self.ui.moneyCount - 0.8, 2)
		self.orderForCustomer.append(Food)
		self.orderBag = order_bag_imgs[min(len(self.orderForCustomer), 3)]

	def update(self, Room, mp):
		if self.orderBag_rect.collidepoint(mp):
			Room.current = Room.bakeryRoom # order complete
			Room.bakeryRoom.giveOrderToCustomer(self.orderForCustomer, Room)
		elif self.cupcakes_rect.collidepoint(mp): self.addToBag("Cupcake")
		elif self.donuts_rect.collidepoint(mp): self.addToBag("Donut")
		elif self.berryMuffins_rect.collidepoint(mp): self.addToBag("Berry Muffin")
		elif self.cinnamonRolls_rect.collidepoint(mp): self.addToBag("Cinnamon Roll")
		elif self.baguettes_rect.collidepoint(mp): self.addToBag("Baguette")
		elif self.cookies_rect.collidepoint(mp): self.addToBag("Cookie")
		elif self.rolls_rect.collidepoint(mp): self.addToBag("Roll")
		elif self.bananaBread_rect.collidepoint(mp): self.addToBag("Banana Bread")
		elif self.pretzels_rect.collidepoint(mp): self.addToBag("Pretzel")
		elif self.cake_rects.collidepoint(mp): self.addToBag("Slice of Cake")
		elif self.velvetMuffins_rects.collidepoint(mp): self.addToBag("Velvet Muffin")
		elif self.eclairs_rect.collidepoint(mp): self.addToBag("Eclair")
		elif self.pie_rect.collidepoint(mp): self.addToBag("Slice of Pie")
		elif self.croissant_rect.collidepoint(mp): self.addToBag("Croissant")
