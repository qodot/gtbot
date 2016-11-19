import pytest
import slacker
import websocket

from bot import Bot
from bot import Translator


@pytest.mark.usefixtures('run_bot')
@pytest.mark.usefixtures('join_test_channel')
class TestBot:
    def test_init(self, bot):
        assert isinstance(bot, Bot)
        assert isinstance(bot._slacker, slacker.Slacker)
        assert isinstance(bot._socket, websocket._core.WebSocket)
        assert isinstance(bot._translator, Translator)
        assert isinstance(bot._gtbot_id, str)
        assert isinstance(bot._default_target, str)

    def test_translate(self, bot, slacker_api, test_channel_id):
        msg = '{} {}'.format(bot._gtbot_id, '안녕')
        slacker_api.chat.post_message(test_channel_id, msg, username='pytest')

    def test_lang(self):
        pass

    def test_target(self):
        pass

    def test_setdefault(self):
        pass
