import pytest

from bot import create_bot


@pytest.fixture(scope='session')
def bot():
    yield create_bot()
