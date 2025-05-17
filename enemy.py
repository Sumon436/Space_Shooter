# enemy.py

import pygame
import random
from settings import ASSETS, SCREEN_WIDTH, BASE_ENEMY_SPEED

class Enemy:
    def __init__(self, index, level=1):
        self.image = pygame.image.load(ASSETS["enemy"])
        self.x = random.randint(0, SCREEN_WIDTH - 64)
        self.y = random.randint(100, 150)
        self.index = index
        self.direction = 1
        self.speed = BASE_ENEMY_SPEED + (level - 1) * 0.2
        self.y_change = 30
        self.bullet_ready = True
        self.bullet_x = 0
        self.bullet_y = 0

    def move(self):
        self.x += self.speed * self.direction
        if self.x <= 0:
            self.direction = 1
            self.y += self.y_change
        elif self.x >= SCREEN_WIDTH - 64:
            self.direction = -1
            self.y += self.y_change

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def reset_position(self):
        self.x = random.randint(0, SCREEN_WIDTH - 64)
        self.y = random.randint(100, 150)

    def update_speed(self, level):
        self.speed = BASE_ENEMY_SPEED + (level - 1) * 0.2
