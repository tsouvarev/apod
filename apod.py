import requests
import json

from datetime import datetime


API_KEY = 'DEMO_KEY'
APOD_URL = 'https://api.nasa.gov/planetary/apod'

SLACK_WEBHOOK_URL = (
    'https://hooks.slack.com/services/'
    'T0320DXKS/B7F8CG6KZ/y7EuYaFs6IM57ytEmujOh8AK'
)


def get_apod_for_today():
    data = {
        'api_key': API_KEY,
        'date': datetime.today().strftime('%Y-%m-%d'),
    }

    return requests.get(APOD_URL, params=data).json()


def get_available_image(apod):
    # sometimes API returns 404 for url,
    # have to check availability
    for url in [apod['hdurl'], apod['url']]:
        if requests.head(url).ok:
            return url
    return None


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


if __name__ == '__main__':
    apod = get_apod_for_today()
    available_image = get_available_image(apod)
    if available_image is not None:
        apod['image'] = available_image
        send_to_slack(apod)
