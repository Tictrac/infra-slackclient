#!/usr/bin/env python3

import argparse
import json
import os
import logging
from slack import WebClient
from slack.errors import SlackApiError

DEFAULT_SLACK_ATTACHMENTS_COLOR = '36A64F'
SLACK_MESSAGE_BLOCKS_TEMPLATE = [
    {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': ''
        }
    }
]

SLACK_MESSAGE_ATTACHMENTS_TEMPLATE = [
    {
        'text': '',
        'color': '',
        'attachment_type': 'default',
        'fields': [
            {
                'value': '',
                'short': False
            }
        ],
        'footer': ''
    }
]


def args_validator(arguments):
    if not (arguments.message or arguments.json_payload):
        raise ValueError('At least one of following arguments is required: [--message, --json_payload]')


class WebSlackClient(object):
    # Initializer / Instance Attributes
    def __init__(self, slack_message_type, slack_channel, slack_token=None, slack_attachments_color=None,
                 slack_attachments_header=None, slack_attachments_footer=None, slack_message=None,
                 slack_json_payload=None):
        self.slack_channel = slack_channel
        self.slack_message_type = slack_message_type
        self.slack_token = slack_token
        self.slack_attachments_color = slack_attachments_color
        self.slack_attachments_footer = slack_attachments_footer
        self.slack_attachments_header = slack_attachments_header
        self.slack_message = slack_message
        self.slack_json_payload = slack_json_payload

    def get_slack_client(self):
        slack_token = self.slack_token or os.environ['SLACK_API_TOKEN']
        return WebClient(token=slack_token)

    def send_slack_message_block_type(self):
        client = self.get_slack_client()
        if self.slack_json_payload:
            slack_message = json.loads(self.slack_json_payload)
        else:
            slack_message = SLACK_MESSAGE_BLOCKS_TEMPLATE.copy()
            slack_message[0]['text']['text'] = self.slack_message
        try:
            client.chat_postMessage(
                channel=self.slack_channel,
                text='SlackClient message',
                blocks=slack_message
            )
        except SlackApiError as e:
            log.error('Notification was not send to %s', self.slack_channel, extra={'error': e.response['error']})

    def send_slack_message_attachments_type(self):
        client = self.get_slack_client()
        if self.slack_json_payload:
            slack_message = json.loads(self.slack_json_payload)
        else:
            slack_message = SLACK_MESSAGE_ATTACHMENTS_TEMPLATE.copy()
            slack_message[0]['text'] = self.slack_attachments_header
            slack_message[0]['footer'] = self.slack_attachments_footer
            slack_message[0]['color'] = self.slack_attachments_color
            slack_message[0]['fields'][0]['value'] = self.slack_message
        try:
            client.chat_postMessage(
                channel=self.slack_channel,
                attachments=slack_message
            )
        except SlackApiError as e:
            log.error('Notification was not send to %s', self.slack_channel, extra={'error': e.response['error']})

    def send_slack_message(self):
        if self.slack_message_type == 'blocks':
            self.send_slack_message_block_type()
        else:
            self.send_slack_message_attachments_type()


if __name__ == '__main__':
    # Args Parser
    parser = argparse.ArgumentParser(description='Slack web-client args')
    parser.add_argument('-c', '--channel', required=True, help='Slack channel name')
    parser.add_argument('-s', '--message_type', required=True, help='Slack message type',
                        choices=['blocks', 'attachments'])
    parser.add_argument('-t', '--token', required=False, help='Slack app token (xoxb-your-token)')
    parser.add_argument('-m', '--message', required=False,
                        help='Slack message. Required if \'json_payload\' argument was not specified')
    parser.add_argument('-p', '--json_payload', required=False,
                        help='Slack message in json payload. Required if \'message\' argument was not specified')
    parser.add_argument('--color', required=False, default=DEFAULT_SLACK_ATTACHMENTS_COLOR,
                        help='Slack attachments message color')
    parser.add_argument('--header', required=False, default='', help='Slack attachments message header')
    parser.add_argument('--footer', required=False, default='', help='Slack attachments message footer')
    parser.add_argument('--debug', action='store_true', help='Log level')

    args = parser.parse_args()
    log = logging.getLogger(__name__)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        log.setLevel(logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    args_validator(args)
    slack_client = WebSlackClient(slack_channel=args.channel, slack_message=args.message, slack_token=args.token,
                                  slack_message_type=args.message_type, slack_json_payload=args.json_payload,
                                  slack_attachments_color=args.color, slack_attachments_footer=args.footer,
                                  slack_attachments_header=args.header)

    slack_client.send_slack_message()
