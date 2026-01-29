FROM python:3.10.8-slim-buster

ENV TZ=Asia/Dhaka
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git build-essential tzdata ffmpeg libssl-dev libffi-dev && \
    ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime && echo "$TZ" > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -U pip wheel==0.45.1

WORKDIR /app
COPY requirements.txt /app
RUN pip install -U -r requirements.txt

COPY . /app

CMD flask run -h 0.0.0.0 -p 5000 & python3 main.py

