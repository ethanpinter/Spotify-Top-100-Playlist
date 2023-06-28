'''
lastfm.py

Library script for interacting with Last.fm data

@ethanpinter
'''

# imports
import requests
from secret import secret
import json
import webbrowser

# globals
LASTFM_API_KEY = secret.get('LASTFM_API_KEY')
LASTFM_SECRET = secret.get('LASTFM_SECRET')
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'

class lastfmAPI:
    def get_token():
        '''
        # Retrieve an access token for Last.fm
        :return: string - access token
        '''
        endpoint = BASE_URL + f'?method=auth.gettoken&api_key={LASTFM_API_KEY}&format=json'
        resp = requests.post(endpoint)
        data = json.loads(resp.text)
        return data['token']
    
    def auth_token(token):
        '''
        # Authenticate an access token using the browser
        :return: None
        '''
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        url = f'http://www.last.fm/api/auth/?api_key={LASTFM_API_KEY}&token={token}'
        webbrowser.get(chrome_path).open(url)

    ## needs fixed
    def get_session(token):
        '''
        # Retrieve an session token for Last.fm
        :return: string - session token
        '''
        params = {
            'api-key': LASTFM_API_KEY,
            'method': 'auth.getsession',
            'format': 'json'
        }
        resp = requests.get(BASE_URL, params=params)
        #data = json.loads(resp.text)
        return resp