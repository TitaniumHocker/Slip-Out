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
from textObject import TextObject


class Game(object):
    def __init__(self, caption, width, height, frame_rate):
        self.frameRate = frame_rate
        self.gameOver = False
        self.objects = []
        self.steps = []
        self.step = 0
        self.pause = False
        self.startUp = True

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
        for obj in self.objects:
            obj.update()

    def draw(self):
        for obj in self.objects:
            obj.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # sys.exit()
            elif event.type == pygame.KEYUP:
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause = False
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP,
                                pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def uploadInstructions(self):
        with open('instructions.txt', 'r') as instructions:
            for step in instructions.read().split('$')[1::]:
                self.steps.append(step.split(':'))

    def createTextWindow(self):
        self.textWindow = TextWindow()
        self.objects.append(self.textWindow)

    def createArrow(self, img='res/img/play.png', pos=(1125, 620)):
        self.arrow = PopUpObject(img, pos)
        self.objects.append(self.arrow)

    def createBackground(self, img):
        self.background = BackGround(img)
        self.objects.append(self.background)

    def createTextObject(self, text, pos=(90, 515)):
        self.textObject = TextObject(text, pos)
        self.objects.append(self.textObject)

    def getReady(self):
        self.uploadInstructions()
        self.createBackground('res/img/menu.png')
        self.createTextWindow()
        self.createTextObject('')
        self.createArrow()

    def handleSteps(self):
        while not self.pause:
            if self.steps[self.step][0] == 'pause' and self.steps[self.step][1].strip() == 'true':
                self.pause = True
            elif self.steps[self.step][0] == 'background':
                self.background.upload(self.steps[self.step][1].strip())
            elif self.steps[self.step][0] == 'music':
                self.music = self.steps[self.step][1].strip()
            elif self.steps[self.step][0] == 'text':
                self.textObject.upload(self.steps[self.step][1].strip())
            elif self.steps[self.step][0] == 'gameover' and self.steps[self.step][1].strip() == 'true':
                self.pause = True
                self.gameOver = True
            self.step += 1

    def run(self):
        while not self.gameOver:
            self.handleSteps()
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
