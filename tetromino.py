from settings import *
from tile import Tile
import random

class Tetromino:
    def __init__(self, pkg):
        self.shape = random.choice(list(SHAPES.keys()))
        self.pkg = pkg
        self.sprite_group = pkg['sprite_group']
        self.field = pkg['play_field']
        self.landed = False
        self.image = pg.image.load(random.choice(pkg['images']))
        self.trigger = pkg['trigger']
        self.image = pg.transform.scale(self.image, (T_SIZE, T_SIZE))
        self.prev_pos = []
        self.curr = False
        self.start()

    def start(self):
        if not self.curr:
            self.pos = VEC(N_COLS + N_COLS // 2 - 1.3, N_ROWS // 2 - 1.2)
        else:
            for tile in self.tiles:
                tile.kill()
            self.pos = VEC(N_COLS // 2 - 1, 0)
        self.tiles = [Tile(self, pos) for pos in SHAPES[self.shape]]


    def is_game_over(self):
        for tile in self.tiles:
            i = int(tile.pos.x)
            j = int(tile.pos.y)
            if i >= 0 and j >= 0:
                if self.field[j][i] != 0:
                    return self.field[j][i].tetromino != self
        return False

    def check_lines(self):
        rows_to_be_cleared = []
        for i in range(N_ROWS - 1, -1, -1):
            counter = 0
            for j in range(N_COLS):
                if self.field[i][j] != 0 and self.field[i][j].tetromino.landed:
                    counter += 1
            if counter == N_COLS:
                rows_to_be_cleared.append(i)

        for i in rows_to_be_cleared:
            for j in range(N_COLS):
                self.field[i][j].dead = True
            self.field[i] = [0] * N_COLS

        if len(rows_to_be_cleared) > 0:
            self.pkg['sound'].play()
            self.pkg['score'] += SCORE[len(rows_to_be_cleared)]
            pg.time.set_timer(self.pkg['usr_event'], max(CAPPED_FD, FALLING_DELAY - self.pkg['score'] // 5))
            self.push_down(rows_to_be_cleared[0], len(rows_to_be_cleared))

    # def get_down(self):
    #     space_available = True
    #     while space_available:
    #         new_pos = [tile.pos + MOVEMENT['down'] for tile in self.tiles]
    #         if self.check_collision(new_pos) == 0:
    #             if any(map(Tile.check_other, self.tiles, new_pos)):
    #                 space_available = False
    #             else:
    #                 self.move('down')
    #         else:
    #             space_available = False

    def get_down(self):
        while not self.landed:
            # pg.time.wait(25)
            self.move('down')
            # self.sprite_group.update()
            # self.sprite_group.draw(self.pkg['screen'])


    def push_down(self, lowest_row, num_of_rows):
        for i in range(lowest_row-1, -1, -1):
            for j in range(N_COLS):
                if self.field[i][j] != 0:
                    self.field[i][j].pos.y += num_of_rows
                    self.field[i + num_of_rows][j] = self.field[i][j]
                    self.field[i][j] = 0

    def clear_prev(self):
        for pos in self.prev_pos:
            i = int(pos.x)
            j = int(pos.y)
            if i >= 0 and j >= 0:
                self.field[j][i] = 0

    def set_field(self):
        for tile in self.tiles:
            i = int(tile.pos.x)
            j = int(tile.pos.y)
            if i >= 0 and j >= 0:
                self.field[j][i] = tile

    def rotate(self):
        pivot = self.tiles[0].pos
        new_pos = [tile.rotate(pivot) for tile in self.tiles]

        status = self.check_collision(new_pos)
        # print(status)
        if status != 1 and status != 2:
            self.pkg['rotate_sfx'].play()
            self.prev_pos = [tile.pos for tile in self.tiles]
            self.clear_prev()
            r = True
            if any(map(Tile.check_other, self.tiles, new_pos)):
                r = False
            if r:
                for tile, pos in enumerate(new_pos):
                    self.tiles[tile].pos = pos
            self.set_field()

    def check_collision(self, positions):
        ans = list(map(Tile.check_collision, self.tiles, positions))
        for i in ans:
            if i == 1:
                return 1
        for i in ans:
            if i == 2:
                return 2
        return 0
    
    def control(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
            self.move('left')
        elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
            self.move('right')
        elif event.type == pg.KEYDOWN and event.key == pg.K_UP and self.shape != 'O':
            self.rotate()
        elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
            self.get_down()

    def move(self, direction):
        move_direction = MOVEMENT[direction]
        new_pos = [tile.pos + move_direction for tile in self.tiles]

        status = self.check_collision(new_pos)

        if status != 1 and status != 2:
            self.prev_pos = [tile.pos for tile in self.tiles]
            # print(self.prev_pos)
            self.clear_prev()
            m = True
            if any(map(Tile.check_other, self.tiles, new_pos)):
                if direction == 'down': 
                    self.landed = True
                m = False
            if m:
                for tile in self.tiles:
                    tile.pos += move_direction
            self.set_field()
            # print(self.prev_pos, end='\n\n')
        elif status == 1:
            self.landed = True
        # print(self.prev_pos)
        # print([tile.pos for tile in self.tiles])
        # print()

    def update(self):
        # self.set_field()
        if self.curr:
            self.trigger = self.pkg['trigger']
            if self.trigger:
                self.move('down')
            self.pkg['game_over'] = self.is_game_over()
            self.check_lines()
