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
            'scope': 'user-read-private playlist-modify-public playlist-modify-private user-top-read'
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
    
    def get_spotify_top_tracks(access_token):
        endpoint = BASE_URL + 'me/top/tracks?limit=50'
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        resp = requests.get(endpoint, headers = headers)
        resp = json.loads(resp.text)
        return resp
    
    def get_track_id_by_name(tracksIDs, access_token):
        '''
        take a track, get info from spotify and save as json
        compare each track result - if artist (from track_name array) matches json artist,
        we know the track is the correct track, otherwise skip to next
        track in saved spotify response
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
            endpoint = BASE_URL + f'search?q=track%3A{trackSafe}%20artist%3A{artistSafe}&type=track&limit=1&offset=0'
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
            "uris": [f'{track_id}']
            })
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'Content-Type': 'application/json'
        }
        requests.post(endpoint, headers = headers, data = data)
        
