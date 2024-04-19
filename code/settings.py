import pygame
from pygame.math import Vector2
import math
from os.path import join
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

LAYERS2 = {
    'constantterrrain':1,
    'movable_vertical':2,
    'movable_horizontal':3,
    'Deathlayer':4,
}


