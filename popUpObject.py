# -*- coding:utf-8 -*-

from pygame.sprite import Sprite
from pygame import Surface
from pygame import image
from pygame import display
from pygame import SRCALPHA
from pygame import Color


class PopUpObject(Sprite):
    def __init__(self, img, pos=(0, 0), slowly=False):
        Sprite.__init__(self)
        self.surface = Surface((1280, 720), SRCALPHA)
        self.image = image.load(img).convert_alpha()
        self.surface.blit(self.image, pos)
        self.slowly = slowly
        self.pos = pos
        self.name = 'popUp'

    def upload(self, img):
        self.image = image.load(img).convert_alpha()
        self.surface = Surface((1280, 720), SRCALPHA)
        self.surface.blit(self.image, self.pos)

    def draw(self, surface):
        surface.blit(self.surface, (0, 0))

    def updatePos(self, pos):
        self.pos = pos

    def update(self):
        pass
