import sys
import spotipy
import spotipy.util as util
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="File of albums",
                    type=str, required=True)
parser.add_argument("-u", "--user", help="Spotify username",
                    type=str, required=True)
args = parser.parse_args()

scope = 'user-library-read user-library-modify'

token = util.prompt_for_user_token(args.user, scope)

print(",".join(['Original Artist', 'Original Album', 'Located Type', 'Found Artist', 'Found Album', 'Found Name', 'Number of tracks', 'Release date', 'uri']))

def locate(artist, album):
    found = 0
    print
    results = sp.search(q='artist:' + artist + ' album:' + album,
                        type='album')
    for item in results['albums']['items']:
        for a in item['artists']:
            the_artist = "The " + artist
            if a['name'].lower() == artist.lower() or the_artist.lower() == a['name'].lower():
                #print json.dumps(item, sort_keys=True, indent=4, separators=(',', ': '))
                print(",".join([artist, album, 'album',
                                a['name'], item['name'], ' ',
                                str(item['total_tracks']), item['release_date'],
                                item['uri']]))
                found = found + 1

    if not found:
        track = album
        results = sp.search(q='artist:' + artist + ' track:' + track,
                            type='track')
        for item in results['tracks']['items']:
            for a in item['album']['artists']:
                the_artist = "The " + artist
                if track.lower() in item['name'].lower() and item['album']['album_type'] == 'album' and (a['name'] == artist or the_artist.lower() == a['name'].lower()):
                    #print json.dumps(item, sort_keys=True, indent=4, separators=(',', ': '))
                    print(",".join([artist, track, 'song name',
                                    a['name'], item['album']['name'], item['name'],
                                    str(item['total_tracks']), item['release_date'],
                                    item['uri']]))
                    found = found + 1

    if not found:
            print(",".join([artist, album, "Unavailable"]))

if token:
    sp = spotipy.Spotify(auth=token)
    with open(args.file, 'r') as album_file:
        for line in album_file:
            tokens = line.split(" - ")
            tokens = map(str.strip, tokens)
            locate(tokens[0], tokens[len(tokens)-1])

else:
    print "Can't get token for", args.user
