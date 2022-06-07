import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
#from database import Database


class Graph:
    '''A Graphing class that will have all of our figure graphs.  Each method returns a valid plotly figure for use in layout'''
    def __init__(self, db):
        self.db = db

    def weekly_time_series(self):
        rows = self.db.query_time_series()
        df = pd.DataFrame(rows, columns=['Day', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'])
        fig = px.bar(df, x='Day', y=['energy', 'loudness', 'speechiness'], barmode='group')
        return fig
