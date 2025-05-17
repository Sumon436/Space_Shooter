# player.py

import pygame
from settings import (
    ASSETS,
    PLAYER_START_X,
    PLAYER_START_Y,
    PLAYER_SPEED,
    PLAYER_MIN_X,
    PLAYER_MAX_X,
    INVINCIBLE_DURATION  # Import global invincibility setting
)

class Player:
    def __init__(self):
        self.image = pygame.image.load(ASSETS["player"])
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.speed = PLAYER_SPEED
        self.x_change = 0
        self.visible = True
        self.exploding = False
        self.explosion_timer = 0
        self.invincible = False
        self.invincible_timer = 0

    def move(self, direction):
        self.x_change = direction * self.speed
        self.x += self.x_change
        self.x = max(PLAYER_MIN_X, min(self.x, PLAYER_MAX_X))

    def reset_position(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y

    def update_invincibility(self):
        if self.invincible:
            self.invincible_timer += 1
            if self.invincible_timer >= INVINCIBLE_DURATION:
                self.invincible = False
                self.invincible_timer = 0

    def draw(self, screen):
        if self.visible:
            # Blink effect while invincible
            if not self.invincible or (self.invincible and (self.invincible_timer // 5) % 2 == 0):
                screen.blit(self.image, (self.x - 16, self.y + 10))
