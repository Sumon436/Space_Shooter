import pygame
from game import Game
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()
game = Game(screen)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.handle_event(event)

    game.update()
    game.draw()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
