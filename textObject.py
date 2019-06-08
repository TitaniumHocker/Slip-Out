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


class TextObject(Sprite):
    def __init__(self, txt, surface):
        Sprite.__init__(self)
        self.surface = Surface((1280, 720), SRCALPHA)
        self.txt = txt.split('&')
        # self.pos = [(90, x + 515) for x in range(0, 600, 25)]
        self.pos = [x + 515 for x in range(0, 600, 25)]
        self.font = font.SysFont(None, 30)
        self.screen = surface
        self.render(self.screen)
        self.first = True

    def upload(self, text, surface):
        self.txt = text.split('&')
        self.render(surface)

    def update(self):
        pass

    def render(self, surface):
        self.surface = Surface((1280, 720), SRCALPHA)
        surface.blit(self.surface, (0, 0))
        display.update()
        for i, txt in enumerate(self.txt):
            for k, sign in enumerate(txt.strip()):
                self.signSurface = Surface((1280, 720), SRCALPHA)
                self.textSurface = self.font.render(sign, True, colour)
                self.signSurface.blit(self.textSurface,
                                      (k * 11 + 90, self.pos[i]))
                self.surface.blit(self.textSurface, (k * 11 + 90, self.pos[i]))
                surface.blit(self.signSurface, (0, 0))
                display.update()
                delay(3)
        self.first = False

    def draw(self, surface, typing=False):
        if self.first:
            self.render(surface)
        else:
            surface.blit(self.surface, (0, 0))
