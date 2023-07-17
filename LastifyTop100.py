'''
LastifyTop100.py

# Script for creating my Top 100 Recent songs on Spotify
# based on data from Last.FM

@ethanpinter
'''

## make sure to start the Flask server first

# imports
import spotifyAPI as sa
import lastfmAPI as last

def main():   
    ## auth
    auth_code = sa.spotifyAPI.request_user_auth()
    access_token = sa.spotifyAPI.get_access_token(auth_code)
    ## get tracks from last
    tracksArtists = last.lastfmAPI.get_top_tracks_and_artists('ethanpinter')
    ## get the spotify ids for songs
    tracksIDs = sa.spotifyAPI.get_track_id_by_name(tracksArtists, access_token)
    ## create a playlist and add songs to it
    playlist_id = sa.spotifyAPI.create_playlist(access_token)
    for track in tracksIDs:
        sa.spotifyAPI.add_track_to_playlist(track, playlist_id, access_token)
    ## modify playlist cover
    sa.spotifyAPI.set_playlist_cover(playlist_id,access_token)

if __name__ == '__main__':
    main()