import pygame
import numpy as np

# SETTINGS  -------------------------------------------------------------------
SCREEN_X = 1280
SCREEN_Y = 720
CARD_SIZE = 64

# PYGAME INIT -----------------------------------------------------------------
pygame.init()
SCREEN = (SCREEN_X, SCREEN_Y)
DISPLAY = pygame.display.set_mode(SCREEN)
ELEMS = []


# CLASSES ---------------------------------------------------------------------
class IsotopeCard(object):
    def __init__(self, atomic_num, isotope_num):
        self.atomic_num = atomic_num
        self.isotope_num = isotope_num

    def draw_card(self):
        x_coord = self.isotope_num * CARD_SIZE
        y_coord = SCREEN_Y - ((self.atomic_num + 1) * CARD_SIZE)
        rect = pygame.Rect(x_coord, y_coord, CARD_SIZE, CARD_SIZE)
        pygame.draw.rect(DISPLAY, (255, 255, 255), rect, 0)
        pygame.draw.rect(DISPLAY, (0, 0, 0), rect, 1)


class PlayerToken(object):
    def __init__(self):
        self.atomic_num = 1
        self.isotope_num = 1

    def draw_token(self):
        x_coord = self.isotope_num * CARD_SIZE
        y_coord = SCREEN_Y - ((self.atomic_num + 1) * CARD_SIZE)
        rect = pygame.Rect(x_coord, y_coord, CARD_SIZE, CARD_SIZE)
        pygame.draw.rect(DISPLAY, (255, 63, 63), rect, 5)

    def add_nuetron(self):
        self.isotope_num += 1
        # if IsotopeCard(self.atomic_num, self.isotope_num) not in ELEMS:
        #     self.isotope_num -= 1
        #     self.atomic_num += 1
        self.draw_token()


# FUNCTIONS -------------------------------------------------------------------
# sample card locations
def create_elems():
    ## TODO: csv parse for element information
    for i in range(1, 3):
        for j in range(i, i + 4):
            ELEMS.append(IsotopeCard(atomic_num=i, isotope_num=j))


# PYGAME STATE MACHINE --------------------------------------------------------
create_elems()
player = PlayerToken()
while True:
    for event in pygame.event.get():
        # Detect quit
        if event.type == pygame.QUIT:
            pygame.quit()
        # Detect input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                player.add_nuetron()

    # Draw background
    pygame.draw.rect(DISPLAY, (0, 0, 0), pygame.Rect(0, 0, SCREEN_X, SCREEN_Y))

    # Draw cards
    for elem in ELEMS:
        elem.draw_card()
    player.draw_token()

    pygame.display.flip()
