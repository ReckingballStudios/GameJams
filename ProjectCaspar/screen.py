# File containing the Screen object


import pygame




class Screen:

    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps
        self.fpsClock = pygame.time.Clock()
        self.pyScreen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Project Caspar")


        # 1 / 100th the width and height respectively;
        # short for screenUnitX and screenUnitY
        self.sux = width / 100.0
        self.suy = height / 100.0
        pass

    def resetScreen(self, width, height):
        self.width = width
        self.height = height
        self.pyScreen = pygame.display.set_mode((self.width, self.height))
        pass



