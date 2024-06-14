from settings import *
import random

class Tile(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        super().__init__(tetromino.sprite_group)
        self.tetromino = tetromino
        self.pos = pos + OFFSET
        self.image = tetromino.image
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos * T_SIZE
        self.dead = False

        self.sfx_image = self.image.copy()
        self.sfx_image.set_alpha(110)
        self.sfx_speed = random.uniform(0.2, 0.6)
        self.sfx_cycles = random.randrange(16, 18)
        self.cycle_counter = 0

    def sfx_end_time(self):
        if self.tetromino.trigger:
            self.cycle_counter += 1
            if self.cycle_counter > self.sfx_cycles:
                self.cycle_counter = 0
                return True

    def sfx_run(self):
        self.image = self.sfx_image
        self.pos.y -= self.sfx_speed
        self.image = pg.transform.rotate(self.image, pg.time.get_ticks() * self.sfx_speed)
    
    def is_alive(self):
        if self.dead:
            if not self.sfx_end_time():
                self.sfx_run()
            else:
                self.kill() 

    def rotate(self, pivot):
        t1 = self.pos - pivot
        t2 = t1.rotate(90)
        return t2 + pivot
    
    def check_other(self, pos):
        return self.tetromino.field[int(pos.y)][int(pos.x)] != 0

    def check_collision(self, pos):
        # print(pos)
        if pos.y >= N_ROWS:
            return 1
        elif pos.x < 0 or pos.x >= N_COLS:
            return 2
        return 0

    def set_rect_pos(self):
        self.rect.topleft = self.pos * T_SIZE

    def update(self):
        self.set_rect_pos()
        self.is_alive()
