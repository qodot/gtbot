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
                       bot_reply):
        self._send_msg('안녕', bot_id, testuser_slacker, testchannel_id)

        def assert_func(reply):
            return 'Hello' == reply
        self._wait_reply(bot_reply, assert_func)

    def test_lang(self, bot_id, testuser_slacker, testchannel_id, bot_reply):
        self._send_msg('/lang', bot_id, testuser_slacker, testchannel_id)

        def assert_func(reply):
            langs = bot_reply[0].split('\n\n')[1]
            langs = langs.split(', ')
            return 104 == len(langs)
        self._wait_reply(bot_reply, assert_func)

    def test_target(self, bot_id, testuser_slacker, testchannel_id, bot_reply):
        self._send_msg('/target ko Hi', bot_id, testuser_slacker,
                       testchannel_id)

        def assert_func(reply):
            return '안녕' == reply
        self._wait_reply(bot_reply, assert_func)

    def test_setdefault(self, bot_id, testuser_slacker, testchannel_id,
                        bot_reply):
        self._send_msg('/setdefault ko', bot_id, testuser_slacker,
                       testchannel_id)

        def assert_func(reply):
            return 'ko' in reply
        self._wait_reply(bot_reply, assert_func)

        self._send_msg('Hi', bot_id, testuser_slacker, testchannel_id)

        def assert_func(reply):
            return '안녕' == reply
        self._wait_reply(bot_reply, assert_func)

    def _send_msg(self, msg, bot_id, testuser_slacker, testchannel_id):
        msg = '{} {}'.format(bot_id, msg)
        testuser_slacker.chat.post_message(testchannel_id, msg,
                                           username='testuser')

    def _wait_reply(self, bot_reply, assert_func):
        has_reply = False
        for _ in range(10):
            time.sleep(2)
            if bot_reply:
                has_reply = True
                if assert_func(bot_reply[0]):
                    del bot_reply[:]  # remove all element in bot_reply
                    break  # assert successfully, then break
                else:
                    raise AssertionError('setting default language failed')
        if not has_reply:
            raise AssertionError('no expected message')
