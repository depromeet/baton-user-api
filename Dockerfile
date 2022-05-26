FROM python:3.9
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver --settings=config.settings.prod 0.0.0.0:8000"]
