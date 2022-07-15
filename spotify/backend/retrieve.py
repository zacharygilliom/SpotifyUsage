#!/usr/bin/env python3
import spotipy
import sys
import os
#sys.path.append(f'{os.getcwd()}/internal')
#sys.path.append('/home/spotifyusage/internal/')
sys.path.append('/home/zach/programming/python/SpotifyUsage/internal')
import creds
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from database import Database

def initialize_backend():
    scope = "user-read-recently-played"
    CLIENT_ID, CLIENT_SECRET = creds.get_client_credentials()
    DBNAME, USER, PASSWORD, HOST, PORT = creds.get_db_credentials()

    #container cache_path for spotify token = /home/spotifyusage/spotify/backend/.cache

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:8080/callback",scope=scope, open_browser=False, cache_path="/home/zach/programming/python/SpotifyUsage/spotify/backend/.cache"))
    db = Database(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    return sp, db

def get_recently_played_tracks(sp_client, db):
    results = sp_client.current_user_recently_played(limit=50)
    id_list = []
    for idx, res in enumerate(results['items']):
        id_list.append({'spotify_id':res['track']['id'], 'name': res['track']['name'], 'artist': res['track']['artists'][0]['name'], 'played_at':res['played_at']})
    db.insert_new_songs(id_list)

def main():
    sp, db = initialize_backend()
    get_recently_played_tracks(sp, db)

if __name__ == '__main__':
    main()
