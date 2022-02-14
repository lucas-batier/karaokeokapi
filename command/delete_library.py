import json
import sys
import requests

if len(sys.argv) < 3:
    print('ERROR: The host and the authorization token is required')

host = sys.argv[1]
token = sys.argv[2]

# Delete artists
response = requests.get(
    '%s/api/artists/?limit=10000' % host,
    headers={"Authorization": "Token %s" % token},
)

artists = json.loads(response.content)["results"]
for artist in artists:
    response = requests.delete(
        '%s/api/artists/%s/' % (host, artist["id"]),
        headers={"Authorization": "Token %s" % token},
    )

    if response.ok:
        print('SUCCESS: Artist %s (%s) deleted' % (artist["name"], artist["id"]))
    else:
        print('ERROR: Failed to delete artist %s (%s)' % (artist["name"], artist["id"]))


# Delete songs
response = requests.get(
    '%s/api/songs/?limit=10000' % host,
    headers={"Authorization": "Token %s" % token},
)

songs = json.loads(response.content)["results"]
for song in songs:
    response = requests.delete(
        '%s/api/songs/%s/' % (host, song["id"]),
        headers={"Authorization": "Token %s" % token},
    )

    if response.ok:
        print('SUCCESS: Song %s (%s) deleted' % (song["title"], song["id"]))
    else:
        print('ERROR: Failed to delete song %s (%s)' % (song["title"], song["id"]))
