import pygame
import random

# Constants
WIDTH = 640
HEIGHT = 480
GAP = 100
PIPE_HEIGHT = 150
GROUND_HEIGHT = 80  # Adjust this value according to your ground image

# Images
img_back = "bg.png"
img_bird = "bird.png"
img_bird_up = "bird-up.png"
img_bird_down = "bird-down.png"
img_pipe = "pipe.png"
img_pipe1 = "pipe1.png"
img_ground = "ground.png"
img_first_kid = "first-kid.png"

# Initialize Pygame
pygame.init()

# Window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Background
background = pygame.transform.scale(pygame.image.load(img_back), (WIDTH, HEIGHT))

# Ground
ground = pygame.image.load(img_ground)
ground_rect = ground.get_rect(midtop = (WIDTH // 2, HEIGHT - GROUND_HEIGHT))

class Bird(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = {
            "up": pygame.image.load(img_bird_up),
            "down": pygame.image.load(img_bird_down),
            "normal": pygame.image.load(img_bird)
        }
        self.image = self.images["normal"]
        self.rect = self.image.get_rect(center = (x, y))
        self.y_speed = 0

    def update(self):
        self.y_speed += 0.5
        self.rect.centery += self.y_speed
        if self.rect.centery >= HEIGHT - GROUND_HEIGHT - self.rect.height // 2:  # Adjust bird's position
            self.rect.centery = HEIGHT - GROUND_HEIGHT - self.rect.height // 2
        if self.rect.centery <= 0:  # Prevent bird from going off the top of the screen
            self.rect.centery = 0
        if self.y_speed < 0:
            self.image = self.images["up"]
        elif self.y_speed > 0:
            self.image = self.images["down"]
        else:
            self.image = self.images["normal"]

    def jump(self):
        self.y_speed = -10

class Pipe(pygame.sprite.Sprite):
    def __init__(self, img, x, y, is_top):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(midbottom = (x, y)) if is_top else self.image.get_rect(midtop = (x, y))
        self.speed = 5

    def update(self):
        self.rect.centerx -= self.speed
        if self.rect.right < 0:  # If the pipe has gone off the screen
            self.kill()  # Remove the pipe

def spawn_pipes():
    y = random.randint(100, HEIGHT - 100 - PIPE_HEIGHT - GROUND_HEIGHT)  # Adjusted y-value for the gap between pipes
    top_pipe = Pipe(img_pipe, WIDTH, y, True)
    bottom_pipe = Pipe(img_pipe1, WIDTH, y + PIPE_HEIGHT, False)
    pipes.add(top_pipe, bottom_pipe)

# Bird
bird = Bird(img_bird, 50, HEIGHT // 2)

# Pipes
pipes = pygame.sprite.Group()
spawn_pipes()  # Spawn the initial pipes

# Game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    if not run:  # If the game is over
        break

    window.blit(background, (0, 0))

    bird.update()
    window.blit(bird.image, bird.rect)

    pipes.update()
    for pipe in pipes:
        window.blit(pipe.image, pipe.rect)

    window.blit(ground, ground_rect)

    if pygame.sprite.spritecollideany(bird, pipes):
        run = False

    if not pipes:  # If all pipes have been removed
        spawn_pipes()  # Spawn new pipes

    pygame.display.update()
    pygame.time.Clock().tick(120)

pygame.quit()
