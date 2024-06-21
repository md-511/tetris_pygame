import sys
from tetris import Tetris
from settings import *

class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Tetris Clone ￣へ￣")
        self.screen = pygame.display.set_mode(FIELD_RES)
        self.clock = pygame.time.Clock()
        self.tetris = Tetris(self)
        self.set_timer()

    def set_timer(self):
        self.usr_event = pygame.USEREVENT + 0
        pygame.time.set_timer(self.usr_event, ANIMATION_DELAY)

    def check_events(self):
        self.trigger = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            
            elif event.type == self.usr_event:
                self.trigger = True

            elif event.type == pygame.KEYDOWN:
                self.tetris.control(event.key)

    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(FIELD_COLOR)
        self.tetris.draw()
        pygame.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    app = App()
    app.run()
