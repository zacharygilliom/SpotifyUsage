#FROM python:3-alpine
#FROM frolvlad/alpine-miniconda3
FROM nickgryg/alpine-pandas

RUN mkdir spotifyusage/

WORKDIR spotifyusage/

#COPY requirements.txt spotifyusage/requirements.txt

COPY . .

RUN \
	apk add --no-cache --update \
	python3 python3-dev gcc \
	gfortran musl-dev g++ libffi-dev \
	openssl-dev libxml2 libxml2-dev \
	libxslt libxslt-dev libjpeg-turbo-dev zlib-dev \
	libpq postgresql-dev bash && \
	pip install --upgrade pip && \
	pip install --upgrade cython && \
	pip install -r requirements.txt && \
	chmod +x spotify/backend/retrieve.py && \
	chmod +x spotify/backend/update.py

RUN echo "*/5 * * * * bash /spotify/backend/retrieve.py" >> newcron
RUN echo "* */1 * * * bash /spotify/backend/update.py" >> newcron
RUN crontab newcron
CMD ["python3", "spotify/dashboard/app.py"]
