import pygame
from player import Submarine, SpaceShip
from trash import Trash
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from utils import Button
import time
import sys

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
spaceship = SpaceShip(all_sprites)


# Variable to track whether a net has been fired recently
net_fired = False
beam_fired = False

# Variable to track count of missed trash
missed_trash_count = 0
missed_net_count = 0

# Variable to track the score
score = 0
completion = False

# stage complete target
score_target = 50

# font for game over text
font = pygame.font.SysFont(None, 72)

# font for score text
score_font = pygame.font.SysFont(None, 36)

# font for stage complete text
stage_complete_font = pygame.font.SysFont(None, 72)


def start_screen(screen):
    # Constants
    WIDTH, HEIGHT = 800, 600
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    FONT_SIZE = 30

    # Font for displaying the text
    font = pygame.font.Font(None, FONT_SIZE)

    # Fill the screen with the background color
    screen.fill(BLACK)

    # Introduction text
    intro_text = [
        "Welcome to Ocean Cleanup Submarine!",
        "The ocean is in desperate need of your help to clear the garbage.",
        "Pilot your submarine and rid the ocean of pollution!",
        "",
        "----------------------------------------------------------------------------------------------",
        "Instructions:",
        "- Use the ARROW keys to navigate your submarine.",
        "- Press SPACE to fire nets and collect garbage.",
        "----------------------------------------------------------------------------------------------",
        "",
        "Press any key to start cleaning...",
        "",
    ]

    # Render and display the introduction text
    y_position = HEIGHT // 4
    for line in intro_text:
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, y_position))
        screen.blit(text, text_rect)
        y_position += FONT_SIZE

    pygame.display.flip()

    # Wait for a key press to start the game
    # wait for 2 seconds
    time.sleep(2)
    wait_for_key()


def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False


def show_text_on_screen(screen, text, font_size, y_position):
    font = pygame.font.Font(None, font_size)
    text_render = font.render(text, True, (255, 255, 255))
    text_rect = text_render.get_rect(center=(SCREEN_WIDTH // 2, y_position))
    screen.blit(text_render, text_rect)


def game_over_screen(screen):
    screen.fill((0, 0, 0))  # Fill the screen with black
    show_text_on_screen(screen, "Game Over", 50, SCREEN_HEIGHT // 3)
    show_text_on_screen(screen, f"Your final score: {score}", 30, SCREEN_HEIGHT // 2)
    show_text_on_screen(screen, "Press any key to exit...", 20, SCREEN_HEIGHT * 2 // 3)
    pygame.display.flip()
    wait_for_key()


def game_paused_screen(screen):
    screen.fill((0, 0, 0))  # Fill the screen with black
    show_text_on_screen(screen, "Game Paused", 50, SCREEN_HEIGHT // 3)
    show_text_on_screen(screen, "Press SHIFT to resume...", 30, SCREEN_HEIGHT // 2)
    pygame.display.flip()

def stage_one_complete_screen(screen):
    screen.fill((0, 0, 0))  # Fill the screen with black
    stage_2_info_1 = "Press SPACE to fire tractor beam from spaceship and"
    stage_2_info_2 = "collect garbage from the ocean floor."
    show_text_on_screen(screen, "Stage 1 Complete!", 50, SCREEN_HEIGHT // 3)
    show_text_on_screen(screen, stage_2_info_1, 30, SCREEN_HEIGHT // 2)
    show_text_on_screen(screen, stage_2_info_2, 30, SCREEN_HEIGHT // 2 + 40)
    show_text_on_screen(screen, "Press any key to continue...", 20, SCREEN_HEIGHT * 2 // 3)
    pygame.display.flip()
    time.sleep(1)
    wait_for_key()

def victory_screen(screen):
    screen.fill((0, 0, 0))  # Fill the screen with black
    show_text_on_screen(screen, "Congratulations!", 50, SCREEN_HEIGHT // 3)
    show_text_on_screen(
        screen,
        f"You've completed all levels with a score of {score}",
        30,
        SCREEN_HEIGHT // 2,
    )
    show_text_on_screen(screen, "Press any key to exit...", 20, SCREEN_HEIGHT * 2 // 3)
    pygame.display.flip()
    wait_for_key()


RED = (255, 0, 0)
YELLOW = (255, 255, 0)

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

start_screen(screen)

running = True
game_over = False
is_paused = False  # Initialize pause state
is_fullscreen = False  # Initialize full screen state

stage_2_setup = False
ship_setup = False

game_stage = 1

while running:
    # Fill 20% sky and then 80% water
    sky_image = pygame.image.load("assets/sky.jpg").convert_alpha()
    sky_image = pygame.transform.scale(
        sky_image, (SCREEN_WIDTH, int(SCREEN_HEIGHT * 0.3))
    )

    # Fill 20% sky and then 80% water
    stage = min(score // 5, len(water_colors) - 1)  # Determine stage based on score
    water_color = water_colors[stage]

    screen.blit(sky_image, (0, 0))
    pygame.draw.rect(
        screen,
        water_color,
        pygame.Rect(0, SCREEN_HEIGHT * 0.3, SCREEN_WIDTH, SCREEN_HEIGHT),
    )
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

        if game_stage == 2 and not is_paused and not game_over and not completion:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # print("Firing tractor beam")
                tractor_beam = pygame.rect.Rect(
                    spaceship.rect.centerx,
                    spaceship.rect.centery,
                    4,
                    SCREEN_HEIGHT - spaceship.rect.centery,
                )
                pygame.draw.line(
                    screen,
                    YELLOW,
                    (spaceship.rect.centerx, spaceship.rect.centery),
                    (spaceship.rect.centerx, SCREEN_HEIGHT),
                    2,
                )
                # all_sprites.add(tractor_beam)
                # beam_fired = True

                # check for collisions between trash and beam
                for trash in trash_group:
                    if tractor_beam.colliderect(trash):
                        pygame.draw.line(
                            screen,
                            YELLOW,
                            (spaceship.rect.centerx, spaceship.rect.centery),
                            (spaceship.rect.centerx, trash.rect.bottom),
                            2,
                        )
                        # mark target as red
                        pygame.draw.rect(screen, RED, trash.rect)
                        trash.kill()
                        score += 1

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
        if not is_paused and not game_over and not completion:
            if ship_setup:
                spaceship.update()
            else:
                if not submarine:
                    spaceship.rect.x += 1.5
                if spaceship.rect.left >= 150:
                    ship_setup = True

            bubble_group.update()
            # remove all inactive trash
            if stage_2_setup == False:
                stage_2_setup = True
                all_sprites.add(spaceship)

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
                    trash_group.add(net)

            # settle down the trash to the ocean floor
            for trash in trash_group:
                if trash.status != "settled":
                    trash.rect.y += 1
                if trash.rect.bottom > SCREEN_HEIGHT:
                    trash.rect.bottom = SCREEN_HEIGHT
                    trash.status = "settled"

            if len(trash_group) == 0:
                completion = True

    all_sprites.draw(screen)

    if completion and game_stage == 1:
        stage_one_complete_screen(screen)
        game_stage = 2
        completion = False
    
    if completion and game_stage == 2:
        victory_screen(screen)
        running = False

    if game_over:
        game_over_screen(screen)
        running = False

    if is_paused:
        game_paused_screen(screen)

    pygame.display.flip()
    clock.tick(60)