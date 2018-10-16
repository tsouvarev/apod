from datetime import date

import requests
from bs4 import BeautifulSoup

from utils import send_to_slack, get_short_url

NAT_GEO_WEBHOOK_URL = (
    'https://hooks.slack.com/services/'
    'T0320DXKS/BANV10RS9/dovyFIwnS3JBiRycr5Nru7PF'
)

PHOTO_OF_THE_DAY_URL = (
    'https://www.nationalgeographic.com/'
    'photography/photo-of-the-day/_jcr_content/.gallery.{year}-{month}.json'
)

EMOJIS = [
    ':ocean:', ':monkey:', ':dolphin:', ':tropical_fish:', ':sunflower:',
    ':palm_tree:', ':rabbit:', ':elephant:', ':herb:', ':panda_face:',
    ':beetle:', ':four_leaf_clover:', ':mushroom:', ':snake:', ':snail:',
    ':bouquet:', ':leaves:', ':crocodile:',
]


def get_data_for_month():
    today = date.today()
    url = PHOTO_OF_THE_DAY_URL.format(year=today.year, month=today.month)
    return requests.get(url).json()


def get_data_for_today(month_data):
    today_json = month_data['items'][0]

    # contains HTML thus needs sanitizing
    raw_explanation = today_json['caption']
    explanation = BeautifulSoup(
        raw_explanation, 'html.parser'
    ).get_text().strip()

    # this URL gets REALLY huge
    image_url = today_json['url']

    return {
        'image': get_short_url(image_url),
        'title': today_json['title'],
        'explanation': explanation,
    }


if __name__ == '__main__':
    month_data = get_data_for_month()
    data = get_data_for_today(month_data)
    send_to_slack(NAT_GEO_WEBHOOK_URL, data, emojis=EMOJIS)
