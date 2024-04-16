import pygame
from player import Submarine, Bubble, Ship
from trash import Trash
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from utils import Button
import time

# Initialize the game
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ocean Cleanup")

# Setup clock
clock = pygame.time.Clock()

# In your main game loop
all_sprites = pygame.sprite.Group()
trash_group = pygame.sprite.Group()
net_group = pygame.sprite.Group()
bubble_group = pygame.sprite.Group()

submarine = Submarine(all_sprites, net_group, bubble_group)
all_sprites.add(submarine)
ship = Ship(net_group, trash_group)

# Variable to track whether a net has been fired recently
net_fired = False

# Variable to track count of missed trash
missed_trash_count = 0
missed_net_count = 0

# Variable to track the score
score = 0
completion = False

# stage complete target
score_target = 5

# font for game over text
font = pygame.font.SysFont(None, 72)

# font for score text
score_font = pygame.font.SysFont(None, 36)

# font for stage complete text
stage_complete_font = pygame.font.SysFont(None, 72)

# Water color stages
water_colors = [
    (69, 89, 78),  # dirtiest water
    (104, 133, 115),
    (138, 178, 154),
    (162, 193, 175),
    (67, 179, 229),
    (56, 165, 222),
    (42, 152, 213),
    (20, 135, 200),
]

# last collision time (trash and submarine)
last_collision_time = 0

# last bubble time
last_bubble_time = time.time()

# Create initial trash
minimum_trash = 5
for i in range(5):
    trash = Trash()
    all_sprites.add(trash)
    trash_group.add(trash)

running = True
game_over = False
is_paused = False  # Initialize pause state
is_fullscreen = False  # Initialize full screen state

stage_2_setup = False

