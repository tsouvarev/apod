import json
import requests


SLACK_WEBHOOK_URL = (
    'https://hooks.slack.com/services/'
    'T0320DXKS/B7F8CG6KZ/y7EuYaFs6IM57ytEmujOh8AK'
)


def send_to_slack(apod):
    text = (
        '%(title)s\n\n'
        '%(image)s\n\n'
        '%(explanation)s'
    ) % apod

    data = {
        'payload': json.dumps({
            'text': text,
            'username': 'apod',
            'icon_emoji': ':sunny:'
        })
    }

    requests.post(SLACK_WEBHOOK_URL, data=data)
