import pygame
import numpy as np

# SETTINGS
SCREEN_X = 1280
SCREEN_Y = 720
CARD_SIZE = 64
ISOTOPES = 10
ELEMS = 5

pygame.init()
SCREEN = (SCREEN_X, SCREEN_Y)
DISPLAY = pygame.display.set_mode(SCREEN)

CARD_GRID = np.zeros((ELEMS, ISOTOPES), np.int8)

# sample card locations
## TODO: replace with csv parse for element information
CARD_GRID[1, 1], CARD_GRID[1, 2], CARD_GRID[1, 3], CARD_GRID[1, 4] = 1, 1, 1, 1
CARD_GRID[2, 2], CARD_GRID[2, 3], CARD_GRID[2, 4], CARD_GRID[2, 5] = 1, 1, 1, 1

while True:
    for event in pygame.event.get():
        # Detect quit
        if event.type == pygame.QUIT:
            pygame.quit()

    # Draw cards
    for i in range(ELEMS):
        for j in range(ISOTOPES):
            if CARD_GRID[i, j]:
                rect = pygame.Rect(j * CARD_SIZE, SCREEN_Y - (i * CARD_SIZE), CARD_SIZE, CARD_SIZE)
                pygame.draw.rect(DISPLAY, (255, 255, 255), rect)

    pygame.display.flip()
