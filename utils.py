import json
import random
import requests


SLACK_WEBHOOK_URL = (
    'https://hooks.slack.com/services/'
    'T0320DXKS/B7F8CG6KZ/y7EuYaFs6IM57ytEmujOh8AK'
)

SLACK_TEST_URL = (
    'https://hooks.slack.com/services/'
    'T0320DXKS/B079DG55K/RJsjlL2K4LVhXOs76QjXpjEx'
)

EMOJIS = [
    ':sunny:',
    ':alien:',
    ':sun_with_face:',
    ':full_moon_with_face:',
    ':star:',
    ':sparkles:',
    ':boom:',
    ':rocket:',
]


def send_to_slack(apod, test=False):
    text = (
        '%(image)s\n\n'
        '%(title)s\n\n'
        '%(explanation)s'
    ) % apod

    data = {
        'payload': json.dumps({
            'text': text,
            'username': 'apod',
            'icon_emoji': random.choice(EMOJIS),
        })
    }

    url = SLACK_TEST_URL if test else SLACK_WEBHOOK_URL

    requests.post(url, data=data)
