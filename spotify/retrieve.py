import spotipy
import sys
sys.path.append('/home/zach/programming/python/SpotifyUsage/internal')
import creds 
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import psycopg

class Database:

    def __init__(self, dbname, user, password, host, port):
        self.params = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host,
            'port': port 
        }

    def create_tables(self):
        with psycopg.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS songs (
                        id serial PRIMARY KEY,
                        name varchar(20),
                        band varchar(20),
                        spotify_id varchar(22))
                    """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS played (
                        song_id integer references songs(id),
                        played_at timestamp)
                    """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS audio_features (
                        song_id integer references songs(id),
                        danceability real,
                        energy real,
                        key integer,
                        loudness real,
                        mode int,
                        speechiness real,
                        acousticness real,
                        instruementalness real,
                        liveness real,
                        valence real,
                        tempo real)
                    """)
                conn.commit()
                conn.close()

    def query(self, db):
        with psycopg.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {db}")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
                conn.commit()
                conn.close()
                return rows

    def insert(self, song, band):
        with psycopg.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO songs (name,band) VALUES(%s,%s)",
                    (song, band))
                conn.commit()
                conn.close()

    def drop(self, table):
        with psycopg.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"DROP TABLE {table}")
                conn.commit()
                conn.close()

def get_recently_played_track_ids(sp_client):
    results = sp_client.current_user_recently_played(limit=50)
    id_list = []
    for idx, res in enumerate(results['items']):
        id_list.append({'spotify_id':res['track']['id'], 'name': res['track']['name'], 'artist': res['track']['artists'][0]['name'], 'played_at':res['played_at']})
    return id_list


if __name__ == '__main__':
    scope = "user-read-recently-played"
    CLIENT_ID, CLIENT_SECRET = creds.get_client_credentials()
    DBNAME, USER, PASSWORD, HOST, PORT = creds.get_db_credentials()    
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:8080/callback",scope=scope))
    


    id_list = get_recently_played_track_ids(sp)
    print(id_list)

#    for idx, res in enumerate(results['items']):
#        id_list.append(res['track']['id'])
#        print(res['track']['name'])
#        print(res['track']['artists'][0]['name'])
#        print(res['played_at'])
#        print("********************************************")

    #features =  sp.audio_features(id_list)
    #print(features[0])
    #print("*************************************************")
    #print(features[1])
    db = Database(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    db.create_tables()
    #db.insert("Breezeblocks", "Alt-J")
    #songs = db.query("songs")
    #print(songs[0][0])
    #db.drop("songs")

