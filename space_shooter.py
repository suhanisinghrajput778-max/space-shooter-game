#Space Shooter Game
#language: python 3 | Library: Pygame
#Concepts: Classes/ Objects, Lists, if/elif/else, collision Detection

import pygame
import random

pygame.init()

# ---------- Window settings ----------
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 48)

# ---------- Ship class ----------
class Ship:
    def __init__(self):
        self.x = 275   #starting x position
        self.y = 520   #ship stays at y = 520
        self.width = 50
        self.height= 50
        self.speed = 8   # moves 8 px per key presss 

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:    # do not go outside the window
            self.x = 0

    def move_right(self):
        self.x += self.speed
        if self.x > WIDTH - self.width:    # max x = 550
            self.x = WIDTH - self.width

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, (0, 200, 255), self.rect())

# ---------- Bullet class ----------
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.speed = 10   # moves 10 px upward per frame

    def move(self):
        self.y -= self.speed

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 0), self.rect())
# ---------- Enemy class ----------
class Enemy:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, WIDTH - self.width) 
        self.y = 0
        self.speed = 2 

    def move(self):
        self.y += self.speed

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, (255, 60, 60), self.rect())

# ---------- Game variables ----------
ship = Ship()
bullets = []    # list of Bullet objects (max 5)
enemies = []    #list of Enemy objects
score = 0
lives = 3
spawn_timer = 0
game_over = False
running = True

# ----------- Main game loop -----------
while running:
    clock.tick(60)  # 60 frames per second

    # ----- Events -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                # Fire only if less than 5 bullets are on screen
                if len(bullets) < 5:
                    bullet_x = ship.x + 25
                    bullet_y = ship.y
                    bullets.append(Bullet(bullet_x, bullet_y))

    if not game_over:
        # ----- Ship movement -----
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ship.move_left()
        elif keys[pygame.K_RIGHT]:
            ship.move_right()

        # ----- Spawn enemies -----
        spawn_timer += 1
        if spawn_timer >=60:   # a new enemy every 1 second  
            enemies.append(Enemy())
            spawn_timer = 0

        # ----- Move bullets ------
        for bullet in bullets[:]:
            bullet.move()
            if bullet.y < -10:   # bullet left the screen
                bullets.remove(bullet)

        # ----- Move enemies -----
        for enemy in enemies[:]:
            enemy.move()
            if enemy.y >= HEIGHT:   #enemy reached the bottom (y = 600)
                enemies.remove(enemy)
                lives -= 1
                if lives <= 0:
                    game_over = True

        # ----- Collision detection -----
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.rect().colliderect(enemy.rect()):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10
                    break           # this bullet is finished

    # ----- Drawing -----
    screen.fill((10, 10, 40))
    ship.draw()
    for bullet in bullets:
        bullet.draw()
    for enemy in enemies:
        enemy.draw()

    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    lives_text = font.render("Lives: " + str(lives), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 110, 10))

    if game_over:
        over_text = big_font.render("GAME OVER", True, (255, 80, 80))
        final_text = font.render("Final Score: " + str(score), True, (255, 255, 255))
        screen.blit(over_text, (150, 250))
        screen.blit(final_text, (210,320))

    pygame.display.flip()

pygame.quit()    



