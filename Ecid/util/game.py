
"""
Game Object


TODO LIST:

Add the science and food dice
Create filters 1-6 for the resource dice
program dice rolls for resource dice
sequentially add functionality for movement Dice
Reskin for movement dice
Add Turrets, obstacles etc.
Mechanic idea, lay out resources on track, choose which resource you are going for, the roll movement dice
    Concept is that you have to guess which tile you will land on, and since the 4 movement dice are 0-1,
    You can use combinatorics to help you


"""
import string

import pygame
import random
import math


class Game:


    """
    Initialize Game Object
    """

    townImage = pygame.image.load('sprites/town256.png')
    labImage = pygame.image.load('sprites/labSymbol.png')
    militaryImage = pygame.image.load('sprites/MilitarySymbol.png')
    foodImage = pygame.image.load('sprites/foodSymbol.png')


    def __init__(self, screen):
        self.gameState = "Player's Turn"
        self.fontGrand = pygame.font.Font('freesansbold.ttf', int(40 * screen.screenUnitX))
        self.fontLargeSelected = pygame.font.Font('freesansbold.ttf', int(22.0 * screen.screenUnitX))
        self.fontLarge = pygame.font.Font('freesansbold.ttf', int(20.0 * screen.screenUnitX))
        self.fontSmall = pygame.font.Font('freesansbold.ttf', int(12.0 * screen.screenUnitX))
        self.menuTiles = []
        self.initializeMenuTiles(screen)
        self.gameTiles = []
        self.initializeGameTiles(screen)
        self.selectedGameTile = 0
        self.turn = 0
        self.movementDice = []
        self.scrambleTimer = 0
        self.initializeMovementDice(screen)
        self.resourceDice = []
        self.scrambleTimer2 = 0
        self.science = 0
        self.military = 0
        self.food = 0
        self.initializeResourceDice(screen)
        self.resourceDieSelected = 0
        self.rollButtons = []
        self.initializeRollButtons(screen)
        self.dieSelected = -1


    def initializeMenuTiles(self, screen):
        for i in range(MenuTile.numMenuTiles):
            menuTileX = (i * screen.screenUnitX * 130)
            menuTileY = screen.screenUnitY * 10
            self.menuTiles.append(MenuTile(screen, menuTileX, menuTileY, i))

    def initializeGameTiles(self, screen):
        for i in range(GameTile.numGameTiles):
            gameTileX = 0
            gameTileY = 0
            orientation = 0
            if i < 16:
                orientation = 0
                gameTileX = (i * 64) + 320
                gameTileY = screen.screenUnitY * 125
            elif i < 19:
                orientation = 1
                gameTileX = (15 * 64) + 320
                gameTileY = (64 * (i-15)) + (screen.screenUnitY * 125)
            elif i < 38:
                orientation = 0
                gameTileX = 1280 - (64 * (i-18))
                gameTileY = 192 + (screen.screenUnitY * 125)
            elif i < 41:
                orientation = 1
                gameTileX = 64
                gameTileY = (64 * (i - 37)) + 192 + (screen.screenUnitY * 125)
            elif i < 57:
                orientation = 0
                gameTileX = 64 + (64 * (i-40))
                gameTileY = 384 + (screen.screenUnitY * 125)

            self.gameTiles.append(GameTile(screen, gameTileX, gameTileY, i, orientation))

    def initializeMovementDice(self, screen):
        for i in range(MovementDice.numDice):
            dieX = (i * 85) + 520
            dieY = 650
            self.movementDice.append(MovementDice(dieX, dieY, 0))

    def initializeResourceDice(self, screen):
        for i in range(ResourceDice.numDice):
            dieX = (i * 115) + 64
            dieY = 650
            self.resourceDice.append(ResourceDice(dieX, dieY, 0, i))

    def initializeRollButtons(self, screen):
        x = 78
        y = 750
        self.rollButtons.append(RollButton(x, y, True))
        x = 555
        y = 750
        self.rollButtons.append(RollButton(x, y, False))


    def handleInput(self, event, screen):
        self.handleMouse(event, screen)

    def handleMouse(self, event, screen):
        pos = pygame.mouse.get_pos()

        # Menu Tiles
        for i in range(MenuTile.numMenuTiles):
            distanceX = pos[0] - self.menuTiles[i].x
            distanceY = pos[1] - self.menuTiles[i].y

            if 0 < distanceX < self.menuTiles[i].size and 0 < distanceY < self.menuTiles[i].sizeY:
                self.menuTiles[i].isSelected = True
                if i == 0 and event.type == pygame.MOUSEBUTTONUP:
                    exit()
                if i == 1 and event.type == pygame.MOUSEBUTTONUP:
                    screen.updateResolution()
                    self.menuTiles[i].updateResolutionText(screen)

            else:
                self.menuTiles[i].isSelected = False

        # Game Tiles
        for i in range(GameTile.numGameTiles):
            distanceX = pos[0] - self.gameTiles[i].x
            distanceY = pos[1] - self.gameTiles[i].y

            if 0 < distanceX < 64 and 0 < distanceY < 64:
                self.gameTiles[i].isSelected = True
                self.selectedGameTile = i
            else:
                self.gameTiles[i].isSelected = False

        # Resource Dice Selection
        for i in range(ResourceDice.numDice):
            distanceX = pos[0] - self.resourceDice[i].x
            distanceY = pos[1] - self.resourceDice[i].y
            if 0 < distanceX < 64 and 0 < distanceY < 64:
                self.resourceDice[i].isSelected = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.resourceDieSelected = i
            else:
                self.resourceDice[i].isSelected = False


        # Roll Buttons
        for i in range(2):
            distanceX = pos[0] - self.rollButtons[i].x
            distanceY = pos[1] - self.rollButtons[i].y

            if 0 < distanceX < 256 and 0 < distanceY < 128:
                self.rollButtons[i].isSelected = True
                if event.type == pygame.MOUSEBUTTONUP:
                    # Roll the RESOURCE DICE
                    if i == 0:
                        self.rollResourceDice()
                    # Roll the MOVEMENT DICE
                    elif i == 1:
                        self.rollMovementDice()
            else:
                self.rollButtons[i].isSelected = False

    def rollResourceDice(self):
        test = 0

    def rollMovementDice(self):
        test = 0

    def update(self):
        test = 0


    def draw(self, screen):
        tint = 35
        screen.fill((tint, tint, tint))
        self.drawGame(screen)
        self.drawGameTiles(screen)
        self.drawMenuTiles(screen)
        self.drawMovementDice(screen)
        self.drawResourceDice(screen)
        self.drawRollButtons(screen)

    def drawGame(self, screen):
        screen.blit(Game.townImage, (50, 25))
        symbolX = 400
        symbolY = 25
        symbolSpacing = 235
        screen.blit(Game.labImage, (symbolX, symbolY))
        screen.blit(Game.militaryImage, ((symbolX + symbolSpacing), symbolY))
        screen.blit(Game.foodImage, ((symbolX + 2*symbolSpacing), symbolY))

        textYOffset = 5
        # Science Text
        text = self.fontGrand.render("{}".format(self.science), True, (0, 0, 0))
        textRect = text.get_rect()
        screen.blit(text, (textRect.x + symbolX + 80, textRect.y + symbolY + textYOffset))

        # Military Text
        text = self.fontGrand.render("{}".format(self.military), True, (0, 0, 0))
        textRect = text.get_rect()
        screen.blit(text, (textRect.x + symbolX + symbolSpacing + 80, textRect.y + symbolY + textYOffset))

        # Food Text
        text = self.fontGrand.render("{}".format(self.food), True, (0, 0, 0))
        textRect = text.get_rect()
        screen.blit(text, (textRect.x + symbolX + 80 + 2*symbolSpacing, textRect.y + symbolY + textYOffset))


    def drawMenuTiles(self, screen):
        for i in range(MenuTile.numMenuTiles):
            if self.menuTiles[i].isSelected:
                text = self.fontLargeSelected.render(self.menuTiles[i].text, True, (0, 0, 0))
            else:
                text = self.fontLarge.render(self.menuTiles[i].text, True, (0, 0, 0))

            textRect = text.get_rect()
            screen.blit(text, ((textRect.x + self.menuTiles[i].x), (textRect.y + self.menuTiles[i].y)))

        # TILE NUMBER
        text = self.fontLarge.render("Tile: {}".format(self.selectedGameTile), True, (0, 0, 0))
        textRect = text.get_rect()
        screen.blit(text, (textRect.x + 1150, textRect.y + 25))
        # TURN NUMBER
        text = self.fontLarge.render("Turn: {}".format(self.turn), True, (0, 0, 0))
        textRect = text.get_rect()
        screen.blit(text, (textRect.x + 1265, textRect.y + 25))

    def drawGameTiles(self, screen):
        for i in range(GameTile.numGameTiles):
            screen.blit(self.gameTiles[i].image, (self.gameTiles[i].x, self.gameTiles[i].y))
            if self.gameTiles[i].isSelected:
                screen.blit(self.gameTiles[i].filter, (self.gameTiles[i].x, self.gameTiles[i].y))

    def drawMovementDice(self, screen):
        for i in range(MovementDice.numDice):
            if self.scrambleTimer > 0:
                self.scrambleTimer -= 1
                screen.blit(self.movementDice[i].image[int(self.scrambleTimer / 10) % 2], (self.movementDice[i].x, self.movementDice[i].y))
            else:
                screen.blit(self.movementDice[i].image[self.movementDice[i].value], (self.movementDice[i].x, self.movementDice[i].y))

        # MOVEMENT DICE TEXT
        text = self.fontLarge.render("Movement Dice", True, (0, 0, 0))
        textRect = text.get_rect()
        screen.blit(text, (textRect.x + 575, textRect.y + 600))

    def drawResourceDice(self, screen):
        for i in range(ResourceDice.numDice):
            if self.scrambleTimer2 > 0:
                self.scrambleTimer2 -= 1
                # screen.blit(self.resourceDice[i].image[int(self.scrambleTimer2 / 10) % 2], (self.resourceDice[i].x, self.resourceDice[i].y))
            else:
                screen.blit(self.resourceDice[i].image[0], (self.resourceDice[i].x, self.resourceDice[i].y))
                if self.resourceDice[i].isSelected or self.resourceDieSelected == i:
                    screen.blit(self.resourceDice[i].image[1], (self.resourceDice[i].x, self.resourceDice[i].y))

        # RESOURCE DICE TEXT
        text = self.fontLarge.render("Resource Dice", True, (0, 0, 0))
        textRect = text.get_rect()
        screen.blit(text, (textRect.x + 118, textRect.y + 600))

    def drawRollButtons(self, screen):
        for i in range(2):
            screen.blit(RollButton.rollButton, (self.rollButtons[i].x, self.rollButtons[i].y))
            if self.rollButtons[i].canRoll:
                screen.blit(RollButton.rollText, (self.rollButtons[i].x, self.rollButtons[i].y))
                if self.rollButtons[i].isSelected:
                    screen.blit(RollButton.rollSelected, (self.rollButtons[i].x, self.rollButtons[i].y))



