from time import sleep

import pygame
from random import *

WIDTH = 640
HEIGHT = 480
GAP = 100
PIPE_HEIGHT = 150
GROUND_HEIGHT = 80
score = 8
speed = 3
shield = False

# Images
img_back = "bg.png"
img_bird = "bird.png"
img_bird_up = "bird-up.png"
img_bird_down = "bird-down.png"
img_bird_shield = "bird-shield.png"
img_bird_up_shield = "bird-up-shield.png"
img_bird_down_shield = "bird-down-shield.png"
img_pipe = "pipe.png"
img_pipe1 = "pipe1.png"
img_ground = "ground.png"
img_first_kid = "first-kid.png"
img_shield = "shield.png"
img_heart = "heart.png"

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

background = pygame.transform.scale(pygame.image.load(img_back), (WIDTH, HEIGHT))

ground = pygame.image.load(img_ground)
ground_rect = ground.get_rect(midtop = (WIDTH // 2, HEIGHT - GROUND_HEIGHT))


class Bird(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = {
            "up": pygame.image.load(img_bird_up),
            "down": pygame.image.load(img_bird_down),
            "normal": pygame.image.load(img_bird),
            "up_shield": pygame.image.load(img_bird_up_shield),
            "down_shield": pygame.image.load(img_bird_down_shield),
            "normal_shield": pygame.image.load(img_bird_shield)
        }
        self.image = self.images["normal"]
        self.rect = self.image.get_rect(center=(x, y))
        self.y_speed = 0

    def update(self):
        self.y_speed += 0.5
        self.rect.centery += self.y_speed
        if self.rect.centery >= HEIGHT - GROUND_HEIGHT - self.rect.height // 2:
            self.rect.centery = HEIGHT - GROUND_HEIGHT - self.rect.height // 2
        if self.rect.centery <= 0:
            self.rect.centery = 0
        if self.y_speed < 0:
            self.image = self.images["up"]
        elif self.y_speed > 0:
            self.image = self.images["down"]
        else:
            self.image = self.images["normal"]

        if shield==True:
            if self.y_speed < 0:
                self.image = self.images["up_shield"]
            elif self.y_speed > 0:
                self.image = self.images["down_shield"]
            else:
                self.image = self.images["normal_shield"]

    def jump(self):
        self.y_speed = -8

class Pipe(pygame.sprite.Sprite):
    def __init__(self, img, x, y, is_top):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(midbottom=(x, y)) if is_top else self.image.get_rect(midtop=(x, y))
        self.speed = speed
        self.is_scored = False

    def update(self):
        self.rect.centerx -= self.speed
        if self.rect.right < 0 and not self.is_scored:
            self.kill()

class Life(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(topleft=(x, y))

class FirstKid(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2

    def update(self):
        self.rect.centerx -= self.speed
        if self.rect.right < 0:
            self.kill()

class Shield(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3

    def update(self):
        self.rect.centerx -= self.speed
        if self.rect.right < 0:
            self.kill()

def spawn_pipes():
    y = randint(100, HEIGHT - 100 - PIPE_HEIGHT - GROUND_HEIGHT)
    top_pipe = Pipe(img_pipe, WIDTH, y, True)
    bottom_pipe = Pipe(img_pipe1, WIDTH, y + PIPE_HEIGHT, False)
    pipes.add(top_pipe, bottom_pipe)

bird = Bird(img_bird, 50, HEIGHT // 2)

pipes = pygame.sprite.Group()
spawn_pipes()

# Lives
lives = pygame.sprite.Group()
for i in range(3):
    life = Life(img_heart, 10 + i * 30, 10)
    lives.add(life)

first_kids = pygame.sprite.Group()
shields = pygame.sprite.Group()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
                print(score)
            if event.key == pygame.K_q:
                score -= 1

    if not run:
        break

    window.blit(background, (0, 0))

    bird.update()
    lives.update()
    first_kids.update()
    shields.update()
    pipes.update()

    window.blit(bird.image, bird.rect)

    for pipe in pipes:
        window.blit(pipe.image, pipe.rect)

    for life in lives:
        window.blit(life.image, life.rect)

    if len(pipes) % 5 == 0:
        score -= 1
    if score == 0:
        score += 8
        speed += 1

    if score == 6:
        if len(first_kids) == 0:
            first_kid = FirstKid(img_first_kid, 600, 385)  # <--- changed
            first_kids.add(first_kid)
    if score == 4:
        if len(shields) == 0:
            shield = Shield(img_shield, 600, 385)  # <--- changed
            shields.add(shield)
    if score == 2:
        if len(first_kids) == 0:
            first_kid = FirstKid(img_first_kid, 600, 385)  # <--- changed
            first_kids.add(first_kid)
    if score == 0:
        if len(first_kids) == 0:
            first_kid = FirstKid(img_first_kid, 600, 385)  # <--- changed
            first_kids.add(first_kid)

    for first_kid in first_kids:
        window.blit(first_kid.image, first_kid.rect)

    for shield in shields:
        window.blit(shield.image, shield.rect)

    if pygame.sprite.spritecollideany(bird, first_kids):
        if len(lives) < 3:
            life = Life(img_heart, 10 + len(lives) * 30, 10)
            lives.add(life)
        first_kids.empty()

    if pygame.sprite.spritecollideany(bird, shields):
        shield = True
        shields.empty()

    window.blit(ground, ground_rect)

    collided_pipes = pygame.sprite.spritecollide(bird, pipes, False)
    if collided_pipes:
        if shield:
            for pipe in collided_pipes:
                pipe.kill()
            shield = False
        elif len(lives) > 1:
            lives.sprites()[-1].kill()
            for pipe in collided_pipes:
                pipe.kill()
        else:
            run = False

    if not pipes:
        spawn_pipes()

    pygame.display.update()
    pygame.time.Clock().tick(90)

pygame.quit()