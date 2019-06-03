# -*- coding:utf-8 -*-

import pygame
from pygame import SRCALPHA
import sys
from collections import defaultdict
import random
from datetime import datetime, timedelta
import os
import time
import pygame
from pygame.rect import Rect
from textWindow import TextWindow
from popUpObject import PopUpObject
from blackout import Blackout
from background import BackGround


class Game(object):
    def __init__(self, caption, width, height, frame_rate):
        # self.backgroundImage = pygame.image.load()
        self.frameRate = frame_rate
        self.gameOver = False
        self.objects = []
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((width, height), SRCALPHA)
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

    def update(self):
        for o in self.objects:
            o.update()

    def draw(self):
        for o in self.objects:
            self.surface.blit(o.draw(), (0, 0))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.background.upload('res/img/scene-02.0.png')
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP,
                                pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def createTextWindow(self):
        self.textWindow = TextWindow()
        self.objects.append(self.textWindow)

    def createArrow(self, img, pos):
        self.arrow = PopUpObject(img, pos)
        self.objects.append(self.arrow)

    def createBackground(self, img):
        self.background = BackGround(img)
        self.objects.append(self.background)

    def getReady(self):
        self.createBackground('res/img/scene-01.0.png')
        self.createTextWindow()
        self.createArrow('res/img/play.png', (1125, 620))

    def run(self):
        while not self.gameOver:
            # self.surface.blit()

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frameRate)


def main():
    slipOut = Game('Slip Out', 1280, 720, 30)
    slipOut.getReady()
    slipOut.run()


if __name__ == '__main__':
    main()
