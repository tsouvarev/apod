import requests

from datetime import datetime

from utils import send_to_slack


API_KEY = 'DEMO_KEY'
APOD_URL = 'https://api.nasa.gov/planetary/apod'


def get_apod_for_today():
    data = {
        'api_key': API_KEY,
        'date': datetime.today().strftime('%Y-%m-%d'),
    }

    return requests.get(APOD_URL, params=data).json()


def get_available_image(apod):
    # sometimes API returns 404 for url,
    # have to check availability
    for url in [apod['url'], apod['hdurl']]:
        if requests.head(url).ok:
            return url
    return None


if __name__ == '__main__':
    apod = get_apod_for_today()
    available_image = get_available_image(apod)
    if available_image is not None:
        apod['image'] = available_image
        send_to_slack(apod)
