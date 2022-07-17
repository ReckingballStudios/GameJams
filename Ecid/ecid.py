

"""
Mason Reck
GMTK Game Jam 2022
Project Ecid Llor
A game made within 48 hours for the game maker's toolkit game jam!
"""


import pygame
import util.screen
import util.game
import util.tutorial


# initialize pygame
pygame.init()

# Global Objects and Values
screen = util.screen.Screen(1440, 900, 60)
game = util.game.Game(screen)
# tutorial = util.tuorial.

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        game.handleInput(event, screen)



    # Update this frame of the game
    game.update()

    # Draw this frame of the game
    game.draw(screen.screen)

    # Update Pygame for this frame
    pygame.display.update()
    screen.fpsClock.tick(screen.FPS)















