from settings import *
from tile import Tile
import random

class Tetromino:
    def __init__(self, tetris):
        self.tetris = tetris
        self.shape = random.choice(list(TETROMINOES.keys()))
        # self.img = pygame.
        self.blocks = [Tile(self, pos) for pos in TETROMINOES[self.shape]]
        # Tile(self, (4, 7))
    
    def move(self, direction='down'):
        move_direction = MOVEMENT[direction]
        # nxt_pos = [tile.pos + move_direction for tile in self.blocks]

        for tile in self.blocks:
            tile.pos += move_direction

    def rotate(self):
        pass

    def check_collision(self):
        pass

    def update(self):
        self.move()
