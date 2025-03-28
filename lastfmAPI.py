'''
lastfm.py

Library script for interacting with Last.fm data

@ethanpinter
'''

# imports
import requests
from secret import secret
import json

class lastfmAPI:

    def __init__(self):
        self.LASTFM_API_KEY = secret.get('LASTFM_API_KEY')
        self.LASTFM_SECRET = secret.get('LASTFM_SECRET')
        self.BASE_URL = 'http://ws.audioscrobbler.com/2.0/'

    def get_top_tracks_and_artists(self, user, limit = 100):
        '''
        :param user: the username of the user
        :param limit: Optional, the number of tracks to return
        return: dictonary with track,artist pairing
        '''
        count = 0
        tracks_artists = []
        url = self.BASE_URL + f'?method=user.gettoptracks&user={user}&api_key={self.LASTFM_API_KEY}&format=json&limit={limit}&period=1month'
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