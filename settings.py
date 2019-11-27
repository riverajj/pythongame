import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 416   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 608  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Sword Hero"
BGCOLOR = DARKGREY
ATTACK_IMG = 'attack.png'
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
WALLS_IMG = 'walls.png'
# Player settings
PLAYER_SPEED = 300
PLAYER_HEALTH = 100
PLAYER_IMG = 'rpg.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 32, 64)
#Monster settings
MOB_DAMAGE = 2
MONSTER_HIT_RECT = pg.Rect(0,0,64,64)
MONSA_IMG = 'bat.png'
MONSB_IMG = 'bat.png'
MONSC_IMG = 'bat.png'
MOB_KNOCKBACK = 20