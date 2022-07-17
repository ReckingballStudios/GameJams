
"""
Game Object


TODO LIST:

Add the science and food dice √
Create filters 1-6 for the resource dice √
program dice rolls for resource dice √
sequentially add functionality for movement Dice √


DEV HACK LINE 238 ATM
upgrade military Resource png
fix target image
animate pickup item moving to the resource tracker
better movement Dice Roll animation to match resource Dice
Reskin for movement dice
Add Turrets, obstacles etc.
Mechanic idea, lay out resources on track, choose which resource you are going for, then roll movement dice
    Concept is that you have to guess which tile you will land on, and since the 4 movement dice are 0-1,
    You can use combinatorics to help you
Sound Design, Dice Roll Sound

"""
import string

import pygame
import random
import math


class Game:


    """
    Initialize Game Object
    """

    tutorialRunning = False

    townImage = pygame.image.load('sprites/town256.png')
    labImage = pygame.image.load('sprites/labSymbol.png')
    militaryImage = pygame.image.load('sprites/MilitarySymbol.png')
    foodImage = pygame.image.load('sprites/foodSymbol.png')
    upgradeBtnImage = pygame.transform.scale(pygame.image.load('sprites/pathHori.png'), (256, 64))
    upgradeGreenImage = pygame.transform.scale(pygame.image.load('sprites/greenFilter.png'), (256, 64))
    upgradeRedImage = pygame.transform.scale(pygame.image.load('sprites/redFilter.png'), (256, 64))
    lightDieFace = pygame.image.load('sprites/lightDieFace.png')
    peopleImage = pygame.image.load('sprites/people.png')
    greenFilter = pygame.image.load('sprites/greenFilter.png')
    redFilter = pygame.image.load('sprites/redFilter.png')
    chainsImage = pygame.image.load('sprites/chainedTile.png')
    diceNumberImages = []
    for i in range(6):
        diceNumberImages.append(pygame.image.load('sprites/Die{}.png'.format(i+1)))
    tokenImages = [pygame.image.load('sprites/labToken.png'),
                   pygame.image.load('sprites/militaryToken.png'),
                   pygame.image.load('sprites/foodToken.png')]

    numTurrets = 4
    baseTurretImage = pygame.transform.scale(pygame.image.load('sprites/Turret.png'), (128, 128))
    turret180Image = pygame.transform.scale(pygame.image.load('sprites/turret180.png'), (128, 128))
    turretFlameImage = pygame.transform.scale(pygame.image.load('sprites/turretFlame.png'), (128, 128))

    turretImage = [
                    [
                        baseTurretImage,
                        pygame.transform.rotate(baseTurretImage, -90)
                    ],
                    [
                        turret180Image,
                        pygame.transform.rotate(turret180Image, 90)
                    ],
                    [
                        pygame.transform.rotate(turretFlameImage, 180),
                        pygame.transform.rotate(turretFlameImage, 270),
                        turretFlameImage
                    ],
                    [
                        pygame.transform.rotate(turretFlameImage, 180),
                        pygame.transform.rotate(turretFlameImage, 90),
                        turretFlameImage
                    ]
                   ]
    turretPos = [(675, 175), (870, 175), (1150, 175), (130, 370)]
    targetImage = pygame.image.load('sprites/target.png')
    upgradeCosts = [10, 20, 30, 50, 10000]
    upgrades = [0, 0, 0]
    upgradeTexts = [
        "{}: +1 Movement Die",
        "{}: +25% Damage",
        "{}: +1 Soldier Token"
    ]
    skrymirImages = [
        pygame.transform.scale(pygame.image.load('sprites/skrymir_powerless.png'), (64, 64)),
        pygame.transform.scale(pygame.image.load('sprites/skrymir.png'), (64, 64)),
        pygame.transform.flip(pygame.transform.scale(pygame.image.load('sprites/skrymir_powerless.png'), (64, 64)), True, False),
        pygame.transform.flip(pygame.transform.scale(pygame.image.load('sprites/skrymir.png'), (64, 64)), True, False)
    ]

    def __init__(self, screen):
        self.gameState = "Next Turn"
        self.fontColossal = pygame.font.Font('freesansbold.ttf', int(150 * screen.screenUnitX))
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
        self.movementRoll = 0
        self.movementDice = []
        self.scrambleTimer = 0
        self.initializeMovementDice(screen)
        self.resourceDice = []
        self.tokensAtBase = 3
        self.damage = 1.0
        self.score = 0
        self.resourceRoll = 0
        self.science = 10
        self.military = 0
        self.food = 0
        self.initializeResourceDice(screen)
        self.resourceDieSelected = 0
        self.rollButtons = []
        self.initializeRollButtons(screen)
        self.dieSelected = -1
        self.upgradeButtons = []
        self.initializeUpgradeButtons(screen)




        if self.gameState == "Next Turn":
            self.nextTurn()

    def resetMovementDice(self):
        for i in range(MovementDice.numDice):
            self.movementDice[i].value = 0

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
        self.movementDice.clear()
        for i in range(MovementDice.numDice):
            dieX = (i * 85) + 490
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
        self.rollButtons.append(GameButton(x, y))
        x = 555
        y = 750
        self.rollButtons.append(GameButton(x, y))

    def initializeUpgradeButtons(self, screen):
        x = 1000
        y = 650
        self.upgradeButtons.append(GameButton(x, y))
        y = 735
        self.upgradeButtons.append(GameButton(x, y))
        y = 820
        self.upgradeButtons.append(GameButton(x, y))

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
                    Game.tutorialRunning = True
                if i == 2 and event.type == pygame.MOUSEBUTTONUP:
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
                if self.gameState == "Select Movement" and event.type == pygame.MOUSEBUTTONUP:
                    self.moveToken(i)


                """
                DEV HACK!!! REMOVE BEFORE RELEASE
                """
                if event.type == pygame.KEYUP:
                    self.gameTiles[i].isOccupied = True
            else:
                self.gameTiles[i].isSelected = False

        # Resource Dice Selection
        for i in range(ResourceDice.numDice):
            distanceX = pos[0] - self.resourceDice[i].x
            distanceY = pos[1] - self.resourceDice[i].y
            if 0 < distanceX < 64 and 0 < distanceY < 64 and self.gameState == "Roll Resource Dice":
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
                    if i == 0 and self.gameState == "Roll Resource Dice":
                        self.rollResourceDice()
                    # Roll the MOVEMENT DICE
                    elif i == 1 and self.gameState == "Roll Movement Dice":
                        self.rollMovementDice()
            else:
                self.rollButtons[i].isSelected = False

        # Upgrade Buttons
        for i in range(3):
            distanceX = pos[0] - self.upgradeButtons[i].x
            distanceY = pos[1] - self.upgradeButtons[i].y

            if 0 < distanceX < 256 and 0 < distanceY < 64:
                self.upgradeButtons[i].isSelected = True
                if i == 0 and self.science >= Game.upgradeCosts[Game.upgrades[i]]:
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.science -= Game.upgradeCosts[Game.upgrades[i]]
                        Game.upgrades[i] += 1
                        MovementDice.numDice += 1
                        self.initializeMovementDice(screen)
                if i == 1 and self.military >= Game.upgradeCosts[Game.upgrades[i]]:
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.military -= Game.upgradeCosts[Game.upgrades[i]]
                        Game.upgrades[i] += 1
                        self.damage += 0.25
                if i == 2 and self.food >= Game.upgradeCosts[Game.upgrades[i]]:
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.food -= Game.upgradeCosts[Game.upgrades[i]]
                        Game.upgrades[i] += 1
                        self.tokensAtBase += 1


            else:
                self.upgradeButtons[i].isSelected = False



    def rollResourceDice(self):
        self.resourceDice[self.resourceDieSelected].scrambleTimer = ResourceDice.scrambleTimerMax
        self.resourceDice[self.resourceDieSelected].resetCoordinates2()
        self.resourceRoll = random.randint(1, 6)
        self.gameState = "Roll Movement Dice"
        self.resetMovementDice()

    def rollMovementDice(self):
        self.scrambleTimer = ResourceDice.scrambleTimerMax / 2
        self.movementRoll = 0
        for i in range(MovementDice.numDice):
            self.movementDice[i].value = random.randint(0, 1)
            self.movementRoll += self.movementDice[i].value

        self.gameState = "Select Movement"

    def moveToken(self, tileIndex):
        gotoGameState = "Next Turn"
        if self.movementRoll == 0:
            self.nextTurn()

        moveTo = self.movementRoll + tileIndex

        isCrossingLockedTile = -1
        for i in range(tileIndex, moveTo+1):
            if i < GameTile.numGameTiles:
                if self.gameTiles[i].isLocked:
                    isCrossingLockedTile = i


        if self.gameTiles[tileIndex].isOccupied:
            moveTo = self.movementRoll + tileIndex

            # avoid index out of bounds and move to the new tile
            if moveTo < GameTile.numGameTiles:
                if not self.gameTiles[moveTo].isOccupied:
                    # If you landed on a pick-up and you rolled the same color gain those resources
                    if not self.gameTiles[moveTo].pickup == -1:
                        if self.resourceDieSelected == self.gameTiles[moveTo].pickup:
                            # self.gameTiles[moveTo].pickup = -1
                            if self.resourceDieSelected == 0:  # Science
                                self.science += self.resourceRoll
                            if self.resourceDieSelected == 1:  # Military
                                self.military += self.resourceRoll
                            if self.resourceDieSelected == 2:  # Food
                                self.food += self.resourceRoll


                    self.gameState = gotoGameState
                    self.gameTiles[tileIndex].isOccupied = False
                    self.gameTiles[moveTo].isOccupied = True
                    if tileIndex == 0:
                        self.tokensAtBase -= 1
                        if self.tokensAtBase > 0:
                            self.gameTiles[tileIndex].isOccupied = True

                    # Damage the locked Tile
                    if not isCrossingLockedTile == -1:
                        index = 0
                        if isCrossingLockedTile == 37:
                            index = 1
                        if isCrossingLockedTile == 56:
                            index = 2
                        GameTile.lockHealth[index] -= self.resourceRoll * self.damage
                        if GameTile.lockHealth[index] <= 0:
                            self.gameTiles[isCrossingLockedTile].isLocked = False
                        self.gameTiles[moveTo].isOccupied = False


            # User gets their token home
            else:
                if not isCrossingLockedTile == -1:
                    # user hits the last locked tile
                    self.gameState = gotoGameState
                    self.tokensAtBase += 1
                    GameTile.lockHealth[2] -= self.resourceRoll * self.damage
                    if GameTile.lockHealth[2] <= 0:
                        self.gameTiles[isCrossingLockedTile].isLocked = False
                        self.gameState = "Victory!"
                    self.gameTiles[tileIndex].isOccupied = False

                else:
                    self.gameState = "Victory!"
                    self.gameTiles[tileIndex].isOccupied = False

        if self.gameState == "Next Turn":
            self.nextTurn()



    def update(self):
        test = 0

    def nextTurn(self):
        # Generate Pickups Around the track
        for i in range(GameTile.numGameTiles):
            if i == 0 or self.gameTiles[i].isOccupied:
                self.gameTiles[i].pickup = -1
                continue

            if self.turn == 0:
                randomNumber = random.randint(0, GameTile.itemRandomness)
                if randomNumber == 0 or randomNumber == 1 or randomNumber == 2:
                    self.gameTiles[i].pickup = randomNumber
            elif self.gameTiles[i].pickup == -1:
                randomNumber = random.randint(0, GameTile.itemRandomness2 + (i*2))
                if randomNumber == 0 or randomNumber == 1 or randomNumber == 2:
                    self.gameTiles[i].pickup = randomNumber

        for i in range(GameTile.numGameTiles):
            # Hit by a turret and sent home
            if self.gameTiles[i].isOccupied and self.gameTiles[i].isTargeted:
                self.gameTiles[0].isOccupied = True
                self.gameTiles[i].isOccupied = False
                self.tokensAtBase += 1

        self.turn += 1
        self.gameTiles[5].isTargeted = Functions.isTargeted((self.turn - 1) % 2)
        self.gameTiles[7].isTargeted = Functions.isTargeted(self.turn % 2)
        self.gameTiles[8].isTargeted = Functions.isTargeted(self.turn % 2)
        self.gameTiles[23].isTargeted = Functions.isTargeted(self.turn % 2)
        self.gameTiles[28].isTargeted = Functions.isTargeted(self.turn % 2)
        self.gameTiles[10].isTargeted = Functions.isTargeted((self.turn - 1) % 2)
        self.gameTiles[25].isTargeted = Functions.isTargeted((self.turn - 1) % 2)
        self.gameTiles[26].isTargeted = Functions.isTargeted((self.turn - 1) % 2)
        self.gameTiles[13].isTargeted = Functions.isTargeted((self.turn - 2) % 3)
        self.gameTiles[14].isTargeted = Functions.isTargeted((self.turn - 2) % 3)
        self.gameTiles[19].isTargeted = Functions.isTargeted(self.turn % 3)
        self.gameTiles[20].isTargeted = Functions.isTargeted(self.turn % 3)
        self.gameTiles[16].isTargeted = Functions.isTargeted((self.turn-1) % 3)
        self.gameTiles[17].isTargeted = Functions.isTargeted((self.turn-1) % 3)
        self.gameTiles[35].isTargeted = Functions.isTargeted((self.turn-2) % 3)
        self.gameTiles[36].isTargeted = Functions.isTargeted((self.turn-2) % 3)
        self.gameTiles[41].isTargeted = Functions.isTargeted(self.turn % 3)
        self.gameTiles[42].isTargeted = Functions.isTargeted(self.turn % 3)
        self.gameTiles[38].isTargeted = Functions.isTargeted((self.turn-1) % 3)
        self.gameTiles[39].isTargeted = Functions.isTargeted((self.turn-1) % 3)




        self.gameState = "Roll Resource Dice"


    def draw(self, screen):
        tint = 35
        screen.fill((tint, tint, tint))
        if not self.gameState == "Victory!":
            self.drawGame(screen)
            self.drawTurrets(screen)
            self.drawGameTiles(screen)
            self.drawMenuTiles(screen)
            self.drawMovementDice(screen)
            self.drawRollButtons(screen)
            self.drawResourceDice(screen)
            self.drawUpgrades(screen)
            self.drawLockHealth(screen)
            self.drawSkrymir(screen)
        else:
            self.drawVictory(screen)

    def drawGame(self, screen):
        # screen.blit(Game.townImage, (30, 30))
        # screen.blit(Game.townImage, (1160, 385))
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

    def drawTurrets(self, screen):
        for i in range(Game.numTurrets):
            angleOffset = self.turn
            if i == 0:
                angleOffset = self.turn - 1
            j = 0
            modImage = 2
            # Fire Turret is j = 1 and in positions 2 and 3
            if i == 2:
                j = 2
                modImage = 3    # Fire tower rotates 3 times
            if i == 3:
                j = 3
                modImage = 3


            screen.blit(Game.turretImage[j][angleOffset % modImage], Game.turretPos[i])

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
        location = (self.gameTiles[0].x, self.gameTiles[0].y-32)
        text = self.fontLarge.render("{}".format(self.tokensAtBase), True, (0, 0, 0))
        screen.blit(text, location)

        for i in range(GameTile.numGameTiles):
            location = (self.gameTiles[i].x, self.gameTiles[i].y)
            # Draw the Tiles
            if not i == 0:
                screen.blit(self.gameTiles[i].image, location)
            # Draw the Tile Filters
            if self.gameTiles[i].isSelected:
                screen.blit(self.gameTiles[i].filter, location)

            # Draw Tokens on the Tiles
            if self.gameTiles[i].isOccupied:
                screen.blit(Game.tokenImages[self.resourceDieSelected], location)
            # Draw Pickups
            if not self.gameTiles[i].pickup == -1:
                screen.blit(GameTile.pickupImage[self.gameTiles[i].pickup], location)

            # Draw Chained Tile if locked
            if self.gameTiles[i].isLocked:
                screen.blit(Game.chainsImage, location)

        for i in range(GameTile.numGameTiles):
            if self.gameTiles[i].isSelected:
                gotoTile = i + self.movementRoll
                if self.gameState == "Select Movement" and gotoTile < GameTile.numGameTiles and \
                        (self.gameTiles[i].isOccupied or i == 0):
                    gotoLocation = (self.gameTiles[gotoTile].x, self.gameTiles[gotoTile].y)
                    if self.gameTiles[gotoTile].isOccupied and not self.movementRoll == 0:
                        screen.blit(Game.redFilter, gotoLocation)
                    else:
                        screen.blit(Game.greenFilter, gotoLocation)

            if self.gameTiles[i].isTargeted:
                screen.blit(Game.targetImage, (self.gameTiles[i].x, self.gameTiles[i].y))

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
            if self.resourceDice[i].scrambleTimer > 0:
                self.resourceDice[i].scrambleTimer -= 1
                location = (self.resourceDice[i].x2, self.resourceDice[i].y2)
                if self.resourceDice[i].scrambleTimer > 70:
                    index = (self.resourceDice[i].scrambleTimer % 20 % 4) + 2
                    screen.blit(self.resourceDice[i].image[index], location)
                else:
                    screen.blit(self.resourceDice[self.resourceDieSelected].image[6], location)
                    screen.blit(Game.diceNumberImages[self.resourceRoll-1], location)


            screen.blit(self.resourceDice[i].image[0], (self.resourceDice[i].x, self.resourceDice[i].y))
            if self.resourceDice[i].isSelected or self.resourceDieSelected == i:
                screen.blit(self.resourceDice[i].image[1], (self.resourceDice[i].x, self.resourceDice[i].y))

        # RESOURCE DICE TEXT
        text = self.fontLarge.render("Resource Dice", True, (0, 0, 0))
        textRect = text.get_rect()
        screen.blit(text, (textRect.x + 118, textRect.y + 600))

    def drawRollButtons(self, screen):
        for i in range(2):
            screen.blit(GameButton.rollButton, (self.rollButtons[i].x, self.rollButtons[i].y))
            if (i == 0 and self.gameState == "Roll Resource Dice") \
                    or (i == 1 and self.gameState == "Roll Movement Dice"):
                screen.blit(GameButton.rollText, (self.rollButtons[i].x, self.rollButtons[i].y))
                if self.rollButtons[i].isSelected:
                    screen.blit(GameButton.rollSelected, (self.rollButtons[i].x, self.rollButtons[i].y))

        # Draw the resource Die result on the button
        if not self.gameState == "Roll Resource Dice":
            # Draw the Face
            location = (self.rollButtons[0].x + 64, self.rollButtons[0].y)
            screen.blit(self.resourceDice[self.resourceDieSelected].image[6], location)
            # Draw the indents signifying how big of a roll you got
            screen.blit(Game.diceNumberImages[self.resourceRoll-1], location)

        # Draw the roll for Movement Dice on the button
        if not self.gameState == "Roll Movement Dice" and not self.gameState == "Rolling Movement Dice" and \
                not self.gameState == "Roll Resource Dice":
            # Draw the Face
            location = (self.rollButtons[1].x + 64, self.rollButtons[1].y)
            if self.movementRoll-1 >= 0:
                screen.blit(Game.diceNumberImages[self.movementRoll-1], location)
            else:
                screen.blit(Game.lightDieFace, location)

    def drawUpgrades(self, screen):
        text = self.fontLarge.render("Upgrades", True, (0, 0, 0))
        textRect = text.get_rect()
        screen.blit(text, (textRect.x + 1064, textRect.y + 600))

        for i in range(3):
            location = (self.upgradeButtons[i].x, self.upgradeButtons[i].y)
            screen.blit(Game.upgradeBtnImage, location)
            screen.blit(GameTile.pickupImage[i], location)

            colorText = (200, 0, 0)
            if i == 0 and self.science >= Game.upgradeCosts[Game.upgrades[i]]:
                colorText = (0, 200, 0)
            elif i == 1 and self.military >= Game.upgradeCosts[Game.upgrades[i]]:
                colorText = (0, 200, 0)
            elif i == 2 and self.food >= Game.upgradeCosts[Game.upgrades[i]]:
                colorText = (0, 200, 0)


            text = self.fontSmall.render(Game.upgradeTexts[i].format(Game.upgradeCosts[Game.upgrades[i]]), True, colorText)
            textRect = text.get_rect()
            screen.blit(text, (self.upgradeButtons[i].x + 64, self.upgradeButtons[i].y + 22))

            if self.upgradeButtons[i].isSelected:
                if i == 0 and self.science >= Game.upgradeCosts[Game.upgrades[i]]:
                    screen.blit(Game.upgradeGreenImage, location)
                elif i == 1 and self.military >= Game.upgradeCosts[Game.upgrades[i]]:
                    screen.blit(Game.upgradeGreenImage, location)
                elif i == 2 and self.food >= Game.upgradeCosts[Game.upgrades[i]]:
                    screen.blit(Game.upgradeGreenImage, location)
                else:
                    screen.blit(Game.upgradeRedImage, location)

    def drawLockHealth(self, screen):
        for i in range(GameTile.numGameTiles):
            if self.gameTiles[i].isLocked:
                index = 0
                x = 64
                y = 64
                if i == 37:
                    index = 1
                    x = -30
                    y = -15
                elif i == 56:
                    index = 2
                    y = -15

                colorText = (200, 0, 0)
                text = self.fontSmall.render("{}".format(GameTile.lockHealth[index]), True, colorText)
                screen.blit(text, (self.gameTiles[i].x, self.gameTiles[i].y + y))

    def drawSkrymir(self, screen):
        powered = 3
        if GameTile.lockHealth[0] <= 0:
            powered = 2
        screen.blit(Game.skrymirImages[powered], (self.gameTiles[18].x + 64, self.gameTiles[18].y))

        powered = 1
        if GameTile.lockHealth[1] <= 0:
            powered = 0
        screen.blit(Game.skrymirImages[powered], (self.gameTiles))


    def drawVictory(self, screen):
        colorText = (0, 200, 0)
        text = self.fontColossal.render("Victory!", True, colorText)
        screen.blit(text, (50, 100))
        text = self.fontColossal.render("In {} Turns!".format(self.turn), True, colorText)
        screen.blit(text, (50, 400))
        text = self.fontGrand.render("Share how many turns it took you! :D".format(self.turn), True, colorText)
        screen.blit(text, (50, 650))


