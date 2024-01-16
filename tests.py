import pytest
from unittest.mock import AsyncMock
from helpers import get_default_state
from handlers import start, game, end
from config import MESSAGES, CONTINUE_GAME, FINISH_GAME, FREE_SPACE, CROSS, ZERO

class MockChat:
    def __init__(self, id):
        self.id = id

    async def send_message(self, text):
        self.text = text


class MockMessage:
    def __init__(self, text):
        self.text = text

    async def reply_text(self, text):
        self.reply_text = text


class MockMessageCallBackQuery:
    def __init__(self):
        pass

    async def edit_text(self, text):
        self.text = text

    async def edit_reply_markup(self, reply_markup):
        self.reply_markup = reply_markup


class MockBot:
    async def send_message(self, chat_id, text, reply_markup):
        self.text = text


@pytest.mark.asyncio
async def test_start():
    update_mock = AsyncMock()
    context_mock = AsyncMock()
    context_mock.bot = MockBot()
    update_mock.effective_chat = MockChat(0)
    update_mock.callback_query.message = MockMessageCallBackQuery()
    update_mock.message = MockMessage("/start")
    state = await start(update_mock, context_mock)
    assert state == CONTINUE_GAME
    assert update_mock.message.reply_text == MESSAGES.START


@pytest.mark.asyncio
async def test_end():
    update_mock = AsyncMock()
    context_mock = AsyncMock()
    context_mock.bot = MockBot()
    update_mock.effective_chat = MockChat(0)
    update_mock.message = MockMessage("/end")
    state = await end(update_mock, context_mock)
    assert state == get_default_state()


@pytest.mark.asyncio
async def test_win_usr_1():
    """usr wins"""
    update_mock = AsyncMock()
    context_mock = AsyncMock()
    context_mock.bot = AsyncMock()
    update_mock.effective_chat = MockChat(0)
    update_mock.callback_query.message = MockMessageCallBackQuery()
    update_mock.callback_query.data = '22'
    context_mock.user_data = {
        'keyboard_state': [
            [CROSS, CROSS, ZERO],
            [CROSS, CROSS, ZERO],
            [ZERO, ZERO, FREE_SPACE]
        ]
    }
    state = await game(update_mock, context_mock)
    assert state == FINISH_GAME
    assert update_mock.effective_chat.text == MESSAGES.WIN_USER


@pytest.mark.asyncio
async def test_win_usr_2():
    """usr wins"""
    update_mock = AsyncMock()
    context_mock = AsyncMock()
    context_mock.bot = AsyncMock()
    update_mock.effective_chat = MockChat(0)
    update_mock.callback_query.data = '11'
    update_mock.callback_query.message = MockMessageCallBackQuery()
    context_mock.user_data = {
        'keyboard_state': [
            [CROSS, ZERO, ZERO],
            [ZERO, FREE_SPACE, ZERO],
            [ZERO, ZERO, CROSS]
        ]
    }
    state = await game(update_mock, context_mock)
    assert state == FINISH_GAME
    assert update_mock.effective_chat.text == MESSAGES.WIN_USER


@pytest.mark.asyncio
async def test_win_ai_1():
    """ai wins"""
    update_mock = AsyncMock()
    context_mock = AsyncMock()
    context_mock.bot = AsyncMock()
    update_mock.effective_chat = MockChat(0)
    update_mock.callback_query.data = '00'
    update_mock.callback_query.message = MockMessageCallBackQuery()
    context_mock.user_data = {
        'keyboard_state': [
            [FREE_SPACE, ZERO, ZERO],
            [ZERO, CROSS, CROSS],
            [ZERO, CROSS, CROSS]
        ]
    }
    state = await game(update_mock, context_mock)
    assert state == FINISH_GAME
    assert update_mock.effective_chat.text == MESSAGES.WIN_AI

@pytest.mark.asyncio
async def test_win_ai_2():
    """ai wins"""
    update_mock = AsyncMock()
    context_mock = AsyncMock()
    context_mock.bot = AsyncMock()
    update_mock.effective_chat = MockChat(0)
    update_mock.callback_query.data = '02'
    update_mock.callback_query.message = MockMessageCallBackQuery()
    context_mock.user_data = {
        'keyboard_state': [
            [ZERO, ZERO, FREE_SPACE],
            [ZERO, CROSS, CROSS],
            [CROSS, FREE_SPACE, CROSS]
        ]
    }
    state = await game(update_mock, context_mock)
    assert state == FINISH_GAME
    assert update_mock.effective_chat.text == MESSAGES.WIN_AI


@pytest.mark.asyncio
async def test_incorrect_field():
    """incorrect input"""
    update_mock = AsyncMock()
    context_mock = AsyncMock()
    context_mock.bot = AsyncMock()
    update_mock.effective_chat = MockChat(0)
    update_mock.callback_query.data = '00'
    update_mock.callback_query.message = MockMessageCallBackQuery()
    context_mock.user_data = {
        'keyboard_state': [
            [CROSS, CROSS, FREE_SPACE],
            [CROSS, FREE_SPACE, CROSS],
            [FREE_SPACE, CROSS, CROSS]
        ]
    }
    state = await game(update_mock, context_mock)
    assert state == CONTINUE_GAME
    assert update_mock.callback_query.message.text == MESSAGES.WRONG_FIELD


@pytest.mark.asyncio
async def test_draw():
    """draw"""
    update_mock = AsyncMock()
    context_mock = AsyncMock()
    context_mock.bot = AsyncMock()
    update_mock.effective_chat = MockChat(0)
    update_mock.callback_query.data = '11'
    context_mock.user_data = {
        'keyboard_state': [
            [CROSS, ZERO, CROSS],
            [CROSS, FREE_SPACE, ZERO],
            [ZERO, CROSS, ZERO]
        ]
    }
    state = await game(update_mock, context_mock)
    assert state == FINISH_GAME
    assert update_mock.effective_chat.text == MESSAGES.DRAW