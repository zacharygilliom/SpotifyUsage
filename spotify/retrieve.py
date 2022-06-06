import spotipy
import sys
import os
sys.path.append(f'{os.getcwd()}/internal')
import creds
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from database import Database
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import psycopg

def initialize_app():
    scope = "user-read-recently-played"
    CLIENT_ID, CLIENT_SECRET = creds.get_client_credentials()
    DBNAME, USER, PASSWORD, HOST, PORT = creds.get_db_credentials()

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:8080/callback",scope=scope))

    db = Database(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    return sp, db

def get_recently_played_tracks(sp_client, db):
    results = sp_client.current_user_recently_played(limit=50)
    id_list = []
    for idx, res in enumerate(results['items']):
        id_list.append({'spotify_id':res['track']['id'], 'name': res['track']['name'], 'artist': res['track']['artists'][0]['name'], 'played_at':res['played_at']})
    db.insert_new_songs(id_list)

def get_recently_played_audio_features(sp_client, db):
    songs_no_features = db.query_songs_no_features()
    if len(songs_no_features) > 0:
        results = sp_client.audio_features(db.query_songs_no_features())
        db.insert_audio_features(results)

def get_bar_graph_data(db):
    rows =  db.query()
    df = pd.DataFrame(rows, columns=['played_at','name', 'artist', 'energy'])
    df.set_index('played_at', drop=False)
    df = df.groupby(['artist']).mean()
    df = df.reset_index()
    df.sort_values(by=['energy'], inplace=True, ascending=False)
    return df

def make_figure(df):
    fig = px.bar(df, x="artist", y="energy")
    return fig

def layout(app, df):
    fig = make_figure(df)
    app.layout = html.Div(children=[
        html.H1(children="Hello Dash"),
        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])

def main():
    app = Dash(__name__)
    sp, db = initialize_app()
    get_recently_played_tracks(sp, db)
    get_recently_played_audio_features(sp, db)
    df = get_bar_graph_data(db)
    layout(app, df)
    app.run_server(debug=True)

if __name__ == '__main__':
    main()

#TODO: fix app.layout
#TODO: add error handling to sql executions
