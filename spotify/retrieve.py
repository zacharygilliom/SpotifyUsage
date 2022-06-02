import spotipy
import sys
import os
sys.path.append(f'{os.getcwd()}/internal')
import creds
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from database import Database
import psycopg

def get_recently_played_tracks(sp_client, db):
    results = sp_client.current_user_recently_played(limit=50)
    id_list = []
    for idx, res in enumerate(results['items']):
        id_list.append({'spotify_id':res['track']['id'], 'name': res['track']['name'], 'artist': res['track']['artists'][0]['name'], 'played_at':res['played_at']})
    db.insert_new_songs(id_list)

def get_recently_played_audio_features(sp_client, db):
    no_features_list = db.query_songs_no_features()
    results = sp_client.audio_features(no_features_list)
    return null

if __name__ == '__main__':

    scope = "user-read-recently-played"
    CLIENT_ID, CLIENT_SECRET = creds.get_client_credentials()
    DBNAME, USER, PASSWORD, HOST, PORT = creds.get_db_credentials()    
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:8080/callback",scope=scope))
    
    #features =  sp.audio_features(id_list)
    #print(features[0])
    #print("*************************************************")
    #print(features[1])
    db = Database(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    get_recently_played_tracks(sp, db)
    get_recently_played_audio_features(sp, db)
    #db.insert_songs(id_list)
    #db.insert("Breezeblocks", "Alt-J")
    #db.drop("songs")
