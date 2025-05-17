import random
import math
import pygame
from pygame import mixer

pygame.init()

# Screen setup
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Space Shooter")

# Load icon and background
icon = pygame.image.load('gallery/galaxy.png')
pygame.display.set_icon(icon)
bg = pygame.image.load('gallery/background.jpg')

# Sounds
mixer.init()
mixer.music.load("gallery/background.wav")
mixer.music.set_volume(0.4)  # Background music volume
mixer.music.play(-1)
explosionSound = mixer.Sound("gallery/explosion.wav")
explosionSound.set_volume(0.5)  # Explosion volume
bulletSound = mixer.Sound("gallery/laser.wav")
bulletSound.set_volume(0.3)  # 🔉 Bullet volume lowered
explosion_channel = mixer.Channel(1)
laser_channel = mixer.Channel(2)

# Fonts
font = pygame.font.Font("freesansbold.ttf", 32)
font_big = pygame.font.Font("freesansbold.ttf", 50)

# Player settings
playerImg = pygame.image.load('gallery/player.png')
playerX = 640
playerY = 600
playerX_change = 0
PLAYER_MIN_X = 0
PLAYER_MAX_X = 1216
player_visible = True
player_exploding = False
player_explosion_timer = 0
invincible = False
invincible_timer = 0
INVINCIBLE_DURATION = 120

# Explosion animation frames
explosion_images = [pygame.transform.scale(pygame.image.load(f'gallery/explosion{i}.png'), (128, 128)) for i in range(1, 5)]
explosions = []
EXPLOSION_DELAY = 30

# Bullet image
bulletImg = pygame.image.load('gallery/bullet.png')

class PlayerBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4
        self.visible = True

    def move(self):
        self.y -= self.speed
        if self.y < 0:
            self.visible = False

    def draw(self, screen):
        if self.visible:
            screen.blit(bulletImg, (self.x, self.y))

player_bullets = []

# Enemy settings
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemy = 7
BASE_ENEMY_SPEED = 0.6
ENEMY_SPEED_INCREMENT = 0.2
BASE_ENEMY_BULLET_SPEED = 0.6
ENEMY_BULLET_SPEED_INCREMENT = 0.1

for i in range(num_enemy):
    enemyImg.append(pygame.image.load('gallery/enemy.png'))
    enemyX.append(random.randint(0, 1216))
    enemyY.append(random.randint(100, 150))
    enemyX_change.append(BASE_ENEMY_SPEED)
    enemyY_change.append(30)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Enemy bullets
enemy_bulletImg = pygame.image.load('gallery/enemy_bullet.png')
enemy_bulletX = [0] * num_enemy
enemy_bulletY = [0] * num_enemy
enemy_bulletY_change = BASE_ENEMY_BULLET_SPEED
enemy_bullet_state = ["ready"] * num_enemy

def enemy_bullet_fire(x, y, i):
    enemy_bullet_state[i] = "fire"
    enemy_bulletX[i] = x + 16
    enemy_bulletY[i] = y + 32

def move_enemy_bullets():
    global player_visible, player_exploding, player_explosion_timer, lives, playerX, playerY, invincible
    for i in range(num_enemy):
        if enemy_bullet_state[i] == "fire":
            screen.blit(enemy_bulletImg, (enemy_bulletX[i], enemy_bulletY[i]))
            enemy_bulletY[i] += enemy_bulletY_change
            if enemy_bulletY[i] > 720:
                enemy_bullet_state[i] = "ready"
            if (abs(enemy_bulletX[i] - playerX) < 30 and abs(enemy_bulletY[i] - playerY) < 40 and
                not player_exploding and player_visible and not invincible):
                enemy_bullet_state[i] = "ready"
                trigger_explosion(playerX - 32, playerY - 32)
                explosion_channel.play(explosionSound)
                player_visible = False
                player_exploding = True
                player_explosion_timer = 0

