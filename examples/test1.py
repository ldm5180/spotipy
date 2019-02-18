import sys
import spotipy
import spotipy.util as util
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="File of albums",
                    type=str, required=True)
parser.add_argument("-o", "--output", help="File for URI output",
                    type=str, required=True)
parser.add_argument("-m", "--missing", help="File of missing items",
                    type=str, required=True)
parser.add_argument("-u", "--user", help="Spotify username",
                    type=str, required=True)
args = parser.parse_args()

output = open(args.output, 'w')
missing = open(args.missing, 'w')

scope = 'user-library-read user-library-modify'

token = util.prompt_for_user_token(args.user, scope)

output.write(",".join(['Original Artist', 'Original Album', 'Located Type',
                       'Found Artist', 'Found Album', 'Found Name',
                       'Number of tracks', 'Release date',
                       'uri']) + '\n')
missing.write(",".join(['Original Artist', 'Original Album']) + '\n')

stats = { 'found' : 0, 'missing' : 0 }

def locate(artist, album):
    found = 0
    results = sp.search(q='artist:' + artist + ' album:' + album,
                        type='album')
    for item in results['albums']['items']:
        for a in item['artists']:
            the_artist = "The " + artist
            if a['name'].lower() == artist.lower() or the_artist.lower() == a['name'].lower():
                #print json.dumps(item, sort_keys=True, indent=4, separators=(',', ': '))
                output.write(",".join([artist, album, 'album',
                                a['name'], item['name'], ' ',
                                str(item['total_tracks']), item['release_date'],
                                       item['uri']]) + '\n')
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
                    output.write(",".join([artist, track, 'song name',
                                    a['name'], item['album']['name'], item['name'],
                                    str(item['total_tracks']), item['release_date'],
                                           item['uri']]) + '\n')
                    found = found + 1

    if not found:
        missing.write(",".join([artist, album]) + '\n')
        stats['missing'] += 1
    else:
        print("FOUND: " + artist + ' - ' + album)
        stats['found'] += 1

if token:
    sp = spotipy.Spotify(auth=token)
    with open(args.file, 'r') as album_file:
        for line in album_file:
            tokens = line.split(" - ")
            tokens = map(str.strip, tokens)
            locate(tokens[0], tokens[len(tokens)-1])
    print("\n**********\n" +
          "  FOUND: " + str(stats['found']) + "\n" +
          "  MISSING: " + str(stats['missing']) + "\n" +
          "**********")
else:
    print "Can't get token for", args.user
