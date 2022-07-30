


"""
Mason Reck
Critical Room Control
7/22/2022

This script is made with the intention of converting monochrome images to hex
form for the XMega384c3-Xplained OLED display


"""

import pygame
import screen
import game


width = 1920
height = 1080

pygame.init()

screen = screen.Screen(width, height, 60)
game = game.Game(screen.sux, screen.suy)


# Tool Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        game.handleMouse(event, screen)
        game.handleKeyboard(event, screen)



    game.update()
    game.draw(screen.pyScreen)


    pygame.display.update()
    screen.fpsClock.tick(screen.fps)




