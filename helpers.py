import numpy as np
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from config import FREE_SPACE, CROSS, ZERO, DEFAULT_STATE
from copy import deepcopy


def ai_move(state: list[list[str]]) -> tuple[int]:
    """get random ai move: (row, col)"""
    empty_idxs = np.where(np.array(state) == FREE_SPACE)
    ai_move_idx = np.random.randint(0, len(empty_idxs[0]))
    return empty_idxs[0][ai_move_idx], empty_idxs[1][ai_move_idx]


def won(state: list[list[str]]) -> bool:
    """check if crosses or zeros have won the game"""
    for side in [CROSS, ZERO]:
        mask = np.array(state) == side
        if any(np.sum(mask, axis=1) == 3) or any(np.sum(mask, axis=0) == 3) or \
           (np.trace(mask) == 3) or (np.trace(np.fliplr(mask)) == 3):
            return True
    return False


def exist_free(state: list[list[str]]) -> bool:
    np_state = np.array(state)
    return (np_state == FREE_SPACE).any()


def generate_keyboard(state: list[list[str]]) -> list[list[InlineKeyboardButton]]:
    """generate tic tac toe keyboard 3x3 (telegram buttons)"""
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
            for r in range(3)
        ]
        for c in range(3)
    ]


def get_default_state() -> list[list[str]]:
    """helper function to get default state of the game"""
    # we dont wanna change DEFAULT_STATE (it is list of lists after all) so deepcopy
    return deepcopy(DEFAULT_STATE)


async def update_keyboard(update: Update, state: list[list[str]]) -> None:
    keyboard = generate_keyboard(state)
    await update.callback_query.message.edit_reply_markup(
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
