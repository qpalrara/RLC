import pygame
from rlc import *
from scroll import *

class SoftwareRender:
    def __init__(self):
        self.RES = self.WIDTH, self.HEIGHT = 1400, 800
        self.WIDTH, self.HEIGHT = self.WIDTH//2, self.HEIGHT//2
        self.FPS = 60
        self.screen = pygame.display.set_mode(self.RES)
        self.clock = pygame.time.Clock()
        self.scroll = Scroll(1000, 700, 300, pygame.Color("black"), 0)
        self.rlc = RLC(self, [10^(3*self.scroll.gauge-5)], [0], [0])
        self.font = pygame.font.SysFont("consolas", 30)

    def update(self, events):
        self.screen.fill(pygame.Color('white'))
        self.screen.blit(self.font.render("Q0 = "+"%.2e"%(10**(3*self.scroll.gauge-5)), True, pygame.Color('black')), (1050, 600))
        self.rlc = RLC(self, [10**(3*self.scroll.gauge-5)], [0], [0])
        self.rlc.draw()
        self.scroll.update(events, self.screen)


    def run(self):
        while True:
            events = pygame.event.get()
            self.update(events)
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.display.flip()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    pygame.init()
    app = SoftwareRender()
    app.run()