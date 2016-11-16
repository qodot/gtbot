import sys
import json

import requests
from slacker import Slacker
from websocket import create_connection


class ChatHandler:
    def __init__(self, slacker, translator):
        self._chat = slacker.chat
        resp = slacker.rtm.start()
        self._socket = create_connection(resp.body['url'])
        self._translator = translator

    def loop(self):
        while True:
            ch, msg = self._read()
            if not ch or not msg:
                continue
            translated_msg = self._translator.translate(msg)
            self._send(ch, translated_msg)

    def _read(self):
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

    def _send(self, ch, msg):
        self._chat.post_message(ch, msg, as_user=True)


class Translator:
    base_url = 'https://translation.googleapis.com/language/translate/v2'

    def __init__(self, api_key):
        self.api_key = api_key

    def translate(self, msg, target='en'):
        params = {
            'key': self.api_key,
            'target': target,
            'q': msg,
        }
        resp = requests.get(self.base_url, params=params).json()
        return resp['data']['translations'][0]['translatedText']

    def availables(self):
        params = {
            'key': self.api_key,
        }
        resp = requests.get(self.base_url + '/languages', params=params).json()
        langs = [lang['language'] for lang in resp['data']['languages']]
        return ', '.join(langs)


def run(slack_token, google_token):
    slacker = Slacker(slack_token)
    chat_handler = ChatHandler(slacker, Translator(google_token))

    print('Start event loop...')
    chat_handler.loop()


if __name__ == '__main__':
    slack_token = sys.argv[1]
    google_token = sys.argv[2]
    run(slack_token, google_token)
