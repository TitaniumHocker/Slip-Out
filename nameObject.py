# -*- coding:utf-8 -*-

from pygame.sprite import Sprite
from pygame import Surface
from pygame import image
from pygame import display
from pygame import SRCALPHA
from pygame import font
from pygame import Color
from pygame.time import delay
from pygame import display

colour = (25, 25, 25)


class NameObject(Sprite):
    def __init__(self, txt, surface, pos, name):
        Sprite.__init__(self)
        self.surface = Surface((1280, 720), SRCALPHA)
        self.txt = txt
        self.pos = pos
        self.font = font.Font('res/fonts/16643.otf', 20)
        self.screen = surface
        self.render(self.screen)
        self.first = True
        self.name = name

    def upload(self, text, surface):
        self.txt = text
        self.render(surface)

    def update(self):
        pass

    def render(self, surface):
        self.surface = Surface((1280, 720), SRCALPHA)
        surface.blit(self.surface, (0, 0))
        display.update()
        for i, txt in enumerate(self.txt):
            self.signSurface = Surface((1280, 720), SRCALPHA)
            self.textSurface = self.font.render(txt, True, colour)
            self.signSurface.blit(self.textSurface,
                                  (i * 11 + self.pos[0], self.pos[1]))
            self.surface.blit(self.textSurface,
                              (i * 11 + self.pos[0], self.pos[1]))
            surface.blit(self.signSurface, (0, 0))
            display.update()
            delay(3)
        self.first = False

    def draw(self, surface, typing=False):
        if self.first:
            self.render(surface)
        else:
            surface.blit(self.surface, (0, 0))