game_stage = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for shift key press to toggle pause
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
            is_paused = not is_paused

        # Check for spacebar press to fire net
        if (
            not net_fired
            and not is_paused
            and not game_over
            and event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
            and game_stage == 1
        ):
            submarine.fire_net()
            net_fired = True

        # Check for spacebar release
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            net_fired = False

        # Check for F key press to toggle full screen
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            is_fullscreen = not is_fullscreen
            if is_fullscreen:
                screen = pygame.display.set_mode(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN
                )
            else:
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Fill 20% sky and then 80% water
    stage = min(score // 2, len(water_colors) - 1)  # Determine stage based on score
    water_color = water_colors[stage]

    # Fill 20% sky and then 80% water
    sky_image = pygame.image.load("assets/sky.jpg").convert_alpha()
    sky_image = pygame.transform.scale(
        sky_image, (SCREEN_WIDTH, int(SCREEN_HEIGHT * 0.3))
    )
    screen.blit(sky_image, (0, 0))
    pygame.draw.rect(
        screen,
        water_color,
        pygame.Rect(0, SCREEN_HEIGHT * 0.3, SCREEN_WIDTH, SCREEN_HEIGHT),
    )

    # Render score text
    score_text = score_font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    if game_stage == 1:
        if (
            not is_paused and not game_over and not completion
        ):  # Only update and draw if game is not paused and not over
            all_sprites.update()


            # Check for collisions between trash and nets using masks
            for trash in trash_group:
                for net in net_group:
                    if (
                        pygame.sprite.collide_mask(trash, net)
                        and trash.status != "missed"
                        and net.status != "missed"
                    ):
                        trash.kill()
                        net.kill()
                        score += 1

            # create bubble every 3 seconds
            if time.time() - last_bubble_time >= 1:
                submarine.release_bubble()
                last_bubble_time = time.time()

            # Check for collisions between trash and submarine using masks
            for trash in trash_group:
                if (
                    pygame.sprite.collide_mask(trash, submarine)
                    and trash.status != "missed"
                ):
                    trash.kill()
                    # slow down the submarine
                    submarine.speed -= 1.5
                    last_collision_time = pygame.time.get_ticks()

            # Check if the submarine has been slowed down for 5 seconds
            if pygame.time.get_ticks() - last_collision_time >= 5000:
                if submarine.speed < 5:
                    if submarine.speed + 1 <= 5:
                        submarine.speed += 1
                    else:
                        submarine.speed = 5

            # update minimum trash
            minimum_trash = 5 + score // 5

            # create new trash if less than 5 trash on screen
            if len(trash_group) < minimum_trash:
                trash = Trash()
                all_sprites.add(trash)
                all_sprites.add(trash)
                trash_group.add(trash)

            # Check for missed trash
            for trash in trash_group:
                if trash.rect.bottom == SCREEN_HEIGHT and trash.status != "missed":
                    missed_trash_count += 1
                    trash.status = "missed"
                    # trash.kill()

            # Check for missed net
            for net in net_group:
                if net.rect.top == 0.3 * SCREEN_HEIGHT - 10 and net.status != "missed":
                    missed_net_count += 1
                    net.status = "missed"
                    # net.kill()

            if missed_trash_count >= 5 or missed_net_count >= 5:
                game_over = True

            if score >= score_target:
                completion = True

    if game_stage == 2:
        if (
            not is_paused and not game_over and not completion
        ):
            if ship.rect.left > 150:
                ship.update()
            else:
                if not submarine:
                    ship.rect.x += 1.5

            bubble_group.update()
            # remove all inactive trash
            if stage_2_setup == False:
                stage_2_setup = True
                all_sprites.add(ship)

            if submarine:
                if submarine.rect.left < SCREEN_WIDTH:
                    submarine.rect.x += 1.5
                else:
                    submarine.kill()
                    submarine = None

            
            # settle down the nets to the ocean floor
            for net in net_group:
                if net.status != "settled":
                    net.rect.y += 1
                if net.rect.bottom > SCREEN_HEIGHT:
                    net.rect.bottom = SCREEN_HEIGHT
                    net.status = "settled"

            # settle down the trash to the ocean floor
            for trash in trash_group:
                if trash.status != "settled":
                    trash.rect.y += 1
                if trash.rect.bottom > SCREEN_HEIGHT:
                    trash.rect.bottom = SCREEN_HEIGHT
                    trash.status = "settled"

    all_sprites.draw(screen)

    if completion:
        # Render "Level Complete" text
        text = "STAGE COMPLETE"
        game_over_text = font.render(text, True, (0, 255, 0))
        text_rect = game_over_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )
        screen.blit(game_over_text, text_rect)

        # create a button to quit
        quit_button = Button(
            SCREEN_WIDTH // 2 - 50,
            SCREEN_HEIGHT // 2 + 50,
            100,
            50,
            "QUIT",
            (0, 0, 0),
            font,
            (255, 255, 255),
            24,
        )
        quit_button.draw(screen)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if quit_button.is_clicked(pos):
                running = False

        # create a button to continue
        continue_button = Button(
            SCREEN_WIDTH // 2 - 50,
            SCREEN_HEIGHT // 2 + 125,
            300,
            50,
            "CONTINUE",
            (0, 0, 0),
            font,
            (65, 176, 110),
            24,
        )
        continue_button.draw(screen)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if continue_button.is_clicked(pos):
                completion = False
                game_stage = 2

    if game_over or is_paused:
        # Render "Game Over" or "Paused" text
        if game_over:
            text = "GAME OVER"
        else:
            text = "PAUSED"
        game_over_text = font.render(text, True, (255, 0, 0))
        text_rect = game_over_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )
        screen.blit(game_over_text, text_rect)

        quit_button = Button(
            SCREEN_WIDTH // 2 - 50,
            SCREEN_HEIGHT // 2 + 50,
            100,
            50,
            "QUIT",
            (0, 0, 0),
            font,
            (255, 255, 255),
            24,
        )
        quit_button.draw(screen)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if quit_button.is_clicked(pos):
                running = False

    pygame.display.flip()
    clock.tick(60)
