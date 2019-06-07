# -*- coding: utf-8 -*-

from pygame.sprite import Sprite
from pygame import Surface
from pygame import image
from pygame import display
from pygame import SRCALPHA
from pygame import Color


class BackGround(Sprite):
    def __init__(self, img):
        Sprite.__init__(self)
        self.surface = Surface((1280, 720), SRCALPHA)
        self.image = image.load(img).convert_alpha()
        self.surface.blit(self.image, (0, 0))

    def upload(self, img):
        self.image = image.load(img).convert_alpha()
        self.surface.fill(Color("black"))
        self.surface.blit(self.image, (0, 0))

    def draw(self, surface):
        surface.blit(self.surface, (0, 0))

    def update(self):
        pass
