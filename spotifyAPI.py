'''
spotifyAPI.py

Library script for interacting with Spotify data

@ethanpinter
'''

# imports
import requests
from secret import secret

# globals
CLIENT_ID = secret.get('CLIENT_ID')
CLIENT_SECRET = secret.get('CLIENT_SECRET')
REDIRECT_URI = "http://localhost:3000"
AUTH_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com"

class spotifyAPI:
    
    def get_access_token():
        '''
        description: requests an auth code for use in retrieving access token
        returns: (string) access_token: the access token used for all authenticated requests
        '''
        auth_response = requests.post(AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })

        # convert the response to JSON
        auth_response_data = auth_response.json()

        # save the access token
        access_token= auth_response_data['access_token']
        return access_token





