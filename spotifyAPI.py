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
from selenium import webdriver
import app

# globals
CLIENT_ID = secret.get('CLIENT_ID')
CLIENT_SECRET = secret.get('CLIENT_SECRET')
REDIRECT_URI = "http://localhost:3000/callback"
TOKEN_URL = "https://accounts.spotify.com/api/token"
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
        endpoint = AUTH_URL
        params  = {
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'scope': 'user-read-private'
        }
        webbrowser.open(endpoint + urlencode(params))
        
        auth_code = ""
        return auth_code
    
    ## i believe it will be easier to redirect the auth code recieved here directly to the get_access_token endpoint in app.py
    

    ## super fucked rn -- throws a 400 malformed request // see above comment on redirect
    def get_access_token(auth_code):
        endpoint = TOKEN_URL
        params = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': REDIRECT_URI
        }

        headers = {
        'Authorization': 'Basic ' + CLIENT_SECRET + ":" + CLIENT_ID,
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        resp = requests.post(endpoint, params=params, headers=headers)
        return resp
    
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