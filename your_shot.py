import requests

from national_geographic import NAT_GEO_WEBHOOK_URL, EMOJIS
from utils import send_to_slack, get_short_url

HASH_TAG = 'mountains'
ORDERING = 'popular'

PHOTO_BASE_URL = 'http://yourshot.nationalgeographic.com'

HASHTAG_URL = (
    'http://yourshot.nationalgeographic.com/rpc/search/photos/'
    '?encode=grid&hashtag={tag}&order_by={ordering}&page_size=1'
).format(tag=HASH_TAG, ordering=ORDERING)


def get_latest_photos():
    return requests.get(HASHTAG_URL).json()


def get_data(latest_photos):
    photo = latest_photos['photos'][0]

    # this URL gets REALLY huge
    image_url = PHOTO_BASE_URL + photo['photo_sizes']['1080x0']

    return {
        'image': get_short_url(image_url),
        'title': photo['title'],
        'explanation': photo['caption'],
    }


if __name__ == '__main__':
    latest_photos = get_latest_photos()
    data = get_data(latest_photos)
    send_to_slack(NAT_GEO_WEBHOOK_URL, data, emojis=EMOJIS, test=True)
