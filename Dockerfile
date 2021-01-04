FROM python:3.7-alpine

MAINTAINER developer@tictrac.com

WORKDIR /app
ADD . /app/

RUN apk update
RUN apk upgrade
RUN apk add bash
RUN apk add build-base

RUN pip install -r requirements.txt

RUN chmod +x slack-client.py
RUN ln -s /app/slack-client.py /usr/local/bin/slack-cli

ENTRYPOINT ["/usr/local/bin/slack-cli"]
