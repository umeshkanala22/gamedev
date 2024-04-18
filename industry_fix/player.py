import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        images_path = "assets/alien_green/"
        idle_states = ["green__0000_idle_1.png", "green__0001_idle_2.png", "green__0002_idle_3.png"]
        turn_states = ["green__0003_turn_1.png", "green__0004_turn_2.png", "green__0005_turn_3.png"]
        right_walk_states = ["green__0006_walk_1.png", "green__0007_walk_2.png", "green__0008_walk_3.png", "green__0009_walk_4.png", "green__0010_walk_5.png", "green__0011_walk_6.png"]
        left_walk_states = ["flip_green__0006_walk_1.png", "flip_green__0007_walk_2.png", "flip_green__0008_walk_3.png", "flip_green__0009_walk_4.png", "flip_green__0010_walk_5.png", "flip_green__0011_walk_6.png"]
        run_states = ["green__0012_run_1.png", "green__0013_run_2.png", "green__0014_run_3.png", "green__0015_run_4.png", "green__0016_run_5.png", "green__0017_run_6.png"]
        jump_states = ["green__0027_jump_1.png", "green__0028_jump_2.png", "green__0029_jump_3.png", "green__0030_jump_4.png"]

        new_width = 25
        new_height = 50
        # Load and resize the images
        self.idle_images = [pygame.transform.scale(pygame.image.load(images_path + image), (new_width, new_height)) for image in idle_states]
        self.turn_images = [pygame.transform.scale(pygame.image.load(images_path + image), (new_width, new_height)) for image in turn_states]
        self.right_walk_images = [pygame.transform.scale(pygame.image.load(images_path + image), (new_width, new_height)) for image in right_walk_states]
        self.left_walk_images = [pygame.transform.scale(pygame.image.load(images_path + image), (new_width, new_height)) for image in left_walk_states]
        self.run_images = [pygame.transform.scale(pygame.image.load(images_path + image), (new_width, new_height)) for image in run_states]
        self.jump_images = [pygame.transform.scale(pygame.image.load(images_path + image), (new_width, new_height)) for image in jump_states]

        self.image = self.idle_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

        self.animation_index = 0
        self.animation_speed = 5
        self.animation_counter = 0

        self.action = "idle"
        self.gravity = 3
        self.vel_y = 0

    def update(self):
        if self.action == "idle":
            self.animate(self.idle_images)
        elif self.action == "turn":
            self.animate(self.turn_images)
        elif self.action == "left_walk":
            self.animate(self.left_walk_images)
        elif self.action == "right_walk":
            self.animate(self.right_walk_images)
        elif self.action == "run":
            self.animate(self.run_images)
        elif self.action == "jump":
            self.animate(self.jump_images)

    def animate(self, images):
        if self.action == "idle":
            # if idle, wait once the animation is finished
            self.animation_speed = 10
            # if self.animation_index == 0:
            #     pygame.time.wait(300)
        else:
            self.animation_speed = 5
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.animation_index = (self.animation_index + 1) % len(images)
            self.image = images[self.animation_index]

    def apply_gravity(self):
        self.rect.y += self.gravity