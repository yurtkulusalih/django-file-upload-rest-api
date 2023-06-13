FROM python:3.9-slim

RUN apt-get -y update && apt-get -y install build-essential python3-pip python3.9-dev \
    python3.9-distutils cmake git wget unzip ffmpeg imagemagick libmagic1 && \
    python3.9 -m pip install --no-cache-dir pybind11 uwsgi wheel setuptools

COPY . /api
WORKDIR /api

RUN echo "\n\e[32mInstalling packages...\n\e[39m" && \
    python3.9 -m pip install --no-cache-dir -r requirements.txt && \
    python3.9 -m pip cache purge && \
    echo "\n\e[32mDone!\n\e[39m"
