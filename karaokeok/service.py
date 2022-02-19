from lyricsgenius import Genius
from youtube_dl import YoutubeDL

from backend.settings import GENIUS_ACCESS_TOKEN


def fetch_youtube_info(url):
    try:
        with YoutubeDL() as youtubedl:
            info = youtubedl.extract_info(url, download=False)

            return info
    except Exception as exception:
        raise exception


def fetch_genius_thumbnail_url(title, artist):
    try:
        genius_api = Genius(GENIUS_ACCESS_TOKEN)
        song = genius_api.search_song(title=title, artist=artist)

        if song is None:
            return None

        thumbnail_url = song.song_art_image_thumbnail_url
        thumbnail_url = thumbnail_url.replace(':', '%3A')
        thumbnail_url = thumbnail_url.replace('/', '%2F')
        thumbnail_url = 'https://t2.genius.com/unsafe/300x0/%s' % thumbnail_url

        return thumbnail_url
    except Exception as exception:
        raise exception
