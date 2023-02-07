# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /python-docker

COPY requirements.txt requirements.txt

RUN apt-get update \
        && apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev libsndfile1-dev -y \
        && pip3 install pyaudio \
        && apt-get install -y zbar-tools

RUN pip3 install -r requirements.txt

RUN apt-get install -y pulseaudio

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]