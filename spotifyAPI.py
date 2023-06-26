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

# globals
CLIENT_ID = secret.get('CLIENT_ID')
CLIENT_SECRET = secret.get('CLIENT_SECRET')
REDIRECT_URI = "http://localhost:3000"
#AUTH_URL = "https://accounts.spotify.com/api/token"
AUTH_URL = "https://accounts.spotify.com/authorize?"
BASE_URL = "https://api.spotify.com/v1/"

class spotifyAPI:
    '''
    ## this is for client creds only, which cannot acces user information
    def get_access_token():
        
        description: requests an auth code for use in retrieving access token
        returns: (string) access_token: the access token used for all authenticated requests
        
        auth_response = requests.post(AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })

        # convert the response to JSON
        auth_response_data = auth_response.json()

        # save the access token
        access_token = auth_response_data['access_token']
        return access_token
    '''
    def request_user_auth():
        ## TO-DO
        endpoint = AUTH_URL
        params  = {
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': 'http://localhost:3000/callback',
            'scope': 'user-read-private'
        }
        #resp = requests.get(endpoint, params)
        webbrowser.open(AUTH_URL + urlencode(params))

    def get_access_token(auth_code):
        ## TO-DO
        return None
    
    def get_user_data(access_token):
        endpoint = BASE_URL + 'me/'
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        resp = requests.get(endpoint, headers=headers)
        resp_data = resp.json()
        #user_id = resp['display_name']
        return resp_data
    
    def get_artist_data(artist_ID, access_token):
        endpoint = BASE_URL + 'artists/' + artist_ID
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        resp = requests.get(endpoint, headers=headers)
        resp_data = resp.json()
        return resp_data

    def create_playlist():
        ## TO-DO
        return None