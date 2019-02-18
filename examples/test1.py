import sys
import spotipy
import spotipy.util as util
import json

scope = 'user-library-read user-library-modify'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope)

print(",".join(['Original Artist', 'Original Album', 'Located Type', 'Found Artist', 'Found Album', 'Found Name', 'uri']))

def locate(artist, album):
    found = 0
    print
    results = sp.search(q='artist:' + artist + ' album:' + album,
                        type='album')
    for item in results['albums']['items']:
        for a in item['artists']:
            the_artist = "The " + artist
            if a['name'] == artist or the_artist == a['name']:
                print(",".join([artist, album, 'album', a['name'], item['name'], item['name'], item['uri']]))
                found = found + 1

    if not found:
        track = album
        results = sp.search(q='artist:' + artist + ' track:' + track,
                            type='track')
        for item in results['tracks']['items']:
            for a in item['album']['artists']:
                the_artist = "The " + artist
                if track.lower() in item['name'].lower() and item['album']['album_type'] == 'album' and (a['name'] == artist or the_artist == a['name']):
                    print(",".join([artist, track, 'song name', a['name'], item['album']['name'], item['name'], item['uri']]))
                    found = found + 1

    if not found:
            print(",".join([artist, album, "Unavailable"]))

if token:
    sp = spotipy.Spotify(auth=token)
    locate("Beatles", "Abbey Road")
    locate("Beatles", "booyah")
    #locate(artist, album)

else:
    print "Can't get token for", username
