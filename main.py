import pygame
import random
import math
import sys

pygame.init()

# Set display
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Space Shooter")

#score
score = 0
font = pygame.font.Font("freesansbold.ttf",32)
score_x = 10
score_y = 10
def score_f(score_x,score_y):
    score_show = font.render("Score: "+str(score),True,(255,255,255))
    screen.blit(score_show,(score_x,score_y))

# Icon
icon = pygame.image.load('gallery/galaxy.png')
pygame.display.set_icon(icon)

# Background
bg = pygame.image.load('gallery/background.jpg')
def back():
    screen.blit(bg, (0, 0))

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
bulletY_change = 2
bullet_state = "ready"




def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x , y))


#enemy
enemyImg =[]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_enemy = 7
for i in range(num_enemy):
 enemyImg.append(pygame.image.load('gallery/enemy.png'))
 enemyX.append(random.randint(0, 1216))
 enemyY.append(random.randint(100, 150))
 enemyX_change.append(0.4)
 enemyY_change.append(10)

def enemy(x, y,i):
    screen.blit(enemyImg[i], (x, y))

#collision detection
def isCollision(enemyX,enemyY,bulletX,bulletY,i):
    distance = math.sqrt((math.pow(enemyX[i]-bulletX,2))+(math.pow(enemyY[i]-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    back()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                playerX_change = 0.3
            if event.key == pygame.K_a:
                playerX_change = -0.3
            if event.key == pygame.K_l:
                if bullet_state == "ready":
                    bulletX = playerX
                    bullet_fire(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_d, pygame.K_a):
                playerX_change = 0

    # Update player position
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1216:
        playerX = 1216

    player(playerX, playerY)


    #enemy movement
    for i in range(num_enemy):
      if enemyX[i] <= 0:
        enemyX_change[i] = 0.4
        enemyY[i] += enemyY_change[i]
      elif enemyX[i] >= 1216:
        enemyX_change[i] = -0.4
        enemyY[i] += enemyY_change[i]
      #collision
      collision = isCollision(enemyX,enemyY,bulletX,bulletY,i)
      if collision:
        bulletY = 600
        bullet_state = "ready"
        enemyX[i] = random.randint(0, 1216)
        enemyY[i] = random.randint(100, 150)
        score += 1
        
     #enemy call
      enemyX[i] += enemyX_change[i]
      enemy(enemyX[i], enemyY[i],i)

    #score call
      score_f(score_x,score_y)

    
    


    # Bullet movement
    if bullet_state == "fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY <= 0:
            bulletY = 600
            bullet_state = "ready"

    pygame.display.update()

pygame.quit()
sys.exit()
