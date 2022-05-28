import spotipy
import sys
sys.path.append('../internal')
import creds 
from spotipy.oauth2 import SpotifyClientCredentials

if __name__ == '__main__':
    CLIENT_ID, CLIENT_SECRET = creds.get_client_credentials()
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET))
    
    results = sp.search(q='weezer', limit=20)
    for idx, track in enumerate(results['tracks']['items']):
        print(idx, track['name'])
    
