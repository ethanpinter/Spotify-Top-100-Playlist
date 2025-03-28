'''
LastifyTop100.py

# Script for creating my Top 100 Recent songs on Spotify
# based on data from Last.FM

@ethanpinter
'''

## Make sure to start the Flask server first!

# imports
from spotifyAPI import spotifyAPI
from lastfmAPI import lastfmAPI
import json

def main():
    # set retcode
    retcode = 0
    
    # grab secrets
    try:
        with open('secret.json') as f:
            secret = json.load(f)
    except Exception as ex:
        retcode = 1
        print(f"Caught exception opening secret.json: {ex}")

    # init classes
    spotify = spotifyAPI()
    last = lastfmAPI()

    # user auth flow, check if we have done interactive auth for this user
    # if we have, we can refresh their access token instead of redoing interactive auth through a web browser
    try:
        if secret.get('SPOTIFY_ACCESS_TOKEN', '') != 'none':
            access_token = spotify.get_refreshed_access_token(secret.get('SPOTIFY_REFRESH_TOKEN', ''))
        else:
            auth_code = spotify.request_user_interactive_auth()
            access_token, refresh_token = spotify.get_access_token(auth_code)
            secret['SPOTIFY_ACCESS_TOKEN'] = access_token
            secret['SPOTIFY_REFRESH_TOKEN'] = refresh_token
            with open('secret.json', 'w') as f:
                json.dump(secret, f)
    except Exception as ex:
        retcode = 1
        print(f"Caught exception authenticating with Spotify: {ex}")

    try:
        ## get tracks from lastFM
        tracksArtists = last.get_top_tracks_and_artists('ethanpinter')

        ## get the spotify ids for songs
        tracksIDs = spotify.get_track_id_by_name(tracksArtists, access_token)

        ## create a playlist and add songs to it
        playlist_id = spotify.create_playlist(access_token)
        for track in tracksIDs:
            spotify.add_track_to_playlist(track, playlist_id, access_token)

        ## modify playlist cover
        #spotify.set_playlist_cover(playlist_id,access_token)
    except Exception as ex:
        retcode = 1
        print(f"Caught exception creating playlist: {ex}")

    print(f"End of Script, retcode: {retcode}")
    exit(retcode)

if __name__ == '__main__':
    main()