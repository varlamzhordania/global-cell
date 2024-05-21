FROM python:3.11

WORKDIR /home/global-cell/web

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

COPY ./requirements.txt /home/global-cell/web

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
