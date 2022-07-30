
"""
Mason Reck
"""

import pygame
import background
import caspar


class Game:




    def __init__(self, sux, suy):
        self.sux = sux
        self .suy = suy


        self.caspar = caspar.Caspar(sux, suy)
        self.background = background.Background(sux, suy, -self.getX(50))

        pass








    def handleMouse(self, event, screen):

        pass

    def handleKeyboard(self, event, screen):

        self.caspar.handleKeyboard(event, screen)

        pass




    def update(self):

        self.caspar.update()
        self.background.update(self.caspar.dx)

        pass




    def draw(self, pyScreen):

        self.background.draw(pyScreen)

        pass




    def getX(self, percent):
        return percent * self.sux

    def getY(self, percent):
        return percent * self.suy







