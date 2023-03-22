# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /app

ARG MONGODB BONSAI_URL RAPIDAPI_KEY
ENV MONGODB=${MONGODB} BONSAI_URL=${BONSAI_URL} RAPIDAPI_KEY=${RAPIDAPI_KEY}

COPY requirements.txt requirements.txt

RUN apt-get update \
        && apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev libsndfile1-dev -y \
        && pip3 install pyaudio \
        && apt-get install -y zbar-tools

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
RUN apt-get install -y pulseaudio

COPY . .

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 60 app:app

