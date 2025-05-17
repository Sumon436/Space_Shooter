# game.py

import pygame
import random
from player import Player
from enemy import Enemy
from bullet import PlayerBullet, EnemyBullet
from explosion import ExplosionManager
from ui import UIManager
from settings import (
    ASSETS, NUM_ENEMIES, LEVEL_UP_SCORE,
    INVINCIBLE_DURATION, SCREEN_WIDTH, SCREEN_HEIGHT,
    AUTO_FIRE_DELAY
)
from pygame import mixer

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.bg = pygame.image.load(ASSETS["background"])
        pygame.display.set_icon(pygame.image.load(ASSETS["icon"]))

        # Sound
        mixer.init()
        mixer.music.load(ASSETS["music"])
        mixer.music.set_volume(0.4)
        mixer.music.play(-1)

        self.explosion_sound = mixer.Sound(ASSETS["explosion_sounds"])
        self.explosion_sound.set_volume(0.5)
        self.laser_sound = mixer.Sound(ASSETS["laser_sound"])
        self.laser_sound.set_volume(0.3)

        self.explosion_channel = mixer.Channel(1)
        self.laser_channel = mixer.Channel(2)

        self.ui = UIManager()
        self.explosions = ExplosionManager()

        self.player = Player()
        self.player_bullets = []
        self.enemies = [Enemy(i) for i in range(NUM_ENEMIES)]
        self.enemy_bullets = []

        self.score = 0
        self.lives = 3
        self.level = 1
        self.auto_mode = False
        self.auto_fire_cooldown = 0

        self.state = "menu"
        self.game_ended = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "menu" and event.key == pygame.K_RETURN:
                self.reset_game()
                self.state = "running"
            elif self.state == "running":
                if event.key == pygame.K_p:
                    self.state = "paused"
                if event.key == pygame.K_l:
                    self.auto_mode = not self.auto_mode
            elif self.state == "paused":
                if event.key == pygame.K_r:
                    self.state = "running"
                elif event.key == pygame.K_n:
                    self.reset_game()
                    self.state = "running"
            elif self.state == "gameover" and event.key == pygame.K_RETURN:
                self.reset_game()
                self.state = "running"

    def reset_game(self):
        self.player = Player()
        self.player_bullets = []
        self.enemy_bullets = []
        self.enemies = [Enemy(i) for i in range(NUM_ENEMIES)]
        self.explosions = ExplosionManager()

        self.score = 0
        self.lives = 3
        self.level = 1
        self.auto_fire_cooldown = 0
        self.state = "running"
        self.game_ended = False

    def update(self):
        if self.state != "running":
            return

        keys = pygame.key.get_pressed()
        direction = 0

        if self.auto_mode:
            self.auto_fire_cooldown += 1
            if self.auto_fire_cooldown >= AUTO_FIRE_DELAY:
                for enemy in self.enemies:
                    if abs(enemy.x - self.player.x) < 30:
                        if self.player.visible:
                            self.player_bullets.append(PlayerBullet(self.player.x, self.player.y))
                            self.laser_channel.play(self.laser_sound)
                        self.auto_fire_cooldown = 0
                        break

            for bullet in self.enemy_bullets:
                if bullet.active and abs(bullet.y - self.player.y) < 80 and abs(bullet.x - self.player.x) < 50:
                    if bullet.x < self.player.x:
                        direction += 1
                    else:
                        direction -= 1
        else:
            if keys[pygame.K_a]: direction = -1
            elif keys[pygame.K_d]: direction = 1
            if keys[pygame.K_k]:
                if not self.player_bullets or (self.player_bullets and self.player_bullets[-1].y < self.player.y - 40):
                    if self.player.visible:
                        self.player_bullets.append(PlayerBullet(self.player.x, self.player.y))
                        self.laser_channel.play(self.laser_sound)

        self.player.move(direction)
        self.player.update_invincibility()

        for bullet in self.player_bullets[:]:
            bullet.move()
            if not bullet.visible:
                self.player_bullets.remove(bullet)

        for bullet in self.enemy_bullets[:]:
            bullet.move()
            if not bullet.active:
                self.enemy_bullets.remove(bullet)
            elif self.check_collision(bullet.x, bullet.y, self.player.x, self.player.y):
                if not self.player.invincible and self.player.visible:
                    self.explosion_channel.play(self.explosion_sound)
                    self.explosions.trigger(self.player.x - 32, self.player.y - 32)
                    self.player.visible = False
                    self.player.exploding = True
                    self.player.explosion_timer = 0
                    bullet.active = False

        if self.player.exploding:
            self.player.explosion_timer += 1
            if self.player.explosion_timer >= 30 * 4:
                self.player.exploding = False
                self.lives -= 1
                if self.lives > 0:
                    self.player.reset_position()
                    self.player.visible = True
                    self.player.invincible = True
                else:
                    self.state = "gameover"

        for enemy in self.enemies:
            enemy.move()
            if enemy.bullet_ready and random.randint(0, 300) < 3:
                self.enemy_bullets.append(EnemyBullet(enemy.x, enemy.y, self.level))
                enemy.bullet_ready = False
            else:
                enemy.bullet_ready = True

        for bullet in self.player_bullets[:]:
            for enemy in self.enemies:
                if self.check_collision(bullet.x, bullet.y, enemy.x, enemy.y):
                    self.explosion_channel.play(self.explosion_sound)
                    self.explosions.trigger(enemy.x, enemy.y)
                    self.score += 1
                    enemy.reset_position()
                    try:
                        self.player_bullets.remove(bullet)
                    except ValueError:
                        pass

        if self.score and self.score % LEVEL_UP_SCORE == 0:
            self.level = self.score // LEVEL_UP_SCORE + 1
            for enemy in self.enemies:
                enemy.update_speed(self.level)

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        if self.state == "menu":
            self.ui.draw_main_menu(self.screen)
        elif self.state == "paused":
            self.ui.draw_pause_menu(self.screen)
        elif self.state == "gameover":
            self.ui.draw_game_over(self.screen, self.score)
        elif self.state == "running":
            self.player.draw(self.screen)
            for bullet in self.player_bullets:
                bullet.draw(self.screen)
            for bullet in self.enemy_bullets:
                bullet.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            self.explosions.update_and_draw(self.screen)
            self.ui.draw_stats(self.screen, self.score, self.lives, self.level)

    def check_collision(self, x1, y1, x2, y2, threshold=30):
        return abs(x1 - x2) < threshold and abs(y1 - y2) < threshold