def isCollision(enemy_x_list, enemy_y_list, bullet_x, bullet_y, enemy_i=None):
    if enemy_i is not None:
        distance = math.sqrt((enemy_x_list[enemy_i] - bullet_x)**2 + (enemy_y_list[enemy_i] - bullet_y)**2)
        return distance < 27
    else:
        return False

def trigger_explosion(x, y):
    explosions.append({"x": x, "y": y, "frame": 0, "timer": 0})

def animate_explosions():
    for explosion in explosions[:]:
        explosion["timer"] += 1
        if explosion["timer"] >= EXPLOSION_DELAY:
            explosion["frame"] += 1
            explosion["timer"] = 0
        if explosion["frame"] >= len(explosion_images):
            explosions.remove(explosion)
        else:
            screen.blit(explosion_images[explosion["frame"]], (explosion["x"], explosion["y"]))

def player(x, y):
    if invincible:
        if (invincible_timer // 5) % 2 == 0:
            screen.blit(playerImg, (x - 16, y + 10))
    else:
        if player_visible:
            screen.blit(playerImg, (x - 16, y + 10))

# Game variables
score = 0
lives = 3
level = 1
LEVEL_UP_SCORE = 30

auto_fire_cooldown = 0
AUTO_FIRE_DELAY = 6

game_state = "menu"
running = True
game_ended = False
auto_mode = False

# Font functions
def game_over():
    over_text = font_big.render("GAME OVER", True, (255, 99, 71))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    restart_text = font.render("Press ENTER for New Game", True, (255, 255, 255))
    screen.blit(over_text, (500, 300))
    screen.blit(score_text, (540, 380))
    screen.blit(restart_text, (460, 440))

def show_stats():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
    level_text = font.render(f"Level: {level}", True, (0, 255, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    screen.blit(level_text, (10, 90))

def show_main_menu():
    title = font_big.render("SPACE SHOOTER", True, (255, 255, 255))
    start = font.render("Press ENTER to Start", True, (255, 255, 255))
    screen.blit(title, (460, 250))
    screen.blit(start, (500, 350))

def show_pause_menu():
    pause_text = font_big.render("PAUSED", True, (255, 255, 255))
    resume = font.render("Press R to Resume", True, (255, 255, 255))
    new_game = font.render("Press N for New Game", True, (255, 255, 255))
    screen.blit(pause_text, (530, 280))
    screen.blit(resume, (500, 350))
    screen.blit(new_game, (500, 400))

def reset_game():
    global score, lives, level, player_visible, player_exploding, player_explosion_timer
    global invincible, invincible_timer, playerX, playerY, player_bullets
    global enemyX, enemyY, enemyX_change, enemy_bulletY_change, enemy_bullet_state, game_ended

    score = 0
    lives = 3
    level = 1
    player_visible = True
    player_exploding = False
    player_explosion_timer = 0
    invincible = False
    invincible_timer = 0
    playerX = 640
    playerY = 600
    player_bullets = []

    for i in range(num_enemy):
        enemyX[i] = random.randint(0, 1216)
        enemyY[i] = random.randint(100, 150)
        enemyX_change[i] = BASE_ENEMY_SPEED
    enemy_bulletY_change = BASE_ENEMY_BULLET_SPEED
    enemy_bullet_state[:] = ["ready"] * num_enemy

    game_ended = False

# Game Loop
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "menu" and event.key == pygame.K_RETURN:
                reset_game()
                game_state = "running"
            elif game_state == "running":
                if event.key == pygame.K_p:
                    game_state = "paused"
                if event.key == pygame.K_l:
                    auto_mode = not auto_mode
            elif game_state == "paused":
                if event.key == pygame.K_r:
                    game_state = "running"
                elif event.key == pygame.K_n:
                    reset_game()
                    game_state = "running"
            elif game_state == "gameover":
                if event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = "running"

    if game_state == "menu":
        show_main_menu()

    elif game_state == "paused":
        show_pause_menu()

    elif game_state == "running" and not game_ended:
        keys = pygame.key.get_pressed()

        if auto_mode:
            auto_fire_cooldown += 1
            if auto_fire_cooldown >= AUTO_FIRE_DELAY:
                for i in range(num_enemy):
                    if abs(enemyX[i] - playerX) < 30:
                        laser_channel.play(bulletSound)
                        player_bullets.append(PlayerBullet(playerX, playerY))
                        auto_fire_cooldown = 0
                        break
            dodge_direction = 0
            for i in range(num_enemy):
                if enemy_bullet_state[i] == "fire":
                    if abs(enemy_bulletY[i] - playerY) < 80 and abs(enemy_bulletX[i] - playerX) < 50:
                        if enemy_bulletX[i] < playerX:
                            dodge_direction += 1
                        else:
                            dodge_direction -= 1
            playerX_change = 0.5 if dodge_direction > 0 else -0.5 if dodge_direction < 0 else 0
        else:
            playerX_change = 0
            if keys[pygame.K_d]:
                playerX_change = 0.4
            elif keys[pygame.K_a]:
                playerX_change = -0.4

            if keys[pygame.K_k]:
                if len(player_bullets) == 0 or (player_bullets and player_bullets[-1].y < playerY - 40):
                    laser_channel.play(bulletSound)
                    player_bullets.append(PlayerBullet(playerX, playerY))

        if player_exploding:
            player_explosion_timer += 1
            if player_explosion_timer >= EXPLOSION_DELAY * len(explosion_images):
                player_exploding = False
                lives -= 1
                if lives > 0:
                    playerX = 640
                    playerY = 600
                    player_visible = True
                    invincible = True
                    invincible_timer = 0
                else:
                    game_ended = True
                    game_state = "gameover"

        if invincible:
            invincible_timer += 1
            if invincible_timer >= INVINCIBLE_DURATION:
                invincible = False

        playerX += playerX_change
        playerX = max(PLAYER_MIN_X, min(playerX, PLAYER_MAX_X))
        player(playerX, playerY)

        for i in range(num_enemy):
            if enemyX[i] <= 0:
                enemyX_change[i] = abs(enemyX_change[i])
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 1216:
                enemyX_change[i] = -abs(enemyX_change[i])
                enemyY[i] += enemyY_change[i]

            for bullet in player_bullets[:]:
                if isCollision(enemyX, enemyY, bullet.x, bullet.y, i):
                    trigger_explosion(enemyX[i], enemyY[i])
                    explosion_channel.play(explosionSound)
                    try:
                        player_bullets.remove(bullet)
                    except ValueError:
                        pass
                    score += 1
                    enemyX[i] = random.randint(0, 1216)
                    enemyY[i] = random.randint(100, 150)

            enemyX[i] += enemyX_change[i]
            enemy(enemyX[i], enemyY[i], i)

            if enemy_bullet_state[i] == "ready" and random.randint(0, 300) < 3:
                enemy_bullet_fire(enemyX[i], enemyY[i], i)

        for bullet in player_bullets[:]:
            bullet.move()
            if not bullet.visible:
                player_bullets.remove(bullet)
            else:
                bullet.draw(screen)

        move_enemy_bullets()
        animate_explosions()
        show_stats()

        if score > 0 and score % LEVEL_UP_SCORE == 0:
            level = score // LEVEL_UP_SCORE + 1
            for i in range(num_enemy):
                speed = BASE_ENEMY_SPEED + ENEMY_SPEED_INCREMENT * (level - 1)
                enemyX_change[i] = speed if enemyX_change[i] > 0 else -speed
            enemy_bulletY_change = BASE_ENEMY_BULLET_SPEED + ENEMY_BULLET_SPEED_INCREMENT * (level - 1)

    elif game_state == "gameover":
        game_over()

    pygame.display.update()
