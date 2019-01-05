import json
import random
import os
import requests
from funcy import retry, silent

from pyshorteners import Shortener, Shorteners
from requests import RequestException


DEFAULT_LIST_OF_SHORTENERS = [
    Shorteners.TINYURL,
    Shorteners.ISGD,
    Shorteners.DAGD,
]


def send_to_slack(webhook_url, data, emojis=None, test=False):
    emoji = get_emoji(emojis)
    url = os.environ['SLACK_TEST_URL'] if test else webhook_url
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


def get_short_url(long_url, shorteners=DEFAULT_LIST_OF_SHORTENERS):
    retryer = retry(5, errors=(RequestException, ), timeout=2)

    for shortener in shorteners:
        shortener = Shortener(shortener)

        short_url = silent(retryer(shortener.short))(long_url)

        if short_url:
            return short_url

    return long_url
