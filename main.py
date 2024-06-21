from settings import *
from tetromino import Tetromino
import sys

# * INIT

pg.init()
if not pg.display.get_init():
    print("Display not Initialized!")
    sys.exit()

screen = pg.display.set_mode(WINDOW)
clk = pg.time.Clock()
pg.display.set_caption("Tetris Clone")

usr_event1 = pg.USEREVENT + 0
pg.time.set_timer(usr_event1, FALLING_DELAY)

tiles = pg.sprite.Group()
play_field = [[0] * N_COLS for _ in range(N_ROWS)]

score = 0
c = 0

pg.mixer.music.load(BGM_PATH)
pg.mixer.music.set_volume(0.3)
pg.mixer.music.play(-1)
img = pg.image.load(CTRL_IMG_PATH)
img = pg.transform.scale(img, (T_SIZE * 0.9, T_SIZE * 0.9))

clear_sound = pg.mixer.Sound(CLEAR_SFX_PATH)
game_over = pg.mixer.Sound(GAME_OVER_SFX_PATH)
rotate_sfx = pg.mixer.Sound(ROTATE_SFX_PATH)

care_package = {'sprite_group' : tiles,
                'play_field' : play_field,
                'screen' : screen,
                'images' : [ASSET_PATH + str(i) + '.png' for i in range(1, 7)],
                'trigger' : False,
                'game_over' : False,
                'score' : score,
                'sound' : clear_sound,
                'rotate_sfx' : rotate_sfx,
                'usr_event' : usr_event1}

running = True

# * FONT

font = ft.Font(FONT_PATH)

# * IMP

tetrominoes = []

# * USEFUL FUNCTIONS

def get_tetromino():
    if len(tetrominoes) < 1:
        tetrominoes.append(Tetromino(care_package))
        tetrominoes.append(Tetromino(care_package))
        tetrominoes[0].curr = True
        tetrominoes[0].start()
    elif len(tetrominoes) < 2:
        tetrominoes[0].curr = True
        tetrominoes[0].start()
        tetrominoes.append(Tetromino(care_package))

    
def check_landed():
    global tetrominoes
    for tetromino in tetrominoes:
        if tetromino.landed:
            tetrominoes = tetrominoes[1:]

def draw_grid():
    pg.draw.rect(screen, FIELD_BG_CLR, (0, 0, N_COLS * T_SIZE, N_ROWS * T_SIZE)) 
    
    for i in range(N_COLS):
        clr = (0, 0, 0)

        # if len(tetrominoes) > 0:

        #     curr = tetrominoes[0]
        #     cols = [tile.pos for tile in curr.tiles]
        #     # print(cols)
        #     for c in cols:
        #         if i == c.x:
        #             clr = (125, 125, 0)

        for j in range(N_ROWS):
            pg.draw.rect(screen, clr, (i * T_SIZE, j * T_SIZE, T_SIZE, T_SIZE), 1)

def draw_txt():
    font.render_to(screen, (PLAY_FIELD[0] * 1.12, T_SIZE), "Score", FONT_CLR, size=T_SIZE * 1.5)
    font.render_to(screen, (PLAY_FIELD[0] * 1.1, 7 * T_SIZE / 2), f"{care_package['score']:0>7}", SCORE_CLR, size=T_SIZE * 1.1)
    font.render_to(screen, (PLAY_FIELD[0] * 1.2, 11 * T_SIZE / 2), "Next", FONT_CLR, size=T_SIZE * 1.2)
    s = pg.Surface((T_SIZE * 10, T_SIZE * 5))
    s.fill((0, 170, 100))
    r = s.get_rect()
    r.topleft = (PLAY_FIELD[0], 15 * T_SIZE / 2)
    screen.blit(s, r)
    font.render_to(screen, (PLAY_FIELD[0] * 1.02, 27 * T_SIZE / 2), "Controls", FONT_CLR, size=T_SIZE * 1.2)
    i = img.copy()
    r = i.get_rect()
    r.topleft = (PLAY_FIELD[0] * 1.15, 30.5 * T_SIZE / 2)
    screen.blit(i, r)
    font.render_to(screen, (PLAY_FIELD[0] * 1.3, 31 * T_SIZE / 2), "Move Left", FONT_CLR, size=T_SIZE * 0.5)
    i = pg.transform.rotate(i, 180)
    r.topleft = (PLAY_FIELD[0] * 1.15, 32.5 * T_SIZE / 2)
    screen.blit(i, r)
    font.render_to(screen, (PLAY_FIELD[0] * 1.3, 33 * T_SIZE / 2), "Move Right", FONT_CLR, size=T_SIZE * 0.5)
    i = pg.transform.rotate(i, 90)
    r.topleft = (PLAY_FIELD[0] * 1.15, 34.5 * T_SIZE / 2)
    screen.blit(i, r)
    font.render_to(screen, (PLAY_FIELD[0] * 1.3, 35 * T_SIZE / 2), "Rotate", FONT_CLR, size=T_SIZE * 0.5)
    i = pg.transform.rotate(i, 180)
    r.topleft = (PLAY_FIELD[0] * 1.15, 36.5 * T_SIZE / 2)
    screen.blit(i, r)
    font.render_to(screen, (PLAY_FIELD[0] * 1.3, 37 * T_SIZE / 2), "Reach Down", FONT_CLR, size=T_SIZE * 0.5)

# * GAME LOOP

while True:
    if running: get_tetromino()

    # * UPDATE


    if len(tetrominoes) > 0: tetrominoes[0].update()
    tiles.update()
    
    # * DRAW

    screen.fill(BG_CLR)
    draw_grid()
    draw_txt()
    tiles.draw(screen)

    pg.display.flip()

    # * EVENT CHECKER
    care_package['trigger'] = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        elif event.type == usr_event1:
            # tetrominoes[0].move('down')
            care_package['trigger'] = True

            # for r in play_field:
            #     print(r)
            # print()
        if len(tetrominoes) > 0: tetrominoes[0].control(event)


    if care_package['game_over']:
        running = False
        pg.mixer.music.stop()
        if c < 1: game_over.play()
        c += 1
        tetrominoes = []

    check_landed()
    clk.tick(FPS)
