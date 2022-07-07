import sys
import os
#TODO: Fix the path to work inside the docker container.
sys.path.append(f'{os.getcwd()}/spotify/backend')
sys.path.append(f'{os.getcwd()}/internal')
import creds
from database import Database
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from layout import Graph
import psycopg
import pandas as pd

external_stylesheet = [dbc.themes.DARKLY]

app = Dash(__name__, external_stylesheets=external_stylesheet)

def time_series_features(db):
    rows = db.query_time_series()
    df = pd.DataFrame(rows, columns=['Day', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'])
    df = df.set_index('Day', drop=False)
    fig = px.bar(df, x='Day', y=['danceability', 'liveness', 'tempo'], barmode='group')
    return fig

def layout(app, graphs):
    app.layout = html.Div(children=[
            html.H1(children='Hello Dash', style={'textAlign':'center'}
        ),
        html.Div(children='''
            Dash: A web application framework for your data
            ''', style={'textAlign':'center'}),
        dcc.Graph(
            id='example-graph',
            figure = graphs.weekly_time_series()
        ),
        dcc.Graph(
            id='unique-graph',
            figure = graphs.unique_songs_day_tempo()
        )
    ])
    return
#TODO: Add callbacks to update the graphs on intervals 

def main():
    DBNAME, USER, PASSWORD, HOST, PORT = creds.get_db_credentials()
    db = Database(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    graphs = Graph(db)
    layout(app, graphs)
    app.run_server(host="0.0.0.0", debug=True)

if __name__ == '__main__':
    main()
