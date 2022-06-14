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
	touch /var/log/cron.log

RUN echo "*/5 * * * * bash /spotify/backend/retrieve.py" >> newcron 2>&1
RUN echo "* */1 * * * bash /spotify/backend/update.py" >> newcron 2>&1
RUN crontab newcron

EXPOSE 8050

#CMD ["python3", "spotify/dashboard/app.py"]
CMD ["crond", "-L", "/var/log/cron.log"]
