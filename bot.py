import sys
import json

from slacker import Slacker
from websocket import create_connection


class ChatHandler:
    def __init__(self, slacker):
        self._chat = slacker.chat
        resp = slacker.rtm.start()
        self._socket = create_connection(resp.body['url'])

    def loop(self):
        while True:
            ch, msg = self.read()
            if ch and msg:
                self.send(ch, msg)

    def read(self):
        parsed = None
        while True:
            event = json.loads(self._socket.recv())
            print('@@@@@@@@@@@@@@@@ {}'.format(event))
            if 'bot_id' in event:
                continue
            parsed = self._parse(event)
            break
        return parsed

    def _parse(self, event):
        if event['type'] == 'message':
            return event['channel'], event['text']
        else:
            return None, None

    def send(self, ch, msg):
        self._chat.post_message(ch, msg, as_user=True)


def run(token):
    slacker = Slacker(token)
    chat_handler = ChatHandler(slacker)

    print('Start event loop...')
    chat_handler.loop()


if __name__ == '__main__':
    token = sys.argv[1]
    run(token)
