import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

class Graph:
    '''A Graphing class that will have all of our figure graphs.  Each method returns a valid plotly figure for use in layout'''
    def __init__(self, db):
        self.db = db

    def weekly_time_series(self):
        rows = self.db.query_time_series()
        df = pd.DataFrame(rows, columns=['Day', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'])
        fig = px.bar(df, x='Day', y=['energy', 'liveness', 'speechiness'], barmode='group', template='plotly_dark')
        for i , t in enumerate(['energy', 'liveness', 'speechiness']):
            fig.data[i].text=t
        fig.update_traces(textposition='outside')
        return fig

    def unique_songs_day_tempo(self):
        rows = self.db.query_unique_songs_by_day()
        df = pd.DataFrame(rows, columns=['Day', 'tempo_range', 'count'])
        df.columns = df.columns.str.strip()
        for idx, row in df.iterrows():
            if row['tempo_range'] == None:
                df.at[idx, 'tempo_range'] = 0
            new_val = row['Day'].strip()
            df.at[idx, 'Day'] = new_val
        fig = px.bar(df, x='Day', y='count', color='tempo_range', template='plotly_dark', text='count')
        fig.update_traces(textfont={'color':'white'})
        return fig

    def count_songs_day(self):
        rows = self.db.query_count_songs_day()
        df = pd.DataFrame(rows, columns=['Day','count'])
        fig = px.line(df, x='Day', y='count', title='Number of Unique Songs Played per Day', markers=True, text='count', template='plotly_dark')
        fig.update_traces(textposition='top center')
        return fig

    def song_count_by_artist(self):
        rows = self.db.query_count_artist()
        df = pd.DataFrame(rows, columns=['Artist', 'Count'])
        fig = px.bar(df, x='Artist', y='Count', template='plotly_dark')
        print(df)
        return fig
