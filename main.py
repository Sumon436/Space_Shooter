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

# Icon and Background
icon = pygame.image.load('gallery/galaxy.png')
pygame.display.set_icon(icon)
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

# Player boundaries
PLAYER_MIN_X = 0
PLAYER_MAX_X = 1216

player_visible = True
player_exploding = False
player_explosion_timer = 0

# Invincibility after hit
invincible = False
invincible_timer = 0
INVINCIBLE_DURATION = 120  # ~2 seconds at 60 FPS

# Explosion Animation
explosion_images = [
    pygame.transform.scale(pygame.image.load(f'gallery/explosion{i}.png'), (128, 128))
    for i in range(1, 5)
]
explosions = []
EXPLOSION_DELAY = 10

def trigger_explosion(x, y):
    explosions.append({'x': x, 'y': y, 'frame': 0, 'timer': 0})

def animate_explosions():
    for explosion in explosions[:]:
        explosion['timer'] += 1
        if explosion['timer'] >= EXPLOSION_DELAY:
            explosion['frame'] += 1
            explosion['timer'] = 0
        if explosion['frame'] >= len(explosion_images):
            explosions.remove(explosion)
        else:
            img = explosion_images[explosion['frame']]
            screen.blit(img, (explosion['x'], explosion['y']))

def player(x, y):
    if invincible:
        if (invincible_timer // 5) % 2 == 0:
            screen.blit(playerImg, (x - 16, y + 10))
    else:
        if player_visible:
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

# Enemy Bullets
enemy_bulletImg = pygame.image.load('gallery/enemy_bullet.png')
enemy_bulletX = [0] * num_enemy
enemy_bulletY = [0] * num_enemy
enemy_bulletY_change = 1
enemy_bullet_state = ["ready"] * num_enemy

def enemy_bullet_fire(x, y, i):
    enemy_bullet_state[i] = "fire"
    enemy_bulletX[i] = x + 16
    enemy_bulletY[i] = y + 32

def move_enemy_bullets():
    global player_visible, player_exploding, player_explosion_timer, lives, game_ended, playerX, playerY, invincible
    for i in range(num_enemy):
        if enemy_bullet_state[i] == "fire":
            screen.blit(enemy_bulletImg, (enemy_bulletX[i], enemy_bulletY[i]))
            enemy_bulletY[i] += enemy_bulletY_change
            if enemy_bulletY[i] > 720:
                enemy_bullet_state[i] = "ready"
            if abs(enemy_bulletX[i] - playerX) < 30 and abs(enemy_bulletY[i] - playerY) < 40 and not player_exploding and player_visible and not invincible:
                enemy_bullet_state[i] = "ready"
                trigger_explosion(playerX - 32, playerY - 32)
                explosionSound = mixer.Sound("gallery/explosion.wav")
                explosionSound.play()
                player_visible = False
                player_exploding = True
                player_explosion_timer = 0

def isCollision(enemyX, enemyY, bulletX, bulletY, i):
    distance = math.sqrt((math.pow(enemyX[i] - bulletX, 2)) + (math.pow(enemyY[i] - bulletY, 2)))
    return distance < 27

font_big = pygame.font.Font("freesansbold.ttf", 50)
def game_over():
    over_text = font_big.render("GAME OVER", True, (255, 99, 71))
    screen.blit(over_text, (500, 370))

def show_stats():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
    level_text = font.render(f"Level: {level}", True, (0, 255, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    screen.blit(level_text, (10, 90))

# Game loop
running = True
game_ended = False
auto_mode = False

while running:
    screen.fill((0, 0, 0))
    back()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                auto_mode = not auto_mode

    if not game_ended:
        keys = pygame.key.get_pressed()

        if auto_mode:
            # Auto-fire when enemy is vertically aligned with player
            if bullet_state == "ready":
                for i in range(num_enemy):
                    if abs(enemyX[i] - playerX) < 30:
                        bulletSound = mixer.Sound("gallery/laser.wav")
                        bulletSound.play()
                        bulletX = playerX
                        bulletY = playerY
                        bullet_fire(bulletX, bulletY)
                        break

            # Auto-dodge bullets
            dodge_direction = 0
            for i in range(num_enemy):
                if enemy_bullet_state[i] == "fire":
                    if abs(enemy_bulletY[i] - playerY) < 80 and abs(enemy_bulletX[i] - playerX) < 50:
                        if enemy_bulletX[i] < playerX:
                            dodge_direction += 1
                        else:
                            dodge_direction -= 1
            if dodge_direction > 0:
                playerX_change = 0.5  # move right
            elif dodge_direction < 0:
                playerX_change = -0.5  # move left
            else:
                playerX_change = 0
        else:
            # Manual movement using A and D keys
            if keys[pygame.K_d]:
                playerX_change = 0.4
            elif keys[pygame.K_a]:
                playerX_change = -0.4
            else:
                playerX_change = 0
            # Manual fire with K key
            if keys[pygame.K_k] and bullet_state == "ready":
                bulletSound = mixer.Sound("gallery/laser.wav")
                bulletSound.play()
                bulletX = playerX
                bulletY = playerY
                bullet_fire(bulletX, bulletY)

        # Player explosion handling
        if player_exploding:
            player_explosion_timer += 1
            if player_explosion_timer >= EXPLOSION_DELAY * len(explosion_images):
                player_exploding = False
                lives -= 1
                if lives > 0:
                    playerX = 640
                    playerY = 600
                    player_visible = True
                    invincible = True
                    invincible_timer = 0
                else:
                    game_ended = True

        # Invincibility timer
        if invincible:
            invincible_timer += 1
            if invincible_timer >= INVINCIBLE_DURATION:
                invincible = False

        playerX += playerX_change
        playerX = max(PLAYER_MIN_X, min(playerX, PLAYER_MAX_X))

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
                trigger_explosion(enemyX[i], enemyY[i])
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

            if enemy_bullet_state[i] == "ready" and random.randint(0, 100) < 1:
                enemy_bullet_fire(enemyX[i], enemyY[i], i)

            enemyX[i] += enemyX_change[i]
            enemy(enemyX[i], enemyY[i], i)

        if bullet_state == "fire":
            bullet_fire(bulletX, bulletY)
            bulletY -= bulletY_change
            if bulletY <= 0:
                bulletY = 600
                bullet_state = "ready"

        move_enemy_bullets()
        animate_explosions()
        show_stats()
    else:
        animate_explosions()
        game_over()

    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
