FROM python:3-alpine

WORKDIR .

COPY requirements.txt requirements.txt

RUN \
	apk add --no-cache --update \
	python3 python3-dev gcc \
	gfortran musl-dev g++ libffi-dev \
	openssl-dev libxml2 libxml2-dev \
	libxslt libxslt-dev libjpeg-turbo-dev zlib-dev \
	libpq postgresql-dev bash
RUN \
	pip install --upgrade pip && \
	pip install --upgrade cython && \
	pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD ["python", "spotify/backend/retrieve.py"]
#CMD ["python", "spotify/backend/update.py"]



