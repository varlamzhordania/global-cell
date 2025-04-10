FROM python:3.11

# Set working directory
WORKDIR /home/global-cell/web

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gettext && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ./requirements.txt /home/global-cell/web
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
