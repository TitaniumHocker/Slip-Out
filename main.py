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
        self.choisePause = False

        pygame.mixer.pre_init(44100, 16, 2, 40960)
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font('res/fonts/16643.otf', 32)
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
        self.nameObject1 = NameObject(text, self.surface, (150, 468), name)
        self.objects.append(self.nameObject1)

    def createNameObject2(self, text, name):
        self.nameObject2 = NameObject(text, self.surface, (900, 468), name)
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
        # self.alert = pygame.mixer.Sound('res/soundFX/Alert.wav')
        # self.alert.set_volume(0.5)
        # self.bubbl = pygame.mixer.Sound('res/soundFX/bubbling_brook.wav')
        # self.bubbl.set_volume(0.5)
        # self.crowd = pygame.mixer.Sound('res/soundFX/crowd_outside.wav')
        # self.crowd.set_volume(0.5)

    def menu(self):
        self.surface.blit(pygame.image.load('res/img/menu.png')
                          .convert_alpha(), (0, 0))
        pygame.display.update()
        self.advance = 0
        for sign in 'Нажмите пробел для продолжения':
            self.textSurface = pygame.Surface((1280, 720), SRCALPHA)
            self.signSurface = self.font.render(sign, True,
                                                (228, 228, 228))
            self.textSurface.blit(self.signSurface,
                                  (200 + self.advance, 20))
            self.surface.blit(self.textSurface, (0, 0))
            pygame.display.update()
            pygame.time.delay(3)
            self.advance += self.font.metrics(sign)[0][4]
        pygame.mixer.music.load('res/music/Main Menu OST.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        while self.startUp:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.startUp = False

    def gameOverLogo(self):
        pygame.mixer.music.load('res/music/Outro OST.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()
        while True:
            self.surface.blit(pygame.image.load('res/img/scene-12.0.png')
                              .convert_alpha(), (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    def handleFX(self, fx, cmd):
        if fx == 'alert':
            if cmd == 'stop':
                self.alert.fadeout(500)
            elif cmd == 'play':
                self.alert = pygame.mixer.Sound('res/soundFX/Alert.wav')
                self.alert.set_volume(0.5)
                self.alert.play()
        elif fx == 'bubbl':
            if cmd == 'stop':
                self.bubbl.fadeout(500)
            elif cmd == 'play':
                self.bubbl = pygame.mixer.\
                             Sound('res/soundFX/bubbling_brook.wav')
                self.bubbl.set_volume(0.5)
                self.bubbl.play()
        elif fx == 'crowd':
            if cmd == 'stop':
                self.crowd.fadeout(500)
            elif cmd == 'play':
                self.crowd = pygame.mixer.\
                             Sound('res/soundFX/crowd_outside.wav')
                self.crowd.set_volume(0.5)
                self.crowd.play()

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
                elif splitedElements[0] == 'pause'\
                        and splitedElements[1].strip() == 'true':
                    self.choisePause = True
                    while self.choisePause:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    self.choisePause = False
                        self.draw()
                        pygame.display.update()
                elif splitedElements[0] == 'music':
                    pass
                elif splitedElements[0] == 'FX':
                    self.handleFX(splitedElements[1].strip(), 'play')
                elif splitedElements[0] == 'FXstop':
                    self.handleFX(splitedElements[1].strip(), 'stop')
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
            elif self.steps[self.step][0] == 'FX':
                self.handleFX(self.steps[self.step][1].strip(),
                              'play')
            elif self.steps[self.step][0] == 'FXstop':
                self.handleFX(self.steps[self.step][1].strip(),
                              'stop')
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
        self.menu()
        self.getReady()
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.handleSteps()
            pygame.display.update()
            self.clock.tick(self.frameRate)


def main():
    slipOut = Game('Slip Out', 1280, 720, 30)
    slipOut.run()


if __name__ == '__main__':
    main()
