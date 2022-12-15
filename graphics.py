import pygame
from pygame.locals import *
import numpy

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

class Window:
    STARTED = False

    def __init__(self, sizexy, FPS=30):
        if __class__.STARTED:
            raise RuntimeError('Only 1 Window allowed per process. Please start a new process.')

        pygame.init()
        pygame.font.init()
        __class__.STARTED = True

        self.fonts = []
        self.label_index = 0

        self.size = sizexy
        self.xmin = -sizexy[0]// 2
        self.xmax = sizexy[0] // 2
        self.ymin = -sizexy[1] // 2
        self.ymax = sizexy[1] // 2

        self.default_font = pygame.font.SysFont('Calibri', 20)
        self.__default_font = 'Calibri', 20
        self.window = pygame.display.set_mode(sizexy)

        self.running = True
        self.frame_counter = 0
        self.loop_frame = 0

        self.clock = pygame.time.Clock()
        self.FPS = FPS

        self.static = []
        self.dynamic = []

    def get_fps(self):
        return self.clock.get_fps()

    def set_loop(self, nframes):
        self.loop_frame = nframes

    def convert(self, point):
        return (int(point[0] + self.xmax), int(-point[1] + self.ymax))

    def draw(self):
        self.window.fill(WHITE)

        self.frame_counter += 1
        if self.loop_frame and self.frame_counter == self.loop_frame:
            self.frame_counter = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

        for draw_call in self.static:
            draw_call()

        for draw_call in self.dynamic:
            draw_call()

        pygame.display.update()
        pygame.display.flip()
        self.clock.tick(self.FPS)

    def text(self, string, position, font_size=20, font_name='Calibri', color=BLUE, antialias=True, bg=None):
        """ Static text """
        if (font_name, font_size) != self.__default_font:
            font = pygame.font.SysFont(font_name, font_size)
            self.fonts.append(font)
        def draw():
            text = font.render(string, antialias, color, bg)
            self.window.blit(text, position)
        self.static.append(draw)
    def dynamic_text(self, stringf, positionf, font_size=20, font_name='Calibri', color=BLUE, antialias=True, bg=None):
        """ Allows dynamic functions for text and position, evaluated at draw """
        if (font_name, font_size) != self.__default_font:
            font = pygame.font.SysFont(font_name, font_size)
            self.fonts.append(font)
        else:
            font = self.default_font
        def draw():
            nonlocal font
            text = font.render(stringf(), antialias, color, bg)
            self.window.blit(text, positionf())
        self.static.append(draw)
    def dynamic_label(self, stringf, color=BLUE, antialias=True, bg=None):
        """ Automatically positions rows of text in the top left corner - fewer args available """
        current_index = self.label_index
        self.label_index += 1
        def draw():
            text = self.default_font.render(stringf(), antialias, color, bg)
            self.window.blit(text, (10, 10+current_index*20))
        self.static.append(draw)

    def custom(self, draw_call):
        """ Put your own in I guess """
        self.dynamic.append(draw_call)

    def line(self, p1, p2, color=BLACK, line_width=1):
        """ Line between p1 and p2 """
        def draw():
            pygame.draw.line(self.window, color, self.convert(p1), self.convert(p2), line_width)
        self.static.append(draw)
    def vert_line(self, x, color=RED, height_frac=1, line_width=1):
        """ Vertical line at x """
        def draw():
            pygame.draw.line(self.window, color, self.convert((x, self.ymin*height_frac)), self.convert((x, self.ymax*height_frac)), line_width)
        self.static.append(draw)
    def horiz_line(self, y, color=RED, width_frac=1, line_width=1):
        """ Horizontal line at y """
        def draw():
            pygame.draw.line(self.window, color, self.convert((self.xmin*width_frac, y)), self.convert((self.xmax*width_frac, y)), line_width)
        self.static.append(draw)

    def arrow(self, p1, p2, color=BLACK, line_width=1):
        """ Nice looking arrow between p1 and p2, points to p2 """
        p1 = numpy.asarray(p1)
        p2 = numpy.asarray(p2)
        dp = (p2-p1)
        perpvec = numpy.asarray((dp[1], -dp[0]))
        def draw():
            #nonlocal p1,p2
            pygame.draw.line(self.window, color, self.convert(p1), self.convert(p2), line_width)
            pygame.draw.line(self.window, color, self.convert(p2), self.convert(p2 + perpvec/5 - (dp/5)), line_width)
            pygame.draw.line(self.window, color, self.convert(p2), self.convert(p2 - perpvec/5 - (dp/5)), line_width)
        self.static.append(draw)
    def dynamic_arrow(self, p1f, p2f, color=BLACK, line_width=1):
        """ Moves dynamically with function inputs for p1 and p2 """
        def draw():
            p1 = numpy.asarray(p1f())
            p2 = numpy.asarray(p2f())
            dp = (p2 - p1)
            tail_vec = numpy.asarray((dp[1], -dp[0]))/5 - dp/5  # makes vector to arrow head points
            #nonlocal p1,p2
            pygame.draw.line(self.window, color, self.convert(p1), self.convert(p2), line_width)
            pygame.draw.line(self.window, color, self.convert(p2), self.convert(p2 + tail_vec), line_width)
            pygame.draw.line(self.window, color, self.convert(p2), self.convert(p2 - tail_vec), line_width)
        self.static.append(draw)

    def polygon(self, *points, color=BLACK, line_width=3):
        def draw():
            pygame.draw.polygon(self.window, color, tuple(map(self.convert, points)), line_width)
        self.static.append(draw)

    def circle(self, center, radius, color=GREEN):
        def draw():
            pygame.draw.circle(self.window, color, self.convert(center), radius)
        self.static.append(draw)
    def dynamic_circle(self, centerf, radiusf, color=GREEN):
        def draw():
            pygame.draw.circle(self.window, color, self.convert(centerf()), radiusf())
        self.static.append(draw)

