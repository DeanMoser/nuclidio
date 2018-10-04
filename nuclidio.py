import pygame
import numpy as np

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
    """Logical board object for a given element isotope, to be rendered onto the chart of the nuclides,
    and for the player token to navigate between based on instability probabilities.

    Parameters
    ----------
    atomic_num : int
        atomic number of desired element, to be used to determine x-coordinate of card
    isotope_num : int
        isotope number for desired element, to be used to determine y-coordinate of card
    probabilities : float[3]
        3 floats between 0 and 1 that determine how likely beta-minus, beta-plus, and alpha decay are respectively

    """
    def __init__(self, atomic_num, isotope_num, probabilities=None):
        self.atomic_num = atomic_num
        self.isotope_num = isotope_num
        if probabilities is None:
            self.stable = True
            self.bm_prob, self.bp_prob, self.a_prob = 0.0, 0.0, 0.0
        else:
            self.stable = False
            self.bm_prob, self.bp_prob, self.a_prob = probabilities[0], probabilities[1], probabilities[2]

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

    def query_stability(self):
        this_elem = None
        for elem in ELEMS:
            if (elem.atomic_num == self.atomic_num) and (elem.isotope_num == self.isotope_num):
                this_elem = elem
                break
        if not this_elem.stable:
            prob = np.random.random()
            elem_probs = [this_elem.bm_prob, this_elem.bp_prob, this_elem.a_prob]
            iter = 0
            ## TODO: some things with probabilities
            while prob >= elem_probs[iter]:
                iter += 1
            if iter == 0:
                pass
            elif iter == 1:
                pass
            elif iter == 2:
                pass

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


class PlaySession(object):
    def __init__(self):
        self.start()

    def start(self):
        self.create_elems()
        self.player = PlayerToken()

    # sample card locations
    def create_elems(self):
        ## TODO: csv parse for element information
        temp_cards = ((1, (1, 2, 3, 4)), (2, (2, 3, 4, 5, 6)), (3, (3, 5, 6, 7, 8)))
        for atomic_num, isotopes in temp_cards:
            for isotope_num in isotopes:
                ELEMS.append(IsotopeCard(atomic_num, isotope_num))

# FUNCTIONS -------------------------------------------------------------------
def event_listen():
    for event in pygame.event.get():
        # Detect quit
        if event.type == pygame.QUIT:
            pygame.quit()
        # Detect input
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_RIGHT:
                session.player.add_nuetron()
            if event.key == KEY_UP:
                session.player.add_proton()
            # DEBUG ops
            if DEBUG:
                if event.key == KEY_FORCE_BM_DECAY:
                    session.player.beta_minus_decay()
                if event.key == KEY_FORCE_BP_DECAY:
                    session.player.beta_plus_decay()
                if event.key == KEY_FORCE_A_DECAY:
                    session.player.alpha_decay()


# PYGAME STATE MACHINE --------------------------------------------------------
session = PlaySession()
while True:
    # Event listener
    event_listen()

    # Draw background
    pygame.draw.rect(DISPLAY, COLOR_BLACK, pygame.Rect(0, 0, SCREEN_X, SCREEN_Y))

    # Draw cards
    for elem in ELEMS:
        elem.draw_card()

    # Draw player
    session.player.draw_token()

    pygame.display.flip()
