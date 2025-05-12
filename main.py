import pygame
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
    player(playerX, playerY)  # Draw the player every frame
    pygame.display.update()   # Update the screen every frame

pygame.quit()
sys.exit()
