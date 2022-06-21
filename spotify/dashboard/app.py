import sys
import os
#TODO: Fix the path to work inside the docker container.
sys.path.append(f'{os.getcwd()}/spotify/backend')
sys.path.append(f'{os.getcwd()}/internal')
import creds
from database import Database
from dash import Dash, html, dcc
from layout import Graph
import psycopg
import pandas as pd

app = Dash(__name__)

def time_series_features(db):
    rows = db.query_time_series()
    df = pd.DataFrame(rows, columns=['Day', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'])
    df = df.set_index('Day', drop=False)
    fig = px.bar(df, x='Day', y=['danceability', 'liveness', 'tempo'], barmode='group')
    return fig

def layout(app, graphs):
    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for your data
        '''),
        dcc.Graph(
            id='example-graph',
            figure = graphs.weekly_time_series()
        ),
        dcc.Graph(
            id='unique-graph',
            figure = graphs.unique_songs_day()
        )
    ])
    return
#TODO: Add callbacks to update the graphs on intervals 
if __name__ == '__main__':
    DBNAME, USER, PASSWORD, HOST, PORT = creds.get_db_credentials()
    db = Database(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    graphs = Graph(db)
    layout(app, graphs)
    app.run_server(host="0.0.0.0", debug=True)
