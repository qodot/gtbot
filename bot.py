import os
import json
from html.parser import HTMLParser

import requests
from slacker import Slacker
from websocket import create_connection


class Bot:
    def __init__(self, slacker, translator):
        self._slacker = slacker
        resp = slacker.rtm.start()
        self._socket = create_connection(resp.body['url'])
        self._translator = translator
        bot_user_id = slacker.users.get_user_id('gtbot')
        self._gtbot_id = '<@{}>'.format(bot_user_id)
        self._default_target = 'en'
        print('Successful bot initializing...')

    def run_loop(self):
        print('Start event loop...')
        while True:
            ch, msg, target = self._read()
            if msg == '/lang':
                msg = self._translator.availables()
            elif msg == '/setdefault':
                msg = self._set_default(target)
            else:
                msg = self._translator.translate(msg, target=target)
            self._send(ch, msg)

    def _read(self):
        while True:
            event = json.loads(self._socket.recv())
            if 'bot_id' in event and event.get('username') != 'testuser':
                continue
            ch, msg, target = self._parse(event)
            if not ch or not msg:
                continue
            break

        return ch, msg, target

    def _parse(self, event):
        if event['type'] != 'message' or\
                not event.get('text') or\
                self._gtbot_id not in event.get('text'):
            return None, None, None

        text = event['text'].replace(self._gtbot_id, '').strip()
        target = self._default_target

        if text.startswith('/target'):
            text = text.replace('/target', '').strip().split()
            target, text = text[0], ' '.join(text[1:])
        if text.startswith('/setdefault'):
            text, target = text.split()

        return event['channel'], text, target

    def _send(self, ch, msg):
        self._slacker.chat.post_message(ch, msg, as_user=True)

    def _set_default(self, target):
        self._default_target = target
        self._translator.set_default_target(target)
        return '기본 번역 언어가 {}(으)로 설정 되었습니다 ^ㅇ^'.format(target)


class Translator:
    _base_url = 'https://translation.googleapis.com/language/translate/v2'
    _html_parser = HTMLParser()

    def __init__(self, api_key):
        self._api_key = api_key
        self._default_target = 'en'

    def translate(self, msg, target=None):
        if not target:
            target = self._default_target
        params = {
            'key': self._api_key,
            'target': target,
            'q': msg,
        }
        resp = requests.get(self._base_url, params=params).json()
        translated_msg = resp['data']['translations'][0]['translatedText']
        return self._unescape(translated_msg)

    def availables(self):
        params = {
            'key': self._api_key,
        }
        resp = requests.get(self._base_url + '/languages', params=params).json()
        langs = [lang['language'] for lang in resp['data']['languages']]
        info = '사용 가능한 언어 코드는 다음과 같아요 ^ㅇ^\n\n'
        return info + ', '.join(langs)

    def set_default_target(self, target):
        self._default_target = target

    def _unescape(self, msg):
        return self._html_parser.unescape(msg)


def create_bot():
    slack_token = os.environ.get('GTBOT_SLACK_TOKEN')
    google_token = os.environ.get('GTBOT_GOOGLE_TOKEN')
    return Bot(Slacker(slack_token), Translator(google_token))


def run():
    bot = create_bot()
    bot.run_loop()


if __name__ == '__main__':
    run()
