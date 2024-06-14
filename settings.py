import pygame as pg
import pygame.freetype as ft

VEC = pg.math.Vector2

T_SIZE = 35
N_COLS = 10
N_ROWS = 20

FPS = 60

FALLING_DELAY = 250
REDUCED_FALLING_DELAY = 15

OFFSET = pg.math.Vector2(N_COLS // 2 - 1, 0)

SCALE_X = 1.8
SLACE_Y = 1.0
PLAY_FIELD = (N_COLS * T_SIZE, N_ROWS * T_SIZE)
WINDOW = (PLAY_FIELD[0] * SCALE_X, PLAY_FIELD[1] * SLACE_Y)

ASSET_PATH = './assets/'
FONT_PATH = './assets/a.ttf'
BGM_PATH = './assets/Tetris.mp3'
CLEAR_SFX_PATH = './assets/clear.wav'
CTRL_IMG_PATH = './assets/a.png'

FIELD_BG_CLR = (22, 22, 22)
BG_CLR = (16, 186, 116)
SCORE_CLR = (14, 27, 54)
FONT_CLR = (255, 245, 247)

MOVEMENT = {'down' : VEC(0, 1),
            'left' : VEC(-1, 0),
            'right' : VEC(1, 0)}

SCORE = {1 : 100,
         2 : 300,
         3 : 900,
         4 : 1700}

SHAPES = {'I' : [VEC(0, 0),
                 VEC(1, 0),
                 VEC(-1, 0),
                 VEC(-2, 0)],
          'T' : [VEC(0, 0),
                 VEC(1, 0),
                 VEC(-1, 0),
                 VEC(0, 1)],
          'O' : [VEC(0, 0),
                 VEC(0, -1),
                 VEC(-1, 0),
                 VEC(-1, -1)],
          'S' : [VEC(0, 0),
                 VEC(1, 0),
                 VEC(0, 1),
                 VEC(-1, 1)],
          'Z' : [VEC(0, 0),
                 VEC(-1, 0),
                 VEC(0, 1),
                 VEC(1, 1)],
          'L' : [VEC(0, 0),
                 VEC(1, 0),
                 VEC(-1, 0),
                 VEC(-1, 1)],
          'J' : [VEC(0, 0),
                 VEC(-1, 0),
                 VEC(1, 0),
                 VEC(1, 1)]}
