# config.py

# Screen settings
WIDTH, HEIGHT = 960, 540

# Colors
BACKGROUND_COLOR = (135, 206, 235)  # Light blue
ROOF_COLOR = (0, 0, 0)  # Black

# Roof settings
ROOF_WIDTH = 700
ROOF_HEIGHT = HEIGHT // 3
ROOF_X = (WIDTH - ROOF_WIDTH) // 2
ROOF_Y = HEIGHT - ROOF_HEIGHT

# Game settings
FPS = 60
PLAYER_JUMP_STRENGTH = -18
PLAYER_GRAVITY = 1
MAX_LEAN_ANGLE = 50
SERVER_IP = '127.0.0.1'
PORT = 5555