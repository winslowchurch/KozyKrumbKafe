import pygame

### STORE ITMES ###
store_categories = [
    "walls", 
    "floors", 
    "frames", 
    "decor",
    "furniture",
    "knickKnacks"
]

# option name and png name, and price
wall_options_list = {
    'Green': ['green.png', 0],
    'Wooden': ['wood.png', 50],
    'Blue Striped': ['blueStripe.png', 50],
    'Pink Dots': ['pinkPolkaDots.png', 50],
    'Brick': ['brick.png', 50],
    'Purple Striped': ['purpleStripe.png', 50],
    'Yellow Wood': ['yellowWood.png', 80],
    'Blue Wood': ['blueWood.png', 80],
    'Fancy White': ['white.png', 80],
    'Fancy Orange': ['orange.png', 80]
}

floor_options_list = {
    'White Check': ['whiteCheckered.png', 0], 
    'Black Check': ['blackCheckered.png', 50],
    'Blue Tile': ['bluetile.png', 60],
    'Wooden': ['wood.png', 80],
    'Plain Pink': ['pinkish.png', 40],
    'Red Check': ['redCheckered.png', 50],
    'Plain Purple': ['purple.png', 40],
    'Plain Green': ['green.png', 50],
    'Raindbow': ['rainbow.png', 50],
    'Yellow Check': ['yellowCheck.png', 50]
}

frame_options_list = {
    'Blue': ['blue.png', 0],
    'Pink': ['pink.png', 50],
    'Wooden': ['wood.png', 80],
    'Green': ['green.png', 50],
    'White': ['white.png', 50],
    'Red': ['red.png', 50],
    'Yellow': ['yellow.png', 50],
    'Purple': ['purple.png', 50],
    'Mint': ['mint.png', 50],
    'Dark Blue': ['darkBlue.png', 50]
}

decor_options_list = {
    'None': ['none.png', 0],
    'Chalkboard': ['chalkboard.png', 45],
    'Cupcake Painting': ['painting.png', 55],
    'Whiteboard': ['whiteboard.png', 45],
    'TV': ['tv.png', 60],
    'Kafe Poster': ['kafePoster.png', 15],
    'Lemon Painting': ['lemon.png', 55],
    'Water Lillies': ['lillies.png', 55],
    'Stupid Poster': ['doughPoster.png', 15],
    'Stupid Poster 2': ['donutPoster.png', 15],
}

knick_knacks_options_list = {
    'None': ['none.png', 0],
    'Coffee': ['coffee.png', 5],
    'Plant': ['plant.png', 22],
    'Flowers': ['flowers.png', 20],
    'Framed Picture': ['picture.png', 10],
    'Cake Stand': ['cake.png', 28],
    'Mixer': ['mixer.png', 40],
    'Cupcake': ['cupcake.png', 2],
    'Candles': ['candles.png', 11],
    'Cookie Jar': ['cookie.png', 8]
}

furniture_options_list = {
    'None': ['none.png', 0],
    'Orange Tables': ['orange.png', 200],
    'White Tables': ['white.png', 200],
    'Blue Tables': ['blue.png', 200],
    'Green Tables': ['green.png', 200],
    'Pink Tables': ['pink.png', 200],
    'Yellow Tables': ['yellow.png', 200],
    'Red Tables': ['red.png', 200],
    'Purple Tables': ['purple.png', 200],
    'Wood Tables': ['wood.png', 220],
}

item_inventory = {
    'walls': ['Green'],
    'floors': ['White Check'],
    'frames': ['Blue'],
    'decor': ['None'],
    'furniture': ['None'],
    'knickKnacks': ['None'],
}

### CUSTOMERS ###
# customer names and png names
customers_list = {
    "Winslow": "winslow.png",
    "Mom": "mom.png",
    "Michela": "michela.png",
    "Maddie": "maddie.png",
    "Anna": "anna.png",
    "Zorro": "zorro.png",
    "Bikini": "bikini.png",
}

# food name and price
food_and_prices_list = {
    "Berry Muffin": 4.10, 
    "Cupcake": 4.20,
    "Cinnamon Roll": 3.50,
    "Banana Bread": 5.00,
    "Baguette": 7.00,
    "Donut": 3.70,
    "Cookie": 3.80,
    "Roll": 3.50,
    "Pretzel": 4.40,
    "Slice of Cake": 5.20,
    "Slice of Pie": 5.1,
    "Velvet Muffin": 4.10,
    "Eclair": 4.8,
    "Croissant": 4.8
}

order_bag_imgs = [
    pygame.image.load('graphics/kitchen/bag1.png'),
    pygame.image.load('graphics/kitchen/bag2.png'),
    pygame.image.load('graphics/kitchen/bag3.png'),
    pygame.image.load('graphics/kitchen/bag4.png'),
]