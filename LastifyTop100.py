'''
LastifyTop100.py

# Script for creating my Top 100 Recent songs on Spotify
# based on data from Last.FM

@ethanpinter
'''

## make sure to start the Flask server first

# imports
from spotifyAPI import spotifyAPI
from lastfmAPI import lastfmAPI

def main():
    # init
    spotify = spotifyAPI()
    last = lastfmAPI()

    # auth
    auth_code = spotify.request_user_auth()
    access_token = spotify.get_access_token(auth_code)

    ## get tracks from last
    tracksArtists = last.get_top_tracks_and_artists('ethanpinter')

    ## get the spotify ids for songs
    tracksIDs = spotify.get_track_id_by_name(tracksArtists, access_token)

    ## create a playlist and add songs to it
    playlist_id = spotify.create_playlist(access_token)
    for track in tracksIDs:
        spotify.add_track_to_playlist(track, playlist_id, access_token)

    ## modify playlist cover
    #spotify.set_playlist_cover(playlist_id,access_token)

if __name__ == '__main__':
    main()