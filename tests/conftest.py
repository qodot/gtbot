import os

import pytest
import slacker

from bot import create_bot


@pytest.fixture(scope='session')
def bot():
    return create_bot()


@pytest.fixture(scope='session')
def run_bot(bot):
    bot.run_loop()


@pytest.fixture(scope='session')
def slacker_api():
    test_token = os.environ.get('GTBOT_SLACK_TOKEN_TEST')
    slacker_api = slacker.Slacker(test_token)
    return slacker_api


@pytest.fixture(scope='session')
def join_test_channel(slacker_api):
    resp = slacker_api.channels.join('test_bot')
    return resp


@pytest.fixture(scope='session')
def test_channel_id(join_test_channel):
    test_channel_id = join_test_channel.body['channel']['id']
    return test_channel_id
