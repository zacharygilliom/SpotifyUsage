#!/usr/bin/env python3
import spotipy
import sys
import os
#TODO: Fix the appended path to work inside the docker container. i.e. their is a dir called spotifyusage now
#sys.path.append(f'{os.getcwd()}/internal')
#sys.path.append('/home/spotifyusage/internal/')
sys.path.append('/home/zach/programming/python/SpotifyUsage/internal/')
import creds
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from database import Database

def initialize_backend():
    scope = "user-read-recently-played"
    CLIENT_ID, CLIENT_SECRET = creds.get_client_credentials()
    DBNAME, USER, PASSWORD, HOST, PORT = creds.get_db_credentials()

    # container cach_path = /home/spotifyusage/spotify/backend/.cache

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:8080/callback",scope=scope, open_browser=False, cache_path="/home/zach/programming/python/spotifyusage/spotify/backend/.cache"))
    db = Database(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    return sp, db

def get_recently_played_audio_features(sp_client, db):
    songs_no_features = db.query_songs_no_features()
    if len(songs_no_features) > 0:
        results = sp_client.audio_features(db.query_songs_no_features())
        db.insert_audio_features(results)

def main():
    sp, db = initialize_backend()
    get_recently_played_audio_features(sp, db)

if __name__ == '__main__':
    main()
