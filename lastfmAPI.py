'''
lastfm.py

Library script for interacting with Last.fm data

@ethanpinter
'''

# imports
from hashlib import md5
import requests
from secret import secret
import json
import webbrowser
from urllib.parse import urlencode

# globals
LASTFM_API_KEY = secret.get('LASTFM_API_KEY')
LASTFM_SECRET = secret.get('LASTFM_SECRET')
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'

class lastfmAPI:
    def get_top_tracks(user, limit = 100):
        url = BASE_URL + f'?method=user.gettoptracks&user={user}&api_key={LASTFM_API_KEY}&format=json&limit={limit}&period=7day'
        resp = requests.get(url)
        resp = json.loads(resp.text)
        filtered = resp['toptracks']
        filtered = filtered['track']
        return filtered