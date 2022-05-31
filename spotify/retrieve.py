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
                        band varchar(20))
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
        
if __name__ == '__main__':
    scope = "user-read-recently-played"
    CLIENT_ID, CLIENT_SECRET = creds.get_client_credentials()
    DBNAME, USER, PASSWORD, HOST, PORT = creds.get_db_credentials()    
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:8080/callback",scope=scope))
   
    results = sp.current_user_recently_played(limit=5)

  
    for idx, res in enumerate(results['items']):
        print(res['track']['name'])
        print(res['track']['artists'][0]['name'])
        print(res['played_at'])
        print("********************************************")

   
    db = Database(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    db.create_tables()
    #db.insert("Breezeblocks", "Alt-J")
    db.query("songs")
    db.drop("songs")

