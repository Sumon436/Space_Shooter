import pygame
import random
import sys

pygame.init()

# Set up the display
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Space Shooter")

# Icon
icon = pygame.image.load('gallery/galaxy.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('gallery/player.png')
playerX = 640
playerY = 600
playerX_change = 0

def player(x, y):
    screen.blit(playerImg,(x, y))


#enmey
enemyImg = pygame.image.load('gallery/enemy.png')
enemyX = random.randint(0,1216)
enemyY = random.randint(100,150)
enemyX_change = 0.4
enemyY_change = 10


def enemy(x,y):
    screen.blit(enemyImg,(x,y))
# Main loop
running = True
while running:
    screen.fill((0, 0, 0))
    
 # Move the player

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_d:
                playerX_change +=0.3
            if event.key == pygame.K_a:
                 playerX_change -=0.3
        if event.type == pygame.KEYUP:
             if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    #call player
    playerX += playerX_change
    #line of boundary
    if playerX <= 0:
        paylerX = 0
    elif playerX >= 1216:
        playerX = 1216
    player(playerX, playerY)  # Draw the player every frame
    #enemy call
    
    if enemyX <= 0:
           enemyX_change = 0.4
           enemyY += enemyY_change
    elif enemyX >= 1216:
         enemyX_change -= 0.4
         enemyY += enemyY_change
    
    enemyX += enemyX_change
    enemy(enemyX,enemyY)
    pygame.display.update()   # Update the screen every frame

pygame.quit()
sys.exit()
