from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.pos = VEC(pos) + INITIAL_OFFSET
        # print(self.pos)
        self.tetromino = tetromino
        super().__init__(self.tetromino.tetris.sprite_group)
        # self.img = self.tetromino.img
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('orange')
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos * TILE_SIZE

    def check_collision(self):
        pass

    def update(self):
        print(self.pos)

