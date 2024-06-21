from settings import *
from tetromino import Tetromino

class Tetris:
    def __init__(self, app):
        self.sprite_group = pygame.sprite.Group()
        self.app = app
        self.tetromino = Tetromino(self)

    def control(self, pressed_key):
        if pressed_key == pygame.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pygame.K_RIGHT:
            self.tetromino.move(direction='right')
        elif pressed_key == pygame.K_UP:
            self.tetromino.rotate()
        # elif pressed_key == pygame.K_DOWN:
        #     self.speed_up = True

    def draw_grid(self):
        for i in range(FIELD_W):
            for j in range(FIELD_H):
                pygame.draw.rect(self.app.screen, 'black', pygame.Rect(i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def update(self):
        self.tetromino.update()
        self.sprite_group.update()

    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)
