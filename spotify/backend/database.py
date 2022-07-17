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

    def query(self):
        with psycopg.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT p.played_at, s.name, s.artist, af.energy
                               FROM songs s
                               LEFT JOIN played p ON s.spotify_id = p.spotify_id
                               LEFT JOIN audio_features af ON s.spotify_id = af.spotify_id""")
                rows = cur.fetchall()
                conn.commit()
                conn.close()
                return rows

    def query_time_series(self):
        with psycopg.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                               SELECT to_char(p.played_at, 'Day') AS Day, avg(af.danceability), avg(af.energy), avg(af.loudness), avg(af.speechiness), avg(af.acousticness), avg(af.instrumentalness),
                                avg(af.liveness), avg(af.valence), avg(af.tempo)
                                    FROM played p
                                    LEFT JOIN audio_features af ON p.spotify_id = af.spotify_id
                                    GROUP BY Day""")
                rows = cur.fetchall()
                conn.commit()
                conn.close()
                return rows

    def query_unique_songs_by_day(self):
        with psycopg.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT tempo_range.Day, tempo_range.tempo_range, COUNT(*) FROM (
                                SELECT to_char(p.played_at, 'Day') AS Day,
                                    CASE WHEN af.tempo < 50 THEN 'Low'
                                        WHEN af.tempo BETWEEN 50 AND 150 THEN 'Mid'
                                        WHEN af.tempo > 150 THEN 'High'
                                        WHEN af.tempo is NULL THEN '0s'
                                    END AS tempo_range
                                FROM played p
                                    LEFT JOIN audio_features af
                                        ON p.spotify_id = af.spotify_id
                            ) tempo_range GROUP BY tempo_range.Day, tempo_range.tempo_range
                           """)
                rows = cur.fetchall()
                conn.commit()
                conn.close()
                return rows

    def query_count_songs_day(self):
        with psycopg.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT to_char(p.played_at, 'MON-DD') AS Day, COUNT(DISTINCT p.spotify_id)
                            FROM played p
                            WHERE p.played_at > CURRENT_DATE - 7
                            GROUP BY Day
                        """)
                rows = cur.fetchall()
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
                if len(rows) >0:
                    return [row[0] for row in rows]
                return []

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

    def query_count_artist(self):
        with psycopg.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT s.artist AS Artist, COUNT(DISTINCT p.played_at) count
                            FROM played p
                            LEFT JOIN songs s
                            ON p.spotify_id = s.spotify_id
                            WHERE p.played_at > CURRENT_DATE - 7
                            GROUP BY Artist
                            ORDER BY count DESC
                            LIMIT 10
                            """)
                rows = cur.fetchall()
                conn.commit()
                conn.close()
                return rows

