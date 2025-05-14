import random
import math
import sys
import pygame
from pygame import mixer

pygame.init()

# Set display
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Space Shooter")

# Score, Lives, and Level
score = 0
lives = 3
level = 1
font = pygame.font.Font("freesansbold.ttf", 32)

def show_stats():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
    level_text = font.render(f"Level: {level}", True, (0, 255, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    screen.blit(level_text, (10, 90))

# Icon
icon = pygame.image.load('gallery/galaxy.png')
pygame.display.set_icon(icon)

# Background
bg = pygame.image.load('gallery/background.jpg')
def back():
    screen.blit(bg, (0, 0))

# Sound
mixer.music.load("gallery/background.wav")
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('gallery/player.png')
playerX = 640
playerY = 600
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x - 16, y + 10))

# Bullet
bulletImg = pygame.image.load('gallery/bullet.png')
bulletX = 0
bulletY = 600
bulletY_change = 4
bullet_state = "ready"

def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_enemy = 7
for i in range(num_enemy):
    enemyImg.append(pygame.image.load('gallery/enemy.png'))
    enemyX.append(random.randint(0, 1216))
    enemyY.append(random.randint(100, 150))
    enemyX_change.append(2)
    enemyY_change.append(30)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def isCollision(enemyX, enemyY, bulletX, bulletY, i):
    distance = math.sqrt((math.pow(enemyX[i] - bulletX, 2)) + (math.pow(enemyY[i] - bulletY, 2)))
    return distance < 27

# Game Over
font_big = pygame.font.Font("freesansbold.ttf", 50)
def game_over():
    over_text = font_big.render("GAME OVER", True, (255, 99, 71))
    screen.blit(over_text, (500, 370))

# Game loop
running = True
game_ended = False

while running:
    screen.fill((0, 0, 0))
    back()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_ended:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    playerX_change = 0.4
                if event.key == pygame.K_a:
                    playerX_change = -0.4
                if event.key == pygame.K_l:
                    if bullet_state == "ready":
                        bulletSound = mixer.Sound("gallery/laser.wav")
                        bulletSound.play()
                        bulletX = playerX
                        bullet_fire(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_d, pygame.K_a):
                    playerX_change = 0

    if not game_ended:
        playerX += playerX_change
        playerX = max(0, min(playerX, 1216))
        player(playerX, playerY)

        for i in range(num_enemy):
            if enemyX[i] <= 0:
                enemyX_change[i] = 1
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 1216:
                enemyX_change[i] = -1
                enemyY[i] += enemyY_change[i]

            if isCollision(enemyX, enemyY, bulletX, bulletY, i):
                explosionSound = mixer.Sound("gallery/explosion.wav")
                explosionSound.play()
                bulletY = 600
                bullet_state = "ready"
                enemyX[i] = random.randint(0, 1216)
                enemyY[i] = random.randint(100, 150)
                score += 1

                if score % 10 == 0:
                    level += 1
                    for j in range(num_enemy):
                        enemyX_change[j] += 0.5

            if enemyY[i] > 550:
                lives -= 1
                enemyY[i] = random.randint(100, 150)
                enemyX[i] = random.randint(0, 1216)

            enemyX[i] += enemyX_change[i]
            enemy(enemyX[i], enemyY[i], i)

        if bullet_state == "fire":
            bullet_fire(bulletX, bulletY)
            bulletY -= bulletY_change
            if bulletY <= 0:
                bulletY = 600
                bullet_state = "ready"

        show_stats()

        if lives <= 0:
            game_ended = True
            game_over()

    else:
        #show player game over text
        player(playerX, playerY)
        game_over()

    pygame.display.update()

# Keep window open until user closes it
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
