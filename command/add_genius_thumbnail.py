import json
import os
import sys

from lyricsgenius import Genius

from backend.settings import GENIUS_ACCESS_TOKEN

if len(sys.argv) < 2:
    print('ERROR: A file name is required')

file_name = sys.argv[1]
with open(file_name) as file:
    rows = json.load(file)

genius_api = Genius(GENIUS_ACCESS_TOKEN, timeout=10, retries=3)
failed_rows = []
for row in rows:
    genius_song = genius_api.search_song(title=row["title"], artist=row["artist"])

    if genius_song is None:
        failed_rows.append(row)
        continue

    thumbnail_url = genius_song.song_art_image_thumbnail_url
    thumbnail_url = thumbnail_url.replace(':', '%3A')
    thumbnail_url = thumbnail_url.replace('/', '%2F')
    thumbnail_url = 'https://t2.genius.com/unsafe/300x0/%s' % thumbnail_url
    row["thumbnail_url"] = thumbnail_url

out_file_name = '%s-genius-thumbnail%s' % (os.path.splitext(file_name)[0], os.path.splitext(file_name)[1])
with open(out_file_name, 'w') as out_file:
    json.dump(rows, out_file, ensure_ascii=False)

if len(failed_rows) > 0:
    error_log_file_name = '%s-errors.json' % os.path.splitext(file_name)[0]
    with open(error_log_file_name, 'w') as error_log_file:
        json.dump(failed_rows, error_log_file, ensure_ascii=False)

    print('WARNING: Some thumbnail were not found, check the log file %s to check them' % error_log_file_name)

print('File %s created' % out_file_name)