class MovementDice:
    # These are static and final elements of the object Die
    numDice = 2

    def __init__(self, dieX, dieY, value):
        self.x = dieX
        self.y = dieY
        self.value = value
        self.image = []
        self.image.append(pygame.image.load('sprites/lightDie0.png'))
        self.image.append(pygame.image.load('sprites/lightDie1.png'))

class ResourceDice:
    numDice = 3
    scrambleTimerMax = 120

    def __init__(self, dieX, dieY, value, index):
        self.x = dieX
        self.y = dieY
        self.x2 = 0
        self.y2 = 0
        self.resetCoordinates2()
        self.value = value
        self.index = index
        self.isSelected = False
        self.scrambleTimer = 0
        self.image = []
        if index == 0:
            self.image.append(pygame.image.load('sprites/greenDie.png'))
            self.image.append(pygame.image.load('sprites/greenSelected.png'))
            self.image.append(pygame.image.load('sprites/greenDie.png'))
            self.image.append(pygame.image.load('sprites/greenDie.png'))
            self.image.append(pygame.image.load('sprites/greenDie.png'))
            self.image.append(pygame.image.load('sprites/greenDie.png'))
            self.image.append(pygame.image.load('sprites/greenDieFace.png'))
        if index == 1:
            self.image.append(pygame.image.load('sprites/militaryDie.png'))
            self.image.append(pygame.image.load('sprites/militaryDieSelected.png'))
            self.image.append(pygame.image.load('sprites/militaryDie.png'))
            self.image.append(pygame.image.load('sprites/militaryDie.png'))
            self.image.append(pygame.image.load('sprites/militaryDie.png'))
            self.image.append(pygame.image.load('sprites/militaryDie.png'))
            self.image.append(pygame.image.load('sprites/militaryDieFace.png'))

        if index == 2:
            self.image.append(pygame.image.load('sprites/foodDice.png'))
            self.image.append(pygame.image.load('sprites/foodDiceSelected.png'))
            self.image.append(pygame.image.load('sprites/foodDice.png'))
            self.image.append(pygame.image.load('sprites/foodDice.png'))
            self.image.append(pygame.image.load('sprites/foodDice.png'))
            self.image.append(pygame.image.load('sprites/foodDice.png'))
            self.image.append(pygame.image.load('sprites/foodDieFace.png'))

        self.image[2] = pygame.transform.rotate(self.image[2], 90)
        self.image[2] = pygame.transform.scale(self.image[2], (128, 128))
        self.image[3] = pygame.transform.rotate(self.image[3], 180)
        self.image[3] = pygame.transform.scale(self.image[3], (128, 128))
        self.image[4] = pygame.transform.rotate(self.image[4], 270)
        self.image[4] = pygame.transform.scale(self.image[4], (128, 128))
        self.image[5] = pygame.transform.rotate(self.image[5], 360)
        self.image[5] = pygame.transform.scale(self.image[5], (128, 128))

    def resetCoordinates2(self):
        self.x2 = random.randint(200, 1000)
        self.y2 = random.randint(100, 500)

