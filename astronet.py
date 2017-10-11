import re
import requests

from bs4 import BeautifulSoup
from datetime import date, timedelta

from utils import send_to_slack


ASTRONET_PREVIEW_URL = 'http://www.astronet.ru/db/apod.html'
ASTRONET_PRINT_URL = 'http://www.astronet.ru/db/print/msg/%s/'


def get_preview_for_date(dt):
    data = {
        'd': dt.strftime('%Y-%m-%d')
    }
    return requests.get(ASTRONET_PREVIEW_URL, params=data).content


def get_details_from_preview(preview):
    bs = BeautifulSoup(preview)

    link_to_details = bs.select('p.title a')[0].attrs['href']
    post_id = re.search('\d+$', link_to_details).group()

    # I use print version because it's cleaner
    details_url = ASTRONET_PRINT_URL % post_id
    return requests.get(details_url).content


def parse_details(details):
    bs = BeautifulSoup(details)

    full_text = bs.select('#content')[0].get_text()
    start = full_text.index('Пояснение:') + len('Пояснение:')

    text = re.sub('\s+', ' ', full_text[start:])

    return {
        'title': bs.select('div font b')[0].get_text(),
        'image': bs.select('div[align="center"] > a > img')[0].attrs['src'],
        'explanation': text.strip(),
    }


if __name__ == '__main__':
    # because of lag in translation
    preview = get_preview_for_date(date.today() - timedelta(2))
    details = get_details_from_preview(preview)
    data = parse_details(details)
    send_to_slack(data, test=True)
