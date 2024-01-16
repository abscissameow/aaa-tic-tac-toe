import os
TOKEN = os.getenv('TG_TOKEN')


class MESSAGES:
    START = "your turn!🐷 please, put ✘ to the free place"
    WIN_USER = "you win!! press /start to play again"
    WIN_AI = "ha-ha, i win! press /start to try again"
    DRAW = "no one wins.. press /start to try again"
    WRONG_FIELD = "this field is occupied, find yourself a free one."


CONTINUE_GAME, FINISH_GAME = range(2)
FREE_SPACE = ' '
CROSS = '✘'
ZERO = 'ø'

DEFAULT_STATE = [[FREE_SPACE for _ in range(3)] for _ in range(3)]
