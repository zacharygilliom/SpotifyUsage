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
        self.create_tables()

    def create_tables(self):
        with psycopg.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS songs (
                        id serial PRIMARY KEY,
                        name varchar(100),
                        artist varchar(100),
                        spotify_id varchar(100) unique)
                    """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS played (
                        spotify_id varchar(100) references songs(spotify_id),
                        played_at timestamp unique)
                    """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS audio_features (
                        spotify_id varchar(100) references songs(spotify_id) unique,
                        danceability real,
                        energy real,
                        key integer,
                        loudness real,
                        mode int,
                        speechiness real,
                        acousticness real,
                        instrumentalness real,
                        liveness real,
                        valence real,
                        tempo real)
                    """)
                conn.commit()
                conn.close()

    def query(self, table):
        with psycopg.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {table}")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
                conn.commit()
                conn.close()
                return rows

    def query_songs_no_features(self):
        with psycopg.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT spotify_id FROM audio_features WHERE danceability is NULL""")
                rows = cur.fetchall()
                conn.commit()
                conn.close()
                return [row[0] for row in rows]

    def insert_new_songs(self, song_list):
        with psycopg.connect(**self.params) as conn:
            with conn.cursor() as cur:
                for song in song_list:
                    cur.execute("""INSERT INTO songs (name, artist, spotify_id)
                                    VALUES(%s,%s, %s)
                                    ON CONFLICT (spotify_id) DO NOTHING""",
                                    (song['name'], song['artist'], song['spotify_id']))
                    cur.execute("""INSERT INTO audio_features (spotify_id)
                                    VALUES(%s)
                                    ON CONFLICT (spotify_id) DO NOTHING""",
                                    (song['spotify_id'],))
                    cur.execute("""INSERT INTO played (spotify_id, played_at)
                                    VALUES (%s, %s)
                                    ON CONFLICT (played_at) DO NOTHING""",
                                    (song['spotify_id'], song['played_at']))
                conn.commit()
                conn.close()

    def insert_audio_features(self, feature_list):
        with psycopg.connect(**self.params) as conn:
            with conn.cursor() as cur:
                for song in feature_list:
                    cur.execute("""UPDATE audio_features
                                   SET danceability = %s, energy = %s, key = %s, loudness = %s, mode = %s, speechiness = %s, acousticness = %s, instrumentalness = %s, liveness = %s,
                                        valence = %s, tempo = %s
                                   WHERE spotify_id = %s""",
                                    (song['danceability'], song['energy'], song['key'], song['loudness'], song['mode'], song['speechiness'], song['acousticness'],
                                     song['instrumentalness'], song['liveness'], song['valence'], song['tempo'], song['id']))
                conn.commit()
                conn.close()

    def drop(self, table):
        with psycopg.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"DROP TABLE {table}")
                conn.commit()
                conn.close()
