from pygame.math import Vector2
# screen
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000
TILE_SIZE = 32


LAYERS = {
    'base' :1,
    'water':2,
    'road' :3,
    
    'fence':5,
    'Interactable' :6,
    'base2':4,
    
        

}

APPLE_POS = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

GROW_SPEED = {
	'corn': 1,
	'tomato': 0.7
}

SALE_PRICES = {
	'wood': 4,
	'apple': 2,
	'corn': 10,
	'tomato': 20
}
PURCHASE_PRICES = {
	'corn': 4,
	'tomato': 5
}