class MenuTile:
    numMenuTiles = 2

    def __init__(self, screen, x, y, index):
        self.x = x
        self.y = y
        self.index = index
        self.size = int(150 * screen.screenUnitX)
        self.sizeY = int(30 * screen.screenUnitY)
        self.isSelected = False
        self.menuTileText = ["    Exit", "Tutorial", "{}x{}".format(screen.width, screen.height), "Placeholder", "Placeholder", "Placeholder"]
        self.text = self.menuTileText[index]

    def updateResolutionText(self, screen):
        self.menuTileText[1] = "{}x{}".format(screen.width, screen.height)
        self.text = self.menuTileText[self.index]

class GameTile:
    numGameTiles = 57
    pickupImage = [pygame.image.load('sprites/labPickup.png'),
                   pygame.image.load('sprites/MilitaryPickup.png'),
                   pygame.image.load('sprites/foodPickup.png')]
    itemRandomness = 10
    itemRandomness2 = 50
    lockHealth = [7, 15, 20]

    def __init__(self, screen, x, y, index, orientation):
        self.x = x
        self.y = y
        self.index = index
        self.pickup = -1
        self.size = int(50 * screen.screenUnitX)
        self.image = pygame.image.load('sprites/pathHori.png')
        if orientation == 1:
            self.image = pygame.image.load('sprites/pathVert.png')
        self.filter = pygame.image.load('sprites/selectionFilter.png')
        self.selected = False
        self.isOccupied = False
        self.isTargeted = False
        if index == 0:
            self.isOccupied = True
        self.isLocked = False
        if index == 18 or index == 37 or index == 56:
            self.isLocked = True



class GameButton:
    rollButton = pygame.image.load('sprites/RollButton.png')
    rollText = pygame.image.load('sprites/RollText.png')
    rollSelected = pygame.image.load('sprites/rollButtonSelected.png')

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isSelected = False

class Functions:

    @staticmethod
    def flip(boolValue):
        if boolValue:
            return False
        else:
            return True

    @staticmethod
    def isTargeted(i):
        if i == 0:
            return True
        else:
            return False
