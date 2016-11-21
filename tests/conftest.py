import os
import subprocess
import time
import json
from _thread import start_new_thread

import pytest
import slacker
from websocket import create_connection

from bot import create_bot


@pytest.fixture(scope='session')
def bot():
    bot = create_bot()
    return bot


@pytest.fixture(scope='session')
def bot_id(bot):
    return bot._gtbot_id


@pytest.fixture(scope='session')
def testuser_slacker():
    test_token = os.environ.get('GTBOT_SLACK_TOKEN_TEST')
    testuser_slacker = slacker.Slacker(test_token)
    return testuser_slacker


@pytest.fixture(scope='session')
def websocket(testuser_slacker):
    resp = testuser_slacker.rtm.start()
    socket = create_connection(resp.body['url'])
    return socket


@pytest.fixture(scope='session')
def run_bot_process(bot_id, testuser_slacker):
    sp = subprocess.Popen('python bot.py', shell=True)
    # waiting for bot online
    for _ in range(10):
        time.sleep(2)
        bot_id = bot_id[2:-1]
        resp = testuser_slacker.users.get_presence(bot_id)
        if resp.body['presence'] == testuser_slacker.presence.ACTIVE:
            break
    else:
        raise AssertionError('bot is offline')
    yield sp
    sp.terminate()


@pytest.fixture(scope='session')
def run_testuser_msg_loop(websocket, bot_reply, bot_id):
    def loop(websocket):
        while True:
            while True:
                event = json.loads(websocket.recv())
                # some event has no user
                user_id = '<@{}>'.format(event.get('user'))
                if event['type'] == 'message' and user_id == bot_id:
                    bot_reply.append(event['text'])
    start_new_thread(loop, (websocket,))


@pytest.fixture(scope='session')
def bot_reply():
    reply = []
    return reply


@pytest.fixture(scope='session')
def join_testchannel(testuser_slacker):
    resp = testuser_slacker.channels.join('test_bot')
    return resp


@pytest.fixture(scope='session')
def testchannel_id(join_testchannel):
    testchannel_id = join_testchannel.body['channel']['id']
    return testchannel_id
