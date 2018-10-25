import pygame
import numpy as np

# SETTINGS  -------------------------------------------------------------------
DEBUG = True

SCREEN_X = 1280
SCREEN_Y = 768
CARD_SIZE = 64
CARD_TEXT_PADDING = 2
# CONTROLS
KEY_RIGHT = pygame.K_RIGHT
KEY_UP = pygame.K_UP
KEY_FORCE_BM_DECAY = pygame.K_m
KEY_FORCE_BP_DECAY = pygame.K_p
KEY_FORCE_A_DECAY = pygame.K_a
KEY_FORCE_RESTART = pygame.K_r
# COLORS
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (200, 200, 200)
COLOR_BLACK = (0, 0, 0)
# COLOR_HIGHLIGHT = (255, 63, 63)
COLOR_TOKEN_SAFE = (0, 180, 255)
COLOR_TOKEN_UNSAFE = (200, 0, 0)
# FONTS
pygame.font.init()
FONT_TITLE = pygame.font.SysFont('DejaVu Sans', 36)
FONT_MENU = pygame.font.SysFont('DejaVu Sans', 24)
FONT_CARD_P = pygame.font.SysFont('DejaVu Sans', 24)
FONT_CARD_S = pygame.font.SysFont('DejaVu Sans', 20)
# FILES
FILE_NUCLIDES = 'nuclides.csv'
FILE_ELEMENTS = 'elements.csv'


# PYGAME INIT -----------------------------------------------------------------
pygame.init()
SCREEN = (SCREEN_X, SCREEN_Y)
DISPLAY = pygame.display.set_mode(SCREEN)


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
    def __init__(self, atomic_num, isotope_num, label='', probabilities=(0.0, 0.0, 0.0)):
        self.atomic_num = atomic_num
        self.isotope_num = isotope_num
        self.label = label
        self.bm_prob, self.bp_prob, self.a_prob = probabilities[0], probabilities[1], probabilities[2]
        self.stable = True if probabilities == (0.0, 0.0, 0.0) else False

    def draw_card(self):
        """Render a rectangular 'board piece' for this logical item, depending on its atomic and isotope ids.

        """
        x_coord = self.isotope_num * CARD_SIZE
        y_coord = SCREEN_Y - ((self.atomic_num + 1) * CARD_SIZE)
        rect = pygame.Rect(x_coord, y_coord, CARD_SIZE, CARD_SIZE)
        fill_color = COLOR_WHITE if self.stable else COLOR_GREY
        p_label = FONT_CARD_P.render(self.label, True, COLOR_BLACK)
        s_label = FONT_CARD_S.render(str(self.isotope_num), True, COLOR_BLACK)
        pygame.draw.rect(DISPLAY, fill_color, rect, 0)
        pygame.draw.rect(DISPLAY, COLOR_BLACK, rect, 1)
        DISPLAY.blit(p_label, (x_coord + CARD_TEXT_PADDING, y_coord + CARD_TEXT_PADDING))
        DISPLAY.blit(s_label, (x_coord + CARD_SIZE - s_label.get_rect().right - CARD_TEXT_PADDING,
                               y_coord + CARD_TEXT_PADDING))


class IsotopeContainer(object):
    def __init__(self):
        self.isotope_cards = []
        self.gen_cards()

    def gen_cards(self):
        with open(FILE_ELEMENTS, 'r') as FILE:
            label_dict = {}
            for line in FILE.readlines():
                # EXPECTED FORMAT:
                #   atomic_number,label
                tokens = line.split(',')
                label_dict[int(tokens[0])] = tokens[1]

        with open(FILE_NUCLIDES, 'r') as FILE:
            for line in FILE.readlines():
                # EXPECTED FORMAT:
                #   atomic_number,isotope,stable,bm_decay,bp_decay,a_decay
                if line[0] is '#':
                    continue
                tokens = line.split(',')
                atomic_num = int(tokens[0])
                isotope_num = int(tokens[1])
                ## TODO: swap proabilities with file vals
                probabilities = (0.0, 0.0, 0.0) if int(tokens[2]) is 1 else (0.25, 0.25, 0.25)
                self.isotope_cards.append(IsotopeCard(atomic_num, isotope_num,
                                                      label_dict[atomic_num].strip(), probabilities))

    def draw_cards(self):
        for card in self.isotope_cards:
            card.draw_card()

    def find(self, atomic_num, isotope_num):
        for card in self.isotope_cards:
            if (card.atomic_num == atomic_num) and (card.isotope_num == isotope_num):
                return card
        return None


