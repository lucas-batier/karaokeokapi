import json
import sys
import requests

if len(sys.argv) < 4:
    print('ERROR: A file name, the host and the authorization token is required')

file_name = sys.argv[1]
host = sys.argv[2]
token = sys.argv[3]
with open(file_name) as file:
    rows = json.load(file)

for row in rows:
    artist_names = [row["artist"]]

    for artist_name in row["featuring_artist"]:
        artist_names.append(artist_name)

    for artist_name in artist_names:
        response = requests.post(
            '%s/api/artists/' % host,
            json={"name": artist_name},
            headers={"Authorization": "Token %s" % token},
        )

        if not response.ok:
            print('ERROR: Failed to create artist %s: %s' % (artist_name, response.content))
            continue

        artist = response.json()
        print('SUCCESS: Artist %s created in database (id: %s, uuid: %s)' % (artist["name"], artist["id"], artist["uuid"]))

    response = requests.post(
        '%s/api/songs/' % host,
        json=row,
        headers={"Authorization": "Token %s" % token},
    )

    if not response.ok:
        print('ERROR: Failed to create song %s: %s' % (row, response.content))
        continue

    song = response.json()
    print('SUCCESS: Song %s created in database (id: %s, uuid: %s)' % (song["title"], song["id"], song["uuid"]))
