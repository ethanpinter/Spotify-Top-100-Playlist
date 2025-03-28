# Spotify-Top-100-Playlist
### Python script to maintain my Top 100 weekly songs on Spotify

- Created to share my latest grooves auto-magically, soon available for other accounts

## Requirements
- Start the Flask server (app.py) in a separate terminal before running the main script (LastifyTop100)
- secret.json containing the following

```json
{
    "SPOTIFY_CLIENT_ID" : "<your-spotify-client-id>",
    "SPOTIFY_CLIENT_SECRET" : "<your-spotify-client-secret>",
    "LASTFM_API_KEY" : "<your-lastfm-api-key>",
    "LASTFM_SECRET" : "<your-lastfm-secret>",
    "SPOTIFY_ACCESS_TOKEN" : "none",
    "SPOTIFY_REFRESH_TOKEN" : "none"
}
