import json
import random
import requests

from pyshorteners import Shortener

SLACK_TEST_URL = (
    'https://hooks.slack.com/services/'
    'T0320DXKS/B079DG55K/RJsjlL2K4LVhXOs76QjXpjEx'
)


def send_to_slack(webhook_url, data, emojis=None, test=False):
    emoji = get_emoji(emojis)
    url = SLACK_TEST_URL if test else webhook_url
    image = data['image']
    text = (
        '%(title)s\n\n'
        '%(explanation)s'
    ) % data

    requests.post(url, data=get_post_data(image, emoji))
    requests.post(url, data=get_post_data(text, emoji))


def get_post_data(text, emoji=None):
    post_data = {
        'text': text,
    }

    if emoji is not None:
        post_data.update(icon_emoji=emoji)

    return {
        'payload': json.dumps(post_data),
    }


def get_emoji(emojis):
    return random.choice(emojis)


def get_short_url(long_url):
    shortener = Shortener('Tinyurl')
    return shortener.short(long_url)
