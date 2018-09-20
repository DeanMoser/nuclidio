import pygame
# import numpy as np

# SETTINGS  -------------------------------------------------------------------
DEBUG = True

SCREEN_X = 1280
SCREEN_Y = 768
CARD_SIZE = 64
# CONTROLS
KEY_RIGHT = pygame.K_RIGHT
KEY_UP = pygame.K_UP
KEY_FORCE_BM_DECAY = pygame.K_m
KEY_FORCE_BP_DECAY = pygame.K_p
KEY_FORCE_A_DECAY = pygame.K_a
# COLORS
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_HIGHLIGHT = (255, 63, 63)


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
        self.stable = True

    def draw_card(self):
        x_coord = self.isotope_num * CARD_SIZE
        y_coord = SCREEN_Y - ((self.atomic_num + 1) * CARD_SIZE)
        rect = pygame.Rect(x_coord, y_coord, CARD_SIZE, CARD_SIZE)
        pygame.draw.rect(DISPLAY, COLOR_WHITE, rect, 0)
        pygame.draw.rect(DISPLAY, COLOR_BLACK, rect, 1)


class PlayerToken(object):
    def __init__(self):
        self.atomic_num = 1
        self.isotope_num = 1

    def draw_token(self):
        x_coord = self.isotope_num * CARD_SIZE
        y_coord = SCREEN_Y - ((self.atomic_num + 1) * CARD_SIZE)
        rect = pygame.Rect(x_coord, y_coord, CARD_SIZE, CARD_SIZE)
        pygame.draw.rect(DISPLAY, COLOR_HIGHLIGHT, rect, 5)

    def add_nuetron(self):
        self.isotope_num += 1
        elem_vals = [(elem.atomic_num, elem.isotope_num) for elem in ELEMS]
        if (self.atomic_num, self.isotope_num) not in elem_vals:
            self.beta_minus_decay()
        self.draw_token()

    def add_proton(self):
        self.atomic_num += 1
        elem_vals = [(elem.atomic_num, elem.isotope_num) for elem in ELEMS]
        if (self.atomic_num, self.isotope_num) not in elem_vals:
            self.beta_plus_decay()
        self.draw_token()

    def beta_minus_decay(self):
        self.isotope_num -= 1
        self.atomic_num += 1

    def beta_plus_decay(self):
        self.atomic_num -= 1
        self.isotope_num += 1

    def alpha_decay(self):
        self.atomic_num -= 2
        self.isotope_num -= 2


# FUNCTIONS -------------------------------------------------------------------
# sample card locations
def create_elems():
    ## TODO: csv parse for element information
    temp_cards = ((1, (1, 2, 3, 4)), (2, (2, 3, 4, 5, 6)), (3, (3, 5, 6, 7, 8)))
    for atomic_num, isotopes in temp_cards:
        for isotope_num in isotopes:
            ELEMS.append(IsotopeCard(atomic_num, isotope_num))


# PYGAME STATE MACHINE --------------------------------------------------------
create_elems()
player = PlayerToken()
while True:
    # Event listener
    for event in pygame.event.get():
        # Detect quit
        if event.type == pygame.QUIT:
            pygame.quit()
        # Detect input
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_RIGHT:
                player.add_nuetron()
            if event.key == KEY_UP:
                player.add_proton()
            # DEBUG ops
            if DEBUG:
                if event.key == KEY_FORCE_BM_DECAY:
                    player.beta_minus_decay()
                if event.key == KEY_FORCE_BP_DECAY:
                    player.beta_plus_decay()
                if event.key == KEY_FORCE_A_DECAY:
                    player.alpha_decay()


    # Draw background
    pygame.draw.rect(DISPLAY, COLOR_BLACK, pygame.Rect(0, 0, SCREEN_X, SCREEN_Y))

    # Draw cards
    for elem in ELEMS:
        elem.draw_card()

    # Draw player
    player.draw_token()

    pygame.display.flip()
