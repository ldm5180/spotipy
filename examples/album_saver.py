import sys
import spotipy
import spotipy.util as util
import argparse
import csv
import pprint

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="CSV File of albums",
                    type=str, required=True)
parser.add_argument("-u", "--user", help="Spotify username",
                    type=str, required=True)
args = parser.parse_args()

scope = 'user-library-read user-library-modify'

token = util.prompt_for_user_token(args.user, scope)

def save_albums(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for album in reader:
            print("SAVING: " + album['Found Artist'] + ' - ' + album['Found Album'])
            results = sp.current_user_saved_albums_add(albums=[album['uri']])

if token:
    sp = spotipy.Spotify(auth=token)
    save_albums(args.file)
else:
    print "Can't get token for", args.user
