# ui.py

import pygame
from settings import ASSETS, SCREEN_WIDTH

class UIManager:
    def __init__(self):
        self.font = pygame.font.Font(ASSETS["font"], 32)
        self.font_big = pygame.font.Font(ASSETS["font"], 50)

    def draw_stats(self, screen, score, lives, level):
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        lives_text = self.font.render(f"Lives: {lives}", True, (255, 0, 0))
        level_text = self.font.render(f"Level: {level}", True, (0, 255, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(level_text, (10, 90))

    def draw_game_over(self, screen, score):
        over_text = self.font_big.render("GAME OVER", True, (255, 99, 71))
        score_text = self.font.render(f"Final Score: {score}", True, (255, 255, 255))
        restart_text = self.font.render("Press ENTER for New Game", True, (255, 255, 255))
        screen.blit(over_text, (SCREEN_WIDTH // 2 - 150, 300))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, 380))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 160, 440))

    def draw_main_menu(self, screen):
        title = self.font_big.render("SPACE SHOOTER", True, (255, 255, 255))
        start = self.font.render("Press ENTER to Start", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 - 200, 250))
        screen.blit(start, (SCREEN_WIDTH // 2 - 120, 350))

    def draw_pause_menu(self, screen):
        pause_text = self.font_big.render("PAUSED", True, (255, 255, 255))
        resume = self.font.render("Press R to Resume", True, (255, 255, 255))
        new_game = self.font.render("Press N for New Game", True, (255, 255, 255))
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - 100, 280))
        screen.blit(resume, (SCREEN_WIDTH // 2 - 100, 350))
        screen.blit(new_game, (SCREEN_WIDTH // 2 - 120, 400))