class MovementDice:
    # These are static and final elements of the object Die
    numDice = 4

    def __init__(self, dieX, dieY, value):
        self.x = dieX
        self.y = dieY
        self.value = value
        self.image = []
        self.image.append(pygame.image.load('sprites/lightDie0.png'))
        self.image.append(pygame.image.load('sprites/lightDie1.png'))

class ResourceDice:
    numDice = 3

    def __init__(self, dieX, dieY, value, index):
        self.x = dieX
        self.y = dieY
        self.value = value
        self.index = index
        self.isSelected = False
        self.image = []
        #if index == 1:
        self.image.append(pygame.image.load('sprites/militaryDie.png'))
        self.image.append(pygame.image.load('sprites/militaryDieSelected.png'))

class MenuTile:
    numMenuTiles = 1

    def __init__(self, screen, x, y, index):
        self.x = x
        self.y = y
        self.index = index
        self.size = int(150 * screen.screenUnitX)
        self.sizeY = int(30 * screen.screenUnitY)
        self.isSelected = False
        self.menuTileText = ["    Exit", "{}x{}".format(screen.width, screen.height), "Placeholder", "Placeholder", "Placeholder"]
        self.text = self.menuTileText[index]

    def updateResolutionText(self, screen):
        self.menuTileText[1] = "{}x{}".format(screen.width, screen.height)
        self.text = self.menuTileText[self.index]

class GameTile:
    numGameTiles = 57

    def __init__(self, screen, x, y, index, orientation):
        self.x = x
        self.y = y
        self.index = index
        self.size = int(50 * screen.screenUnitX)
        self.image = pygame.image.load('sprites/pathHori.png')
        if orientation == 1:
            self.image = pygame.image.load('sprites/pathVert.png')
        self.filter = pygame.image.load('sprites/selectionFilter.png')
        self.selected = False

class RollButton:
    rollButton = pygame.image.load('sprites/RollButton.png')
    rollText = pygame.image.load('sprites/RollText.png')
    rollSelected = pygame.image.load('sprites/rollButtonSelected.png')

    def __init__(self, x, y, canRoll):
        self.x = x
        self.y = y
        self.isSelected = False
        self.canRoll = canRoll


class Functions:

    @staticmethod
    def flip(boolValue):
        if boolValue:
            return False
        else:
            return True


