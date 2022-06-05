FROM python:3.9
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

CMD ["gunicorn", "--bind", "0:8000", "config.wsgi:application"]
