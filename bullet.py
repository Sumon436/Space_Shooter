# bullet.py

import pygame
from settings import ASSETS, BULLET_SPEED, BASE_ENEMY_BULLET_SPEED

class PlayerBullet:
    def __init__(self, x, y):
        self.image = pygame.image.load(ASSETS["bullet"])
        self.x = x
        self.y = y
        self.speed = BULLET_SPEED
        self.visible = True

    def move(self):
        self.y -= self.speed
        if self.y < 0:
            self.visible = False

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, (self.x, self.y))


class EnemyBullet:
    def __init__(self, x, y, level=1):
        self.image = pygame.image.load(ASSETS["enemy_bullet"])
        self.x = x + 16
        self.y = y + 32
        self.speed = BASE_ENEMY_BULLET_SPEED + (level - 1) * 0.1
        self.active = True

    def move(self):
        self.y += self.speed
        if self.y > 720:
            self.active = False

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))