class PlayerToken(object):
    """Logical object for player token. The player is able to navigate over several element cards
    via subatomic processes. The player will be bounced back to other elements via radioactive decay.

    """
    def __init__(self):
        self.atomic_num = 1
        self.isotope_num = 1
        self.safe = True

    def draw_token(self):
        """Render colored outline above the current elem card to indicate player location.

        """
        token_color = COLOR_TOKEN_SAFE if self.safe else COLOR_TOKEN_UNSAFE
        x_coord = self.isotope_num * CARD_SIZE
        y_coord = SCREEN_Y - ((self.atomic_num + 1) * CARD_SIZE)
        rect = pygame.Rect(x_coord, y_coord, CARD_SIZE, CARD_SIZE)
        pygame.draw.rect(DISPLAY, token_color, rect, 5)

    def query_stability(self):
        """Query the current element card to determine which kind, if any, of radioactive decay is likely to occur.
        Determine which of these does occur and move the player. To be called after a player move.

        """
        this_elem = ISOTOPE_CONTAINER.find(self.atomic_num, self.isotope_num)
        if this_elem is not None and not this_elem.stable:
            prob = np.random.random()
            prob_windows = [this_elem.bm_prob,
                            this_elem.bm_prob + this_elem.bp_prob,
                            this_elem.bm_prob + this_elem.bp_prob + this_elem.a_prob,
                            1.0]
            iter = 0
            while prob >= prob_windows[iter]:
                iter += 1
            # print(iter)
            # print(prob, prob_windows)
            ## TODO: render intermediate unstable location with unsafe color for small time
            self.safe = False
            pygame.time.wait(500)
            if iter == 0:
                self.beta_minus_decay()
            elif iter == 1:
                self.beta_plus_decay()
            elif iter == 2:
                self.alpha_decay()
            else:
                print('safe')
            self.safe = True

    def add_nuetron(self):
        """Nuetron bombardment results in increasing the isotope, thereby moving 'right' on the board.

        """
        self.isotope_num += 1
        card = ISOTOPE_CONTAINER.find(self.atomic_num, self.isotope_num)
        if card is None:
            self.isotope_num -= 1
        elif not card.stable:
            self.query_stability()

    def add_proton(self):
        """Proton bombardment results in increasing the atomic number, thereby moving 'up' on the board.

        """
        self.atomic_num += 1
        card = ISOTOPE_CONTAINER.find(self.atomic_num, self.isotope_num)
        if card is None:
            self.atomic_num -= 1
        elif not card.stable:
            self.query_stability()

    def beta_minus_decay(self):
        """Beta minus decay is the emission of an electron, thereby converting one nuetron
        to a proton, and moving the player 'up and left' on the board.

        """
        self.isotope_num -= 1
        self.atomic_num += 1

    def beta_plus_decay(self):
        """Beta plus decay is the emission of a positron, thereby converting one proton
        to a nuetron, and moving the player 'down and right' on the board.

        """
        self.atomic_num -= 1
        self.isotope_num += 1

    def alpha_decay(self):
        """Alpha decay is the emission of a Helium nucleus, thereby and moving the player
        'down 2x and left 2x' on the board.

        """
        self.atomic_num -= 2
        self.isotope_num -= 2


class PlaySession(object):
    def __init__(self):
        self.start()

    # def menu(self):
    #     title = FONT_TITLE.render(u'NUCLID.IO', True, COLOR_WHITE)
    #     DISPLAY.blit(title, (0, 0))

    def start(self):
        # self.create_elems()
        self.player = PlayerToken()

    def draw_session(self):
        # Draw background
        pygame.draw.rect(DISPLAY, COLOR_BLACK, pygame.Rect(0, 0, SCREEN_X, SCREEN_Y))

        # Draw cards
        ISOTOPE_CONTAINER.draw_cards()

        # Draw player
        self.player.draw_token()

        pygame.display.flip()


# FUNCTIONS -------------------------------------------------------------------
def event_listen():
    for event in pygame.event.get():
        # Detect quit
        if event.type == pygame.QUIT:
            pygame.quit()
        # Detect input
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_RIGHT:
                SESSION.player.add_nuetron()
            if event.key == KEY_UP:
                SESSION.player.add_proton()
            # DEBUG ops
            if DEBUG:
                if event.key == KEY_FORCE_BM_DECAY:
                    SESSION.player.beta_minus_decay()
                if event.key == KEY_FORCE_BP_DECAY:
                    SESSION.player.beta_plus_decay()
                if event.key == KEY_FORCE_A_DECAY:
                    SESSION.player.alpha_decay()
                if event.key == KEY_FORCE_RESTART:
                    SESSION.player.atomic_num = 1
                    SESSION.player.isotope_num = 1


# PYGAME STATE MACHINE --------------------------------------------------------
ISOTOPE_CONTAINER = IsotopeContainer()
SESSION = PlaySession()
while True:
    # Event listener
    event_listen()

    # Draw
    SESSION.draw_session()
