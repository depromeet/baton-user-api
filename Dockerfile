FROM python:3.9
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt