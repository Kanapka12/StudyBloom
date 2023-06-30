FROM python:3.11-slim-buster
WORKDIR /usr/src/StudyBloom
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip pipenv
COPY Pipfile* ./
RUN pipenv install --system --ignore-pipfile
COPY . .


