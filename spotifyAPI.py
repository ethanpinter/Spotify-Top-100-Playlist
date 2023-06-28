'''
spotifyAPI.py

Library script for interacting with Spotify data

@ethanpinter
'''

# imports
import requests
from secret import secret
from urllib.parse import urlencode
import webbrowser
import base64
import json
import linecache
import os

# globals
CLIENT_ID = secret.get('CLIENT_ID')
CLIENT_SECRET = secret.get('CLIENT_SECRET')
REDIRECT_URI = "http://localhost:3000/callback"
TOKEN_URL = "https://accounts.spotify.com/api/token"
AUTH_URL = "https://accounts.spotify.com/authorize?"
BASE_URL = "https://api.spotify.com/v1/"

class spotifyAPI:
    def request_user_auth():
        '''
        # Gets user authentication through Spotify Web login
        :returns: string - authorization code for user
        '''
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        params  = {
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'scope': 'user-read-private'
        }
        url = AUTH_URL + urlencode(params)
        webbrowser.get(chrome_path).open(url)      
        line = linecache.getline('request.data', 7)
        os.remove('response.data')
        os.remove('request.data')
        split = line.split("?")
        auth_code = split[1]
        return auth_code[5:-3]
        
    def get_access_token(auth_code):
        '''
        # Exchange authorization code for access token
        :param auth_code: string - the authorization code for the user provided from request_user_auth()
        :returns: string - access token for user
        '''
        endpoint = TOKEN_URL
        params = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': REDIRECT_URI
        }
        auth_header = base64.urlsafe_b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode('ascii'))
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic %s' % auth_header.decode('ascii')
        }

        resp = requests.post(endpoint, params=params, headers=headers)
        data = json.loads(resp.text)
        return data['access_token']
    
    def get_user_data(access_token):
        '''
        # Retrieves information about the user based on the access token
        :param access_token: string - the access token for the user
        :returns: json dict() object - user information
        '''
        endpoint = BASE_URL + 'me/'
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        resp = requests.get(endpoint, headers=headers)
        data = json.loads(resp.text)
        return data
    
    def get_artist_data(artist_ID, access_token):
        '''
        # Retrieves information about an artist
        :param artist_ID: the UUID of the artist
        :param access_token: string - the access token for the user
        :returns: json dict() object - artist information
        '''
        endpoint = BASE_URL + 'artists/' + artist_ID
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        resp = requests.get(endpoint, headers=headers)
        data = json.loads(resp.text)
        return data

    def create_playlist():
        ## TO-DO
        return None