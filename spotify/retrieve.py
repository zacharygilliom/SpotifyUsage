import spotipy
import sys
sys.path.append('/home/zach/programming/python/SpotifyUsage/internal')
import creds 
from spotipy.oauth2 import SpotifyClientCredentials
import psycopg

def connect():
    with psycopg.connect("dbname=spotifyusage user=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS songs (
                    name varchar(20))
                """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS title (
                    name varchar(10))
                """)
            conn.commit()


if __name__ == '__main__':
    CLIENT_ID, CLIENT_SECRET = creds.get_client_credentials()
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET))
    
    results = sp.search(q='weezer', limit=20)
    for idx, track in enumerate(results['tracks']['items']):
        print(idx, track['name'])
    
    connect()


