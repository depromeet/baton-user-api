FROM python:3.9
ENV PYTHONUNBUFFERED=1

RUN mkdir /baton-user-api
WORKDIR /baton-user-api

COPY requirement.txt /baton-user-api/
RUN pip install -r requirement.txt
COPY . /baton-user-api/