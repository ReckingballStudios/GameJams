# File containing all variables for the screen

import pygame



class Screen:

    resolutions = [1920, 1080, 1440, 900]

    def __init__(self, width, height, FPS):
        self.width = width
        self.height = height
        self.screenUnitX = width / 1000.0    # A screenUnit is 1/1000th of a screen
        self.screenUnitY = height / 1000.0   # To account for any resolution the player wishes to have
        self.FPS = FPS
        self.fpsClock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        icon = pygame.image.load('sprites/icon.png')
        pygame.display.set_caption("Ecid Llor")
        pygame.display.set_icon(icon)

    def updateResolution(self):
        if self.width == Screen.resolutions[0]:
            self.width = Screen.resolutions[2]
            self.height = Screen.resolutions[3]
        else:
            self.width = Screen.resolutions[0]
            self.height = Screen.resolutions[1]

        self.screenUnitX = self.width / 1000.0
        self.screenUnitY = self.height / 1000.0
        self.screen = pygame.display.set_mode((self.width, self.height))





