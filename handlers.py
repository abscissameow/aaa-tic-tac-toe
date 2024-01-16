from helpers import (
    ai_move, won, exist_free, generate_keyboard,
    get_default_state, update_keyboard
)
from config import (
    MESSAGES, CONTINUE_GAME, FINISH_GAME, FREE_SPACE, CROSS, ZERO
)
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on /start."""
    context.user_data['keyboard_state'] = get_default_state()
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(MESSAGES.START, reply_markup=reply_markup)
    return CONTINUE_GAME


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Main processing of the game"""
    state = context.user_data['keyboard_state']
    # user latest move
    row, col = map(int, update.callback_query.data)
    # check if user is dumb
    if state[row][col] != FREE_SPACE:
        await update.callback_query.message.edit_text(
            text=MESSAGES.WRONG_FIELD
        )
        return CONTINUE_GAME

    state[row][col] = CROSS
    # check if user wins
    if won(state):
        await update_keyboard(update, state)
        await update.effective_chat.send_message(
            text=MESSAGES.WIN_USER
        )
        return FINISH_GAME
    # check if there exist free space
    if not exist_free(state):
        await update_keyboard(update, state)
        await update.effective_chat.send_message(
            text=MESSAGES.DRAW
        )
        return FINISH_GAME
    # ai moves
    ai_row, ai_col = ai_move(state)
    state[ai_row][ai_col] = ZERO
    # check if ai wins
    if won(state):
        await update_keyboard(update, state)
        await update.effective_chat.send_message(
            text=MESSAGES.WIN_AI
        )
        return FINISH_GAME
    await update_keyboard(update, state)
    return CONTINUE_GAME


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Returns ConversationHandler.END, which tells the
    ConversationHandler that the conversation is over.
    """
    # reset state to default so you can play again with /start
    context.user_data['keyboard_state'] = get_default_state()
    return ConversationHandler.END
