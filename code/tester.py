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
tmx_file_path = '/home/silversage22/Desktop/sem4/COP290/game/data/tsx/level1.tmx'  # Replace with your TMX file path
tmx_data = pytmx.load_pygame(tmx_file_path, pixelalpha=True)

# Camera class to handle movement and zooming
class Camera:
    def __init__(self, screen_width, screen_height, scale_factor=1.0):
        self.camera = pygame.Rect(0, 0, screen_width, screen_height)
        self.scale_factor = scale_factor

    def apply(self, target_rect):
        # Apply the camera offset and scaling to the target rect
        return target_rect.move(-self.camera.x, -self.camera.y).inflate(self.scale_factor, self.scale_factor)

    def update(self, target):
        # Center the camera on the target (e.g., player) and adjust zoom
        self.camera.center = target.center
        self.camera.width = int(screen_width * self.scale_factor)
        self.camera.height = int(screen_height * self.scale_factor)

# Create a camera object
camera = Camera(screen_width, screen_height)

# Function to draw the TMX map
def draw_map(screen, tmx_data, camera):
    # Draw tile layers
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, tile in layer.tiles():
                if tile:
                    # Calculate the position with respect to the camera and zoom
                    pos = camera.apply(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    screen.blit(pygame.transform.scale(tile, (int(TILE_SIZE * camera.scale_factor), int(TILE_SIZE * camera.scale_factor))), pos)
    
    # Draw object layers
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledObjectGroup):
            for obj in layer:
                if obj.image:  # If the object is an image
                    # Calculate the position with respect to the camera and zoom
                    pos = camera.apply(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                    screen.blit(pygame.transform.scale(obj.image, (int(obj.width * camera.scale_factor), int(obj.height * camera.scale_factor))), pos)
                elif obj.name:
                    # You can add additional handling for different object types here
                    # For example, drawing shapes (rectangles, ellipses, etc.) or text
                    pass

# Main game loop
running = True
clock = pygame.time.Clock()

# Set initial target (e.g., player or a point of interest) to center the camera
target = pygame.Rect(400, 300, TILE_SIZE, TILE_SIZE)  # This is just an example; you can use your player object

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Adjust zoom with '+' and '-' keys
            if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                camera.scale_factor *= 1.1  # Increase zoom
            elif event.key == pygame.K_MINUS:
                camera.scale_factor /= 1.1  # Decrease zoom
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Update the camera based on the target position
    camera.update(target)
    
    # Draw the TMX map using the camera
    draw_map(screen, tmx_data, camera)
    
    # Update the display
    pygame.display.flip()
    
    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

