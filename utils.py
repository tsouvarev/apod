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
    emoji = get_emoji()
    url = SLACK_TEST_URL if test else SLACK_WEBHOOK_URL
    image = apod['image']
    text = (
        '%(title)s\n\n'
        '%(explanation)s'
    ) % apod

    requests.post(url, data=get_post_data(image, emoji))
    requests.post(url, data=get_post_data(text, emoji))


def get_post_data(text, emoji=None, username='apod'):
    if emoji is None:
        emoji = get_emoji()

    return {
        'payload': json.dumps({
            'text': text,
            'username': username,
            'icon_emoji': emoji,
        })
    }


def get_emoji():
    return random.choice(EMOJIS)
