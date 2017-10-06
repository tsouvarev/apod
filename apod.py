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


def send_to_slack(apod):
    text = '%(title)s\n\n%(url)s\n\n%(explanation)s' % apod

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
    send_to_slack(apod)
