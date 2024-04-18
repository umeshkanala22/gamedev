import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from player import Player

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((1080, 648))
pygame.display.set_caption("Industry Fix")

# Load the map
level_1_map = load_pygame("assets/level_1.tmx")
background_image = level_1_map.get_layer_by_name("background").image
background_image = pygame.transform.scale(background_image, (1080, 648))
tilewidth = level_1_map.tilewidth
tileheight = level_1_map.tileheight

def render_level_1_map():
    screen.blit(background_image, (0, 0))
    for layer in level_1_map.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, tile in layer.tiles():
                tile = pygame.transform.scale(tile, (tilewidth * 2, tileheight * 2))
                if tile:
                    screen.blit(tile, (x * tilewidth * 2, y * tileheight * 2))

def main():
    clock = pygame.time.Clock()
    player = Player()
    all_sprites = pygame.sprite.Group(player)

    landed = False


    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.rect.x -= 2
            player.action = "left_walk"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.rect.x += 2
            player.action = "right_walk"
        # elif keys[pygame.K_UP] or keys[pygame.K_w]:
        #     player.action = "jump"
        #     player.jump()
        else:
            player.action = "idle"

        # Fill the screen with white
        render_level_1_map()

        all_sprites.update()

        player.apply_gravity()

        if not landed:
            for layer in level_1_map.layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    if layer.name == "base":
                        for x, y, tile in layer.tiles():
                            tile_rect = pygame.Rect(x * tilewidth * 2, y * tileheight * 2, tilewidth * 2, tileheight * 2)
                            if player.rect.colliderect(tile_rect):
                                player.gravity = 0
                                landed = True
                            # print(player.rect.bottom, tile_rect.top)
                        # if player.rect.left > tile_rect.right:
                            # player.rect.x = tile_rect.right
                            # player.gravity = 3

        if landed:
            for layer in level_1_map.layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    if layer.name == "base":
                        for x, y, tile in layer.tiles():
                            tile_rect = pygame.Rect(x * tilewidth * 2, y * tileheight * 2, tilewidth * 2, tileheight * 2)
                            keys = pygame.key.get_pressed()
                            # check if down arrow or s is pressed
                            if player.rect.left > 36*9 and player.rect.bottom < 36*13 + 2 and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                                player.gravity = 2
                                landed = False
                            else:
                                player.gravity = 0
                                landed = True
        


        all_sprites.draw(screen)

        # Update the screen
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()