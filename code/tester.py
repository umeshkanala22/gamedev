import pygame
import pytmx
import os

# Constants
TILE_SIZE = 32  # Set this to your desired tile size

# Initialize Pygame
pygame.init()

# Create a screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the TMX map file using pytmx
tmx_file_path = '/home/silversage22/Desktop/sem4/COP290/game/data/tsx/level1.tmx'  
# Replace with your TMX file path
tmx_data = pytmx.load_pygame(tmx_file_path, pixelalpha=True)

# Function to draw the TMX map
def draw_map(screen, tmx_data):
    # Draw tile layers
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, tile in layer.tiles():
                if tile:
                    screen.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))
    
    # Draw object layers
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledObjectGroup):
            for obj in layer:
                if obj.image:  # If the object is an image
                    screen.blit(obj.image, (obj.x, obj.y))
                elif obj.name:
                    # You can add additional handling for different object types here
                    # For example, drawing shapes (rectangles, ellipses, etc.) or text
                    pass

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the TMX map
    draw_map(screen, tmx_data)
    
    # Update the display
    pygame.display.flip()
    
    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
