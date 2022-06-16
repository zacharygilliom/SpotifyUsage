FROM zacharygilliom/spotifybackend

RUN mkdir spotifyusage/

WORKDIR spotifyusage/

COPY . .

RUN \
	apk add --no-cache --upgrade rsyslog vim && \
	pip install --upgrade pip && \
	pip install --upgrade cython && \
	pip install -r requirements.txt && \
	chmod +x spotify/backend/retrieve.py && \
	chmod +x spotify/backend/update.py && \
	chmod +x scripts.sh && \
	touch /var/log/cron.log

RUN echo "*/1 * * * * /usr/bin/env python3 /home/spotifyusage/spotify/backend/retrieve.py" >> newcron 2>&1
RUN echo "* */1 * * * /usr/bin/env pyton3 /home/spotifyusage/spotify/backend/update.py" >> newcron 2>&1
ADD oauth2.py /usr/local/lib/python3.10/site-packages/spotipy/
RUN crontab newcron

EXPOSE 8050
EXPOSE 8080

CMD ["./scripts.sh"]
