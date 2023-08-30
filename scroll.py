import pygame as pg

class Scroll:
    def __init__(self, start_x:int, start_y:int, length:int, color, type:int):
        self.start_x = start_x
        self.start_y = start_y
        self.length = length
        self.type = type
        self.color = color
        if self.type == 0:
            self.rect = pg.Rect(start_x-10, start_y-5, 20, 10)
        else:
            self.rect = pg.Rect(start_x-5, start_y+10, 10, 20)
        self.clicking = False
        self.gauge = 0



    def update(self, events, screen):
        self.draw(screen)
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(pg.mouse.get_pos()):
                self.clicking = True
            if event.type == pg.MOUSEBUTTONUP:
                self.clicking = False
        self.move()
        if self.type == 0:
            self.gauge = (self.rect.centerx - self.start_x)/self.length
        else:
            self.gauge = (self.rect.centery - self.start_y)/self.length

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        if self.type == 0:
            pg.draw.line(screen, pg.Color('black'), (self.start_x, self.start_y), (self.start_x+self.length, self.start_y))
        else:
            pg.draw.line(screen, pg.Color('black'), (self.start_x, self.start_y), (self.start_x, self.start_y+self.length))

    def move(self):
        mouse_pos = pg.mouse.get_pos()
        if self.clicking:
            if self.type == 0:
                self.rect.centerx = min(max(mouse_pos[0], self.start_x), self.start_x + self.length)
            else:
                self.rect.centery = min(max(mouse_pos[1], self.start_y), self.start_y + self.length)

