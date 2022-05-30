import spotipy
import sys
sys.path.append('/home/zach/programming/python/SpotifyUsage/internal')
import creds 
from spotipy.oauth2 import SpotifyClientCredentials
import psycopg

class Database:

    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def create_tables(self):
        params = {
                'dbname': self.dbname,
                'user': self.user,
                'password': self.password,
                'host': self.host,
                'port': self.port 
        }
        with psycopg.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS songs (
                        id serial PRIMARY KEY,
                        name varchar(20),
                        band varchar(20))
                    """)
                conn.commit()
                conn.close()

    def query(self):
        params = {
                'dbname': self.dbname,
                'user': self.user,
                'password': self.password,
                'host': self.host,
                'port': self.port 
        }
        with psycopg.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM songs")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
                conn.commit()
                conn.close()

    def insert(self):
        params = {
                'dbname': self.dbname,
                'user': self.user,
                'password': self.password,
                'host': self.host,
                'port': self.port 
        }
        with psycopg.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO songs (name,band) VALUES(%s,%s)",
                    ("Little Dark Age", "MGMT"))
                conn.commit()
                conn.close()
        
if __name__ == '__main__':
    CLIENT_ID, CLIENT_SECRET = creds.get_client_credentials()
    DBNAME, USER, PASSWORD, HOST, PORT = creds.get_db_credentials()    
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET))
    
    results = sp.search(q='weezer', limit=20)
    for idx, track in enumerate(results['tracks']['items']):
        print(idx, track['name'])
   
    db = Database(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    db.create_tables()
    db.insert()
    db.query()


