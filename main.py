import pygame
from rlc import *

class SoftwareRender:
    def __init__(self):
        self.RES = self.WIDTH, self.HEIGHT = 1400, 800
        self.WIDTH, self.HEIGHT = self.WIDTH//2, self.HEIGHT//2
        self.FPS = 60
        self.screen = pygame.display.set_mode(self.RES)
        self.clock = pygame.time.Clock()
        self.rlc = RLC(self)

    def draw(self):
        self.screen.fill(pygame.Color('white'))
        self.rlc.draw()


    def run(self):
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.display.flip()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    pygame.init()
    app = SoftwareRender()
    app.run()