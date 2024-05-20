FROM python:3.11

WORKDIR /home/global-cell

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

COPY ./requirements.txt /home/global-cell

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
