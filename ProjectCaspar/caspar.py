


import pygame






class Caspar:





    def __init__(self, sux, suy):
        self.sux = sux
        self.suy = suy


        self.x = self.getX(-50)
        self.y = self.getY(80)
        self.dx = 0
        self.dy = 0
        self.speedX = self.getX(0.5)
        self.speedY = self.getY(0.7)

        self.west = False
        self.north = False
        self.east = False
        self.south = False
        pass


    def handleKeyboard(self, event, screen):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.west = True
            elif event.key == pygame.K_w:
                self.north = True
            elif event.key == pygame.K_d:
                self.east = True
            elif event.key == pygame.K_s:
                self.south = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.west = False
            elif event.key == pygame.K_w:
                self.north = False
            elif event.key == pygame.K_d:
                self.east = False
            elif event.key == pygame.K_s:
                self.south = False
        pass


    def update(self):
        self.dx = 0
        self.dy = 0
        if self.north:
            self.dy -= self.speedY
        if self.east:
            self.dx += self.speedX
        if self.south:
            self.dy += self.speedY
        if self.west:
            self.dx -= self.speedX


        pass



    def getX(self, percent):
        return percent * self.sux

    def getY(self, percent):
        return percent * self.suy

























