# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
WORKDIR /john-pizza
RUN python3 -m pip install -U pip wheel setuptools
COPY requirements.txt /john-pizza/
RUN python3 -m pip install -r requirements.txt
COPY . /john-pizza/