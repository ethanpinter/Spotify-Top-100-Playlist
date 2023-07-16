'''
lastfm.py

Library script for interacting with Last.fm data

@ethanpinter
'''

# imports
import requests
from secret import secret
import json

# globals
LASTFM_API_KEY = secret.get('LASTFM_API_KEY')
LASTFM_SECRET = secret.get('LASTFM_SECRET')
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'

class lastfmAPI:
    def get_top_tracks_and_artists(user, limit = 100):
        '''
        return: dictonary with track,artist pairing
        '''
        count = 0
        tracks_artists = []
        url = BASE_URL + f'?method=user.gettoptracks&user={user}&api_key={LASTFM_API_KEY}&format=json&limit={limit}&period=7day'
        resp = requests.get(url)
        resp = json.loads(resp.text)
        while count <= 99:
            temp = []
            filteredTrack = resp['toptracks']['track'][count]['name']
            filteredArtist = resp['toptracks']['track'][count]['artist']['name']
            temp.append(filteredTrack)
            temp.append(filteredArtist)
            tracks_artists.append(temp)
            count += 1
        return tracks_artists