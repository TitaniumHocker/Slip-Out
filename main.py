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
from background import BackGround
from textObject import TextObject
from nameObject import NameObject
import config as cfg


class Game(object):
    def __init__(self, caption, width, height, frame_rate):
        self.frameRate = frame_rate
        self.gameOver = False
        self.objects = []
        self.steps = []
        self.step = 0
        self.pause = False
        self.startUp = True
        self.awaitChoise = False

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

    def draw(self, passed='None'):
        for obj in self.objects:
            if obj.name == passed or obj.name in passed:
                pass
            else:
                obj.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.awaitChoise:
                    self.pause = False
                elif event.key == pygame.K_1 and self.awaitChoise:
                    self.awaitChoise = False
                    if '|' in self.choises[0]:
                        self.gameOver = True
                        self.choiseHandler(self.choises[0])
                    else:
                        self.choiseHandler(self.choises[0])
                elif event.key == pygame.K_2 and self.awaitChoise:
                    self.awaitChoise = False
                    if '|' in self.choises[1]:
                        self.gameOver = True
                        self.choiseHandler(self.choises[1])
                    else:
                        self.choiseHandler(self.choises[1])
                else:
                    pass
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP,
                                pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def uploadInstructions(self):
        with open('instructions.txt', 'r', encoding='utf-8') as instructions:
            for step in instructions.read().split('$')[1::]:
                self.steps.append(step.split(':'))

    def createTextWindow(self):
        self.textWindow = TextWindow('res/img/dialog.png')
        self.objects.append(self.textWindow)

    def createArrow(self, img, pos=cfg.arrowPos):
        self.arrow = PopUpObject(img, pos)
        self.objects.append(self.arrow)

    def createBackground(self, img):
        self.background = BackGround(img)
        self.objects.append(self.background)

    def createTextObject(self, text):
        self.textObject = TextObject(text, self.surface)
        self.objects.append(self.textObject)

    def createNameObject1(self, text, name):
        self.nameObject1 = NameObject(text, self.surface, (150, 470), name)
        self.objects.append(self.nameObject1)

    def createNameObject2(self, text, name):
        self.nameObject2 = NameObject(text, self.surface, (900, 470), name)
        self.objects.append(self.nameObject2)

    def createPerson1(self, img, pos):
        self.person1 = PopUpObject(img, pos)
        self.objects.append(self.person1)

    def createPerson2(self, img, pos):
        self.person2 = PopUpObject(img, pos)
        self.objects.append(self.person2)

    def createPopUp1(self, img, pos):
        self.popUp1 = PopUpObject(img, pos)
        self.objects.append(self.popUp1)

    def createPopUp2(self, img, pos):
        self.popUp2 = PopUpObject(img, pos)
        self.objects.append(self.popUp2)

    def getReady(self):
        self.uploadInstructions()
        self.createBackground('res/img/none.png')
        self.createPopUp1('res/img/none.png', cfg.popUp1Pos)
        self.createPopUp2('res/img/none.png', cfg.popUp2pos)
        self.createPerson1('res/img/none.png', cfg.hero1Pos)
        self.createPerson2('res/img/none.png', cfg.hero2Pos)
        self.createTextWindow()
        self.createArrow('res/img/none.png')
        self.createTextObject('')
        self.createNameObject1('', 'name1')
        self.createNameObject2('', 'name2')

    def gameOverLogo(self):
        while True:
            self.surface.blit(pygame.image.load('res/img/scene-12.0.png')
                              .convert_alpha(), (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.quit()

    def choiseHandler(self, choise):
        if '@' not in choise:
            self.draw('TextObject')
            self.textObject.upload(choise.split('=')[1].strip(),
                                   self.surface)
        else:
            for el in choise.split('@'):
                splitedElements = el.split('=')
                if splitedElements[0] == 'text':
                    self.draw('TextObject')
                    self.textObject.upload(splitedElements[1].strip(),
                                           self.surface)
                elif splitedElements[0] == 'music':
                    pass
                elif splitedElements[0] == 'name1':
                    self.draw('name1')
                    self.nameObject1.upload(splitedElements[1].strip(),
                                            self.surface)
                elif splitedElements[0] == 'name2':
                    self.draw('name2')
                    self.nameObject2.upload(splitedElements[1].strip(),
                                            self.surface)
                elif splitedElements[0] == 'person1':
                    self.person1.upload(splitedElements[1].strip())
                elif splitedElements[0] == 'person2':
                    self.person2.upload(splitedElements[1].strip())
                elif splitedElements[0] == 'background':
                    self.background.upload(splitedElements[1].strip())
                elif splitedElements[0] == 'textwindow':
                    self.textWindow.upload(splitedElements[1].strip())

    def handleSteps(self):
        while not self.pause:
            if self.gameOver:
                self.gameOverLogo()
            elif self.steps[self.step][0] == 'pause'\
                    and self.steps[self.step][1].strip() == 'true':
                self.pause = True
            elif self.steps[self.step][0] == 'background':
                self.background.upload(self.steps[self.step][1].strip())
            elif self.steps[self.step][0] == 'music':
                self.music = self.steps[self.step][1].strip()
            elif self.steps[self.step][0] == 'text':
                self.draw('TextObject')
                self.textObject.upload(self.steps[self.step][1].strip(),
                                       self.surface)
            elif self.steps[self.step][0] == 'person1':
                self.person1.upload(self.steps[self.step][1].strip())
            elif self.steps[self.step][0] == 'person2':
                self.person2.upload(self.steps[self.step][1].strip())
            elif self.steps[self.step][0] == 'name1':
                self.draw('name1')
                self.nameObject1.upload(self.steps[self.step][1], self.surface)
            elif self.steps[self.step][0] == 'name2':
                self.draw('name2')
                self.nameObject2.upload(self.steps[self.step][1], self.surface)
            elif self.steps[self.step][0] == 'choise':
                self.awaitChoise = True
                self.pause = True
                self.choises = self.steps[self.step][1].split(';')
            elif self.steps[self.step][0] == 'textwindow':
                self.textWindow.upload(self.steps[self.step][1].strip())
            elif self.steps[self.step][0] == 'popup1':
                self.parsedPopUp1 = self.steps[self.step][1].split('&')
                self.popUp1.upload(self.parsedPopUp1[0].strip())
            elif self.steps[self.step][0] == 'popup2':
                self.parsedPopUp2 = self.steps[self.step][1].split('&')
                self.popUp2.upload(self.parsedPopUp2[0].strip())
            elif self.steps[self.step][0] == 'gameover'\
                    and self.steps[self.step][1].strip() == 'true':
                self.pause = True
                self.gameOver = True
                self.gameOverLogo()
            self.step += 1

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.handleSteps()
            pygame.display.update()
            self.clock.tick(self.frameRate)


def main():
    slipOut = Game('Slip Out', 1280, 720, 30)
    slipOut.getReady()
    slipOut.run()


if __name__ == '__main__':
    main()
