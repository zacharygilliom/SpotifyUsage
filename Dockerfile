FROM zacharygilliom/spotifybackend

RUN mkdir spotifyusage/

WORKDIR spotifyusage/

COPY . .
COPY backend-cron /etc/cron.d/backend-cron

RUN \
	apk add --no-cache --upgrade rsyslog vim && \
	pip install --upgrade pip && \
	pip install --upgrade cython && \
	pip install -r requirements.txt && \
	chmod +x spotify/backend/retrieve.py && \
	chmod +x spotify/backend/update.py && \
	chmod +x scripts.sh && \
	touch /var/log/cron.log && \
	mv oauth2.py /usr/local/lib/python3.10/site-packages/spotipy/

RUN chmod 0644 /etc/cron.d/backend-cron
RUN crontab /etc/cron.d/backend-cron

EXPOSE 8050
EXPOSE 8080

CMD ["./scripts.sh"]
