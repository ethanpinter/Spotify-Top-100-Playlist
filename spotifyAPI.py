'''
spotifyAPI.py

Library script for interacting with Spotify data

@ethanpinter
'''

# imports
import requests
#from secret import secret
from urllib.parse import urlencode
import webbrowser
import base64
import json
import linecache
import os
import urllib.parse
import random

class spotifyAPI:

    def __init__(self):

        # grab secrets
        with open('secret.json') as f:
            secret = json.load(f)

        self.SPOTIFY_CLIENT_ID = secret.get('SPOTIFY_CLIENT_ID')
        self.SPOTIFY_CLIENT_SECRET = secret.get('SPOTIFY_CLIENT_SECRET')
        self.REDIRECT_URI = "http://localhost:3000/callback"
        self.TOKEN_URL = "https://accounts.spotify.com/api/token"
        self.AUTH_URL = "https://accounts.spotify.com/authorize?"
        self.BASE_URL = "https://api.spotify.com/v1/"

    def request_user_interactive_auth(self):
        '''
        # Gets user authentication through Spotify Web login
        :returns: string - authorization code for user
        '''
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        params  = {
            'client_id': self.SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': self.REDIRECT_URI,
            'scope': 'user-read-private playlist-modify-public playlist-modify-private user-top-read ugc-image-upload'
        }
        url = self.AUTH_URL + urlencode(params)
        webbrowser.get(chrome_path).open(url)      
        line = linecache.getline('request.data', 7)
        os.remove('response.data')
        os.remove('request.data')
        split = line.split("?")
        auth_code = split[1]
        return auth_code[5:-3]
        
    def get_access_token(self, auth_code):
        '''
        # Exchange authorization code for access token
        :param auth_code: string - the authorization code for the user provided from request_user_auth()
        :returns: string - access token for user
        '''
        endpoint = self.TOKEN_URL
        params = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.REDIRECT_URI
        }
        auth_header = base64.urlsafe_b64encode((self.SPOTIFY_CLIENT_ID + ':' + self.SPOTIFY_CLIENT_SECRET).encode('ascii'))
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic %s' % auth_header.decode('ascii')
        }

        resp = requests.post(endpoint, params=params, headers=headers)
        data = json.loads(resp.text)
        return data['access_token'], data['refresh_token']
    
    def get_refreshed_access_token(self, refresh_token):
        '''
        # Refresh an access token instead of doing user interactive auth
        :param access_token: string - access token provided during user interactive auth
        :return access_token: string - refreshed access token
        '''
        endpoint = self.TOKEN_URL
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
        auth_header = base64.urlsafe_b64encode((self.SPOTIFY_CLIENT_ID + ':' + self.SPOTIFY_CLIENT_SECRET).encode('ascii'))

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic %s' % auth_header.decode('ascii')
        }

        resp = requests.post(endpoint, params=params, headers=headers)
        data = json.loads(resp.text)
        return data['access_token']

    def get_track_id_by_name(self, tracksIDs, access_token):
        '''
        # Get the spotify ID of a track
        :param trackIDs: 2D dictionary containing track name, artist name pairs
        :param access_token: string - the access token for the user
        '''
        results = []
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        count = 0
        while count <= 99:
            trackSafe = urllib.parse.quote(tracksIDs[count][0])
            artistSafe = urllib.parse.quote(tracksIDs[count][1])
            if trackSafe.__contains__("'"):
                trackSafe.replace("'", '%27')
            if artistSafe.__contains__("'"):
                artistSafe.replace("'", '%27')
            endpoint = self.BASE_URL + f'search?q=track%3A{trackSafe}%20artist%3A{artistSafe}&type=track&limit=1&offset=0'
            try:
                resp = requests.get(endpoint, headers=headers)
                respJson = json.loads(resp.text)
                filtered = respJson['tracks']['items'][0]['uri']
                results.append(filtered)
            except:
                print(f'Errored on song: {tracksIDs[count][0]}')
                print(respJson['tracks']['items'])
            count += 1
        return results

    def create_playlist(self, access_token):
        '''
        # Create a new playlist on Spotify
        :param access_token: string - the access token for the user
        '''
        endpoint = self.BASE_URL + 'users/ethan_pinter/playlists'
        data = json.dumps({
            "name": "Top 100 Recent",
            "description": "Top 100 monthly songs listed in order of popularity and auto-updated by a script I wrote (https://github.com/ethanpinter/Spotify-Top-100-Playlist)"
            })
    
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'Content-Type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        }
        resp = requests.post(endpoint, headers = headers, data = data)
        resp = json.loads(resp.text)
        return resp['uri']

    def add_track_to_playlist(self, track_id, playlist_id, access_token):
        '''
        # Add a track to a playlist
        :param track_id: Spotify ID of a track
        :param playlist_id: Playlist ID given when creating playlist
        :param access_token: string - the access token for the user
        '''
        playlist_id_safe = playlist_id[17:]
        endpoint = self.BASE_URL + f'playlists/{playlist_id_safe}/tracks'
        data = json.dumps({
            "uris": [f'{track_id}']
            })
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'Content-Type': 'application/json'
        }
        requests.post(endpoint, headers = headers, data = data)
    
    def set_playlist_cover(self, playlist_id, access_token):
        '''
        # Set the playlist cover image based on a random image collection
        :param playlist_id: the Spotify ID of the playlist
        :param access_token: authorized user access token
        :return: None
        '''
        playlist_id_safe = playlist_id[17:]
        number_of_imgs = len(os.listdir('playlistCovers'))
        imageIndex = random.randint(1, number_of_imgs)
        file = f'playlistCovers/{imageIndex}.jpg'
        with open(file, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data)
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'Content-Type': 'application/json'
        }
        data = encoded
        endpoint = self.BASE_URL + f'playlists/{playlist_id_safe}/images'
        resp = requests.put(endpoint, headers = headers, data=data)
        
