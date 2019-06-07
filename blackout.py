# -*- coding:utf-8 -*-

from pygame.sprite import Sprite
from pygame import Surface
from pygame import image
from pygame import display
from pygame import SRCALPHA


class Blackout(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.surface = Surface((1280, 720), SRCALPHA)
        self.image = image.load(img).convert_alpha()
        self.surface.blit(self.image, (0, 0))

    def upload(self, img):
        self.image = image.load(img).convert_alpha()
        self.surface.blit(self.image, (0, 0))

    def draw(self):
        return self.surface

    def update(self):
        pass
