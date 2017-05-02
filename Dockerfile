FROM python:3.5
MAINTAINER qodot <waitingforqodot@gmail.com>

WORKDIR /app

ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

CMD python bot.py
