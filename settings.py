# settings.py

# Screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Player
PLAYER_START_X = 640
PLAYER_START_Y = 600
PLAYER_MIN_X = 0
PLAYER_MAX_X = 1216
PLAYER_SPEED = 5
INVINCIBLE_DURATION = 120

# Bullet
BULLET_SPEED = 4
AUTO_FIRE_DELAY = 6

# Enemy
NUM_ENEMIES = 7
BASE_ENEMY_SPEED = 5
ENEMY_SPEED_INCREMENT = 0.2
BASE_ENEMY_BULLET_SPEED = 4
ENEMY_BULLET_SPEED_INCREMENT = 0.1

# Explosion
EXPLOSION_DELAY = 5
AUTO_FIRE_DELAY = 9  # or try 2 for very fast fire


# Game Logic
LEVEL_UP_SCORE = 30

# Assets (relative paths)
ASSETS = {
    "icon": "gallery/galaxy.png",
    "background": "gallery/background.jpg",
    "player": "gallery/player.png",
    "enemy": "gallery/enemy.png",
    "bullet": "gallery/bullet.png",
    "enemy_bullet": "gallery/enemy_bullet.png",
    "explosion_sounds": "gallery/explosion.wav",
    "laser_sound": "gallery/laser.wav",
    "music": "gallery/background.wav",
    "explosions": [f"gallery/explosion{i}.png" for i in range(1, 5)],
    "font": "freesansbold.ttf"
}
