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
import urllib.parse

# globals
SPOTIFY_CLIENT_ID = secret.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = secret.get('SPOTIFY_CLIENT_SECRET')
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
            'client_id': SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'scope': 'user-read-private playlist-modify-public playlist-modify-private'
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
        auth_header = base64.urlsafe_b64encode((SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET).encode('ascii'))
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
    
    def get_track_id_by_name(track_name, access_token):
        '''
        take either one or many
        '''
        results = []
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        track_name_safe = urllib.parse.quote(track_name)
        endpoint = BASE_URL + 'search' + f'?q=track%3A{track_name_safe}&type=track&market=US&limit=1&offset=0'
        try:
            resp = requests.get(endpoint, headers=headers)
            resp = json.loads(resp.text)
            filtered = resp['tracks']
            filtered1 = filtered['items']
            filtered2 = filtered1[0]
            results.append(filtered2['uri'])
            #results.append(filtered2['name'])
        except:
            print(f'Errored on song: {track_name}')
            print(f"here's the response: {filtered}")
        return results

    def create_playlist(access_token):
        
        endpoint = BASE_URL + 'users/ethan_pinter/playlists'
        data = json.dumps({
            "name": "Top 100 Recent",
            "description": "Top 100 recent songs listed in order and auto-updated by a script I wrote (https://github.com/ethanpinter/Spotify-Top-100-Playlist)"
            })
    
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'Content-Type': 'application/json'
        }
        resp = requests.post(endpoint, headers = headers, data = data)
        resp = json.loads(resp.text)
        return resp['uri']
    
    def add_track_to_playlist(track_id, playlist_id, access_token):
        playlist_id_safe = playlist_id[17:]
        endpoint = BASE_URL + f'playlists/{playlist_id_safe}/tracks'
        data = json.dumps({
            "uris": [
                f"{track_id}"
                ]
            })
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'Content-Type': 'application/json'
        }
        resp = requests.post(endpoint, headers = headers, data = data)
        return resp
