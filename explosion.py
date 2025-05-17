# explosion.py

import pygame
from settings import ASSETS

class ExplosionManager:
    def __init__(self, delay=5):  # Default delay set to faster value
        self.images = [pygame.transform.scale(pygame.image.load(path), (128, 128)) for path in ASSETS["explosions"]]
        self.explosions = []
        self.delay = delay

    def trigger(self, x, y):
        self.explosions.append({"x": x, "y": y, "frame": 0, "timer": 0})

    def update_and_draw(self, screen):
        for explosion in self.explosions[:]:
            explosion["timer"] += 1
            if explosion["timer"] >= self.delay:
                explosion["frame"] += 1
                explosion["timer"] = 0
            if explosion["frame"] >= len(self.images):
                self.explosions.remove(explosion)
            else:
                screen.blit(self.images[explosion["frame"]], (explosion["x"], explosion["y"]))
