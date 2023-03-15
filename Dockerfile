# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /python-docker

ARG MONGODB BONSAI_URL RAPIDAPI_KEY
ENV MONGODB=${MONGODB} BONSAI_URL=${BONSAI_URL} RAPIDAPI_KEY=${RAPIDAPI_KEY}

COPY requirements.txt requirements.txt

RUN apt-get update \
        && apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev libsndfile1-dev -y \
        && pip3 install pyaudio \
        && apt-get install -y zbar-tools

RUN pip3 install -r requirements.txt

RUN apt-get install -y pulseaudio

COPY . .

# RUN --mount=type=secret,id=MONGODB \
#   --mount=type=secret,id=BONSAI_URL \
#   --mount=type=secret,id=RAPIDAPI_KEY \
#   export MONGODB=$(cat /run/secrets/MONGODB) && \
#   export BONSAI_URL=$(cat /run/secrets/BONSAI_URL) && \
#   export RAPIDAPI_KEY=$(cat /run/secrets/RAPIDAPI_KEY)


# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]

# CMD ["export MONGODB=$(cat /run/secrets/MONGODB) && \
#   export BONSAI_URL=$(cat /run/secrets/BONSAI_URL) && \
#   export RAPIDAPI_KEY=$(cat /run/secrets/RAPIDAPI_KEY)"]