# gtbot

[![Build Status](https://travis-ci.org/qodot/gtbot.svg?branch=master)](https://travis-ci.org/qodot/gtbot)

구글 번역 API를 이용한 슬랙 번역 봇입니다.

## Features

- 슬랙 채널에 봇을 초대해 놓고 `@gtbot`으로 말을 걸면 번역을 할 수 있습니다. 최초 기본 번역 언어는 영어(en)입니다.

![overview](/readmeimages/overview.png)

- 구글 번역 API에서 지원하는 언어 코드를 알 수 있습니다.

![lang](/readmeimages/lang.png)

- 특정한 언어를 지정해서 번역할 수 있습니다. (일본어를 몰라서 제대로 번역이 된건지 모르겠습니다...)

![target](/readmeimages/target.png)

- 매번 언어를 지정할 필요 없이, 특정한 언어를 기본 번역 언어로 설정할 수 있습니다.

![setdefault](/readmeimages/setdefault.png)

## Install

### Clone repository

```sh
git clone https://github.com/qodot/gtbot.git
```

### Install dependencies

이 애플리케이션이 동작하는데 필요한 파이썬 라이브러리들을 설치합니다. (이 때, 파이썬 가상환경을 만들어서 설치하는 것을 추천합니다.)

```sh
pip install -r requirements.txt
```

### Get a slack bot API token

1. [슬랙 앱 빌드 페이지](https://showerbugs.slack.com/apps/build)로 들어가셔서 `Something just for my team(Make a Custom Integration)`을 선택합니다.
2. `Bots`를 선택합니다.
3. 봇의 이름을 입력해야 하는데, **이 때 반드시 이름을 `gtbot`으로 설정합니다.**
4. API 토큰이 보이는데 이것을 환경변수에 다음과 같이 추가합니다.

```sh
export GTBOT_SLACK_TOKEN=<your_token>
```

### Get a google translation API token

[구글 번역 API 문서](https://cloud.google.com/translate/docs/getting-started)를 참고해서 API 토큰을 얻고, 환경변수에 다음과 같이 추가합니다.

```sh
export GTBOT_GOOGLE_TOKEN=<your_token>
```

### Get a slack test user API token

__* 이 항목은 이 애플리케이션의 테스트를 실행하기 위해 필요한 항목으로, 테스트를 실행하지 않을 분은 건너뛰어도 괜찮습니다.__

[슬랙 테스트 토큰 발급 페이지](https://api.slack.com/docs/oauth-test-tokens)에 가서 봇 Integration을 했던 팀의 테스트 토큰을 발급 받고, 환경변수에 다음과 같이 추가합니다.

```sh
export GTBOT_SLACK_TOKEN_TEST=<your_token>
```

## Run

다음과 같이 실행합니다.

```sh
python bot.py
```

테스트 실행은 다음과 같습니다.

```sh
pytest
```

테스트 커버리지 측정을 테스트와 함께 하려면 다음과 같이 실행합니다.

```sh
pytest --cov
```

## Dependencies

### Application

- python 3.5
- slacker [https://github.com/os/slacker](https://github.com/os/slacker)
- requests [http://docs.python-requests.org/en/master](http://docs.python-requests.org/en/master)
- websocket-client [https://github.com/liris/websocket-client](https://github.com/liris/websocket-client)

### test

- pytest [http://doc.pytest.org/en/latest](http://doc.pytest.org/en/latest)
- coverage [https://coverage.readthedocs.io/en/coverage-4.2](https://coverage.readthedocs.io/en/coverage-4.2)
- pytest-cov [http://pytest-cov.readthedocs.io/en/latest](http://pytest-cov.readthedocs.io/en/latest/)
