import time

import pytest
import slacker
import websocket

from bot import Bot
from bot import Translator


@pytest.mark.usefixtures('run_bot_process')
@pytest.mark.usefixtures('run_testuser_msg_loop')
@pytest.mark.usefixtures('join_testchannel')
class TestBot:
    def test_init(self, bot):
        assert isinstance(bot, Bot)
        assert isinstance(bot._slacker, slacker.Slacker)
        assert isinstance(bot._socket, websocket._core.WebSocket)
        assert isinstance(bot._translator, Translator)
        assert isinstance(bot._gtbot_id, str)
        assert isinstance(bot._default_target, str)

    def test_translate(self, bot_id, testuser_slacker, testchannel_id,
                       testuser_msgs):
        msg = '{} {}'.format(bot_id, '안녕')
        testuser_slacker.chat.post_message(testchannel_id, msg,
                                           username='testuser')

        for _ in range(10):
            time.sleep(2)
            if testuser_msgs:
                print('--------------------------------------')
                print(testuser_msgs)
                print('--------------------------------------')
        else:
            raise AssertionError('no expected message')

    def test_lang(self):
        pass

    def test_target(self):
        pass

    def test_setdefault(self):
        pass
