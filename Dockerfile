FROM zacharygilliom/spotifybackend

RUN mkdir spotifyusage/

WORKDIR spotifyusage/

COPY . .

RUN \
	apk add --no-cache --upgrade rsyslog && \
	pip install --upgrade pip && \
	pip install --upgrade cython && \
	pip install -r requirements.txt && \
	chmod +x spotify/backend/retrieve.py && \
	chmod +x spotify/backend/update.py && \
	chmod +x scripts.sh && \
	touch /var/log/cron.log

RUN echo "*/5 * * * * bash /home/spotifyusage/spotify/backend/retrieve.py" >> newcron 2>&1
RUN echo "* */1 * * * bash /home/spotifyusage/spotify/backend/update.py" >> newcron 2>&1
RUN crontab newcron

EXPOSE 8050

CMD ["./scripts.sh"]
