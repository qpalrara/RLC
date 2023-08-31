import math
import pygame
# Vcos(wt) = Q/C + (dQ/dt)R + L(d^2Q/dt^2)
class RLC:
    def __init__(self, render, q, q_, q__):
        self.render = render
        
        self.q = q
        self.q_ = q_
        self.q__ = q__

        # 전압, 전기용량, 인덕턴스, 저항, 각진동수, 시간, 시간 변화(600000프레임 -> 1초)
        self.V = 150
        self.C = 3.5E-6
        self.L = 0.6
        self.R = 250
        self.w = 60*2*math.pi
        self.t = 0
        self.dt = 1 / (render.FPS*1000)

        # 그래프 너비, 높이
        self.graph_width = 0.1
        self.height = 100

        # 세가지 그래프의 색깔, 위치
        self.colors = {'q': pygame.Color('red'), 'q_': pygame.Color('green'), 'q__': pygame.Color('blue')}
        self.positions = {'q': 150, 'q_': 400, 'q__': 650}

        self.font = pygame.font.SysFont("Consolas", 15)
        # n 주기까지 그림
        self.graph_len = 8

        
        for i in range(8000):
            self.update()

    def draw(self):
        '''
        모든 데이터를 그리고 극댓값을 표시함
        '''
        for key, data in zip(self.colors.keys(), [self.q, self.q_, self.q__]):

            max_val = max([abs(value) for value in data]+[0.0001])
            self.draw_line((100, self.positions[key]), max_val)
            scale_factor = self.height / max_val

            for i in range(len(data)):
                if i != len(data)-1:
                    if data[i] > data[i-1] and data [i] > data[i+1] and data[i]:
                        self.render.screen.blit(self.font.render("%.2e"%(data[i]), True, pygame.Color('black')), (70+i*self.graph_width, self.positions[key]-data[i]*scale_factor-20))
                pygame.draw.circle(self.render.screen, self.colors[key], 
                                   (100 + i * self.graph_width, - data[i] * scale_factor + self.positions[key]), 2)
                

    def draw_line(self, pos, max_val):
        '''
        그래프의 틀을 그림
        '''
        x, y = pos
        pygame.draw.line(self.render.screen, pygame.Color('gray'), pos, [x + self.graph_len*100, y], 3)
        for i, v in [(100, -max_val), (50, -max_val/2), (-50, max_val/2), (-100, max_val)]:
            pygame.draw.line(self.render.screen, pygame.Color('gray'), [x, y+i], [x + self.graph_len*100, y+i], 1)
            self.render.screen.blit(self.font.render("%.2e"%(v), True, pygame.Color("black")), (x-80, y+i-7))
        
        self.render.screen.blit(self.font.render("0", True, pygame.Color("black")), (x-15, y-7))

        pygame.draw.line(self.render.screen, pygame.Color('gray'), [x, y-100], [x, y+100], 3)
        for i in range(1, self.graph_len+1):
            pygame.draw.line(self.render.screen, pygame.Color('gray'), [x+100*i, y-100], [x+100*i, y+100], 1)
            self.render.screen.blit(self.font.render(f"{i}T", True, pygame.Color("black")), (100*i+107, y+7))

    def update(self):
        '''
        전하량, 전류, 전류 변화를 업데이트함
        '''
        self.q_.append(self.q_[-1] + self.q__[-1]*self.dt)
        self.q.append(self.q[-1] + self.q_[-1]*self.dt)
        self.q__.append((self.V * math.cos(self.w * self.t) - self.q[-1] / self.C - self.R * self.q_[-1]) / self.L)
        self.t += self.dt

class Energy:
    def __init__(self, render, rlc):
        self.render = render
        self.rlc = rlc
        self.L = self.rlc.L
        self.C = self.rlc.C
        self.UL = []
        self.UC = []
        self.U = []

        self.colors = {'UL': pygame.Color('red'), 'UC': pygame.Color('blue'), 'U' : pygame.Color('green')}

        # 그래프 너비, 높이
        self.graph_width = 0.1
        self.height = 100

        # n 주기까지 그림
        self.graph_len = 8

        self.font = pygame.font.SysFont("Consolas", 15)

        self.update()

    def update(self):
        self.UL = [1/2*self.L*i**2 for i in self.rlc.q_]
        self.UC = [i**2/(2*self.C) for i in self.rlc.q]
        self.U = [i+j for i, j in zip(self.UL, self.UC)]
    
    def draw(self):
        '''
        모든 데이터를 그리고 극댓값을 표시함
        '''
        max_val = max([abs(value) for value in self.UL + self.UC]+[0.0001])
        self.draw_line((100, 150), max_val)
        scale_factor = self.height / max_val
        for key, data in zip(self.colors.keys(), [self.UL, self.UC, self.U]):
            for i in range(len(data)):
                if i != len(data)-1:
                    if data[i] > data[i-1] and data [i] > data[i+1] and data[i]:
                        self.render.screen.blit(self.font.render("%.2e"%(data[i]), True, pygame.Color('black')), (70+i*self.graph_width, 150 -data[i]*scale_factor-20))
                pygame.draw.circle(self.render.screen, self.colors[key], 
                                   (100 + i * self.graph_width, - data[i] * scale_factor + 150), 2)
                

    def draw_line(self, pos, max_val):
        '''
        그래프의 틀을 그림
        '''
        x, y = pos
        pygame.draw.line(self.render.screen, pygame.Color('gray'), pos, [x + self.graph_len*100, y], 3)
        for i, v in [(100, -max_val), (50, -max_val/2), (-50, max_val/2), (-100, max_val)]:
            pygame.draw.line(self.render.screen, pygame.Color('gray'), [x, y+i], [x + self.graph_len*100, y+i], 1)
            self.render.screen.blit(self.font.render("%.2e"%(v), True, pygame.Color("black")), (x-80, y+i-7))
        
        self.render.screen.blit(self.font.render("0", True, pygame.Color("black")), (x-15, y-7))

        pygame.draw.line(self.render.screen, pygame.Color('gray'), [x, y-100], [x, y+100], 3)
        for i in range(1, self.graph_len+1):
            pygame.draw.line(self.render.screen, pygame.Color('gray'), [x+100*i, y-100], [x+100*i, y+100], 1)
            self.render.screen.blit(self.font.render(f"{i}T", True, pygame.Color("black")), (100*i+107, y+7))