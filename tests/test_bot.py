from slacker import Chat
from websocket._core import WebSocket

from bot import Translator


class TestBot:
    def test_init(self, bot):
        assert isinstance(bot._chat, Chat)
        assert isinstance(bot._socket, WebSocket)
        assert isinstance(bot._translator, Translator)
        assert isinstance(bot._gtbot_id, str)
        assert isinstance(bot._default_target, str)
