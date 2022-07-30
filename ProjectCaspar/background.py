


import pygame



class Background:

    NUM = 3

    def __init__(self, sux, suy, x):
        self.sux = sux
        self.suy = suy

        self.x = [x for i in range(Background.NUM)]

        self.sprites = []
        self.initSprites()
        pass



    def initSprites(self):
        # Sunny background
        self.sprites.append(pygame.image.load('Sprites/Backgrounds/DesertPlanetSky.png'))
        self.sprites[0] = pygame.transform.scale(self.sprites[0], (self.getX(100), self.getY(100)))

        # Background Layer 1
        self.sprites.append(pygame.image.load('Sprites/Backgrounds/DesertPlanetBackgroundLayer1.png'))
        self.sprites[1] = pygame.transform.scale(self.sprites[1], (self.getX(200), self.getY(100)))

        # Background Layer 2
        self.sprites.append(pygame.image.load('Sprites/Backgrounds/DesertPlanetBackgroundLayer2.png'))
        self.sprites[2] = pygame.transform.scale(self.sprites[2], (self.getX(200), self.getY(100)))
        pass



    def draw(self, pyScreen):
        pyScreen.blit(self.sprites[0], (0, 0))
        for i in range(1, Background.NUM):
            pyScreen.blit(self.sprites[i], (self.x[i], 0))

        pass




    def update(self, dx):
        for i in range(len(self.x)):
            self.x[i] -= i * 0.25 * dx

        pass




    def getX(self, percent):
        return percent * self.sux
    def getY(self, percent):
        return percent * self.suy




