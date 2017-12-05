import re
import requests

from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import date, timedelta

from utils import send_to_slack


ASTRONET_PREVIEW_URL = 'http://www.astronet.ru/db/apod.html'
ASTRONET_PRINT_URL = 'http://www.astronet.ru/db/print/msg/%s/'
YOUTUBE_VIDEO_URL = 'https://youtube.com/watch?v=%s'
VIMEO_VIDEO_URL = 'https://vimeo.com/%s/'


def get_preview_for_date(dt):
    data = {
        'd': dt.strftime('%Y-%m-%d')
    }
    return requests.get(ASTRONET_PREVIEW_URL, params=data).content


def get_details_from_preview(preview):
    bs = BeautifulSoup(preview, "html.parser")

    link_to_details = bs.select('p.title a')[0].attrs['href']
    post_id = re.search('\d+$', link_to_details).group()

    # I use print version because it's cleaner
    details_url = ASTRONET_PRINT_URL % post_id
    return requests.get(details_url).content.decode('cp1251')


def get_image_from_details(details):
    images = details.select('div[align="center"] img')
    if images:
        return images[0].attrs['src']

    videos = details.select('div[align="center"] > center > iframe')
    if videos:
        video_url = videos[0].attrs['src']
        parts = urlparse(video_url).path.split('/')

        if 'vimeo' in video_url:
            vimeo_video_id = parts[-1]
            return VIMEO_VIDEO_URL % vimeo_video_id

        if 'embed' in video_url:
            youtube_video_id = parts[2]
            return YOUTUBE_VIDEO_URL % youtube_video_id

    raise NotImplementedError("Can't parse image")


def parse_details(details):
    bs = BeautifulSoup(details, "html.parser")

    title = bs.select('div font b')[0].get_text()
    image = get_image_from_details(bs)
    content = bs.select('#content')[0]

    for tag in ['table', 'div', 'b', 'p']:
        for node in content.select(tag):
            node.extract()

    text = re.sub('\s+', ' ', content.get_text())

    return {
        'title': title,
        'image': image,
        'explanation': text.strip(),
    }


if __name__ == '__main__':
    # because of lag in translation
    preview = get_preview_for_date(date.today() - timedelta(2))
    details = get_details_from_preview(preview)
    data = parse_details(details)
    send_to_slack(data)
