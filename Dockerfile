FROM python:3.9-slim

ADD . /code

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
