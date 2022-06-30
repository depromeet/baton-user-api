# baton-user-api

[Google Play에서 바통 다운로드](https://play.google.com/store/apps/details?id=com.depromeet.baton)

![banner](https://user-images.githubusercontent.com/86508420/176690477-a0d002fc-ce84-4820-a3a9-daaba24d9eb6.png)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

디프만 11기 6조 바통의 API Gateway & 인증서버, 마이페이지 API

baton-user-api는 django projects로 구성되며 기능은 아래와 같다.

1. auth-server: api-gateway, 인증 API
2. user-api: 마이페이지 API

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [API endpoints](#api-endpoints)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [See more](#see-more)

## Background

### Architecture

![API Flowpng](https://user-images.githubusercontent.com/86508420/176701877-78c21e38-c2e5-40d5-a815-fd0a9ddc358a.png)
![인프라](https://user-images.githubusercontent.com/86508420/176702393-281778aa-46cd-4815-aeb1-72a971b371a5.png)


### Database Schema

![DBSchema_light](https://user-images.githubusercontent.com/86508420/176701610-721ab6c0-8a22-41e3-9ab9-b33b4fb6e881.png)


### CI/CD

![CICD](https://user-images.githubusercontent.com/86508420/176702474-614a02fa-a296-4ab1-9e06-eb8de6a6e9ea.png)


## Install

1. 레포지토리 파일을 다운로드

```
$ git clone https://github.com/depromeet/baton-user-api.git
```

## Usage

docker 및 docker-compose가 설치된 Linux 환경에서만 실행 가능

### Local environment

* 환경변수 파일로 .env.local 사용

* django runserver로 서버 구동

#### 실행 방법

1. 프로젝트 디렉토리에 `.env.local` 파일 생성. (xxxx는 사용자 로컬 환경에 맞추어 입력)

```
SECRET_KEY=xxxx

DATABASES_NAME=xxxx
DATABASES_USER=xxxx
DATABASES_PASSWORD=xxxx
DATABASES_HOST=host.docker.internal
DATABASES_PORT=xxxx

KAKAO_REST_API_KEY=xxxx

AWS_S3_ACCESS_KEY_ID=xxxx
AWS_S3_SECRET_ACCESS_KEY=xxxx
```

2. docker-compose 실행

```
$ docker-compose -f docker-compose.local.yml up
```

### Production environment

* 환경변수 파일로 .env.prod 사용

* gunicorn을 wsgi 서버로 사용

#### 실행 방법

1. 프로젝트 디렉토리에 `.env.prod` 파일 생성. (xxxx는 사용자 배포 환경에 맞추어 입력)

```
SECRET_KEY=xxxx

DATABASES_NAME=xxxx
DATABASES_USER=xxxx
DATABASES_PASSWORD=xxxx
DATABASES_HOST=xxxx
DATABASES_PORT=xxxx

KAKAO_REST_API_KEY=xxxx

AWS_S3_ACCESS_KEY_ID=xxxx
AWS_S3_SECRET_ACCESS_KEY=xxxx
```

2. docker-compose 실행

```
$ docker-compose -f docker-compose.prod.yml up
```

#### Upload static files in production environment (optional)

1. `.env.prod`를 각 앱 디렉토리로 복사

```
$ cp .env.prod auth-server/
$ cp .env.prod user-api/
```

2. docker-compose 실행

```
$ docker-compose -f docker-compose.prod.yml up
```

2. static 파일을 AWS S3 버킷에 저장 (새로운 터미널에서 명령어 입력)

```
$ docker exec -it user-api /bin/bash
/app# python manage.py collectstatic --settings=config.settings.prod --noinput
```

```
$ docker exec -it auth-server /bin/bash
/app# python manage.py collectstatic --settings=config.settings.prod --noinput
```

## API endpoints

swagger로 API 명세 제공

* [auth-server swagger](https://baton.yonghochoi.com/swagger)
* [user-api swagger](https://baton.yonghochoi.com/user/swagger)

## Features

* RESTful API
* Extensible - Oauth provider 추가 용이 등
* auth-server와 user-api 사이의 종속성 제거

## Technology Stack

<div align='center'>

![OAuth2.0](https://img.shields.io/badge/-OAuth2.0-FFCD00?logo=Kakao&logoColor=black&style=flat)
![JWT](https://img.shields.io/badge/-JWT-000000?logo=JSON%20Web%20Tokens&logoColor=white&style=flat)<br>
![Django](https://img.shields.io/badge/-Django-092E20?logo=Django&logoColor=white&style=flat)
![MySQL](https://img.shields.io/badge/-MySQL-blue?logo=MySQL&logoColor=white&style=flat)<br>
![Python](https://img.shields.io/badge/-Python-3776AB?logo=Python&logoColor=white&style=flat)
![Gunicorn](https://img.shields.io/badge/-Gunicorn-499848?logo=Gunicorn&logoColor=white&style=flat)
![Swagger](https://img.shields.io/badge/-Swagger-a4ff82?logo=Swagger&logoColor=black&style=flat)<br>
![Docker](https://img.shields.io/badge/-Docker-2496ED?logo=Docker&logoColor=white&style=flat)
![Github--Actions](https://img.shields.io/badge/-Github--Actions-0006ff?logo=GitHub%20Actions&logoColor=white&style=flat)
![AWS S3](https://img.shields.io/badge/-AWS%20S3-569A31?logo=Amazon%20S3&logoColor=white&style=flat)

</div>

### Python packages

#### Common

* Python 3.9
* [Django](https://www.djangoproject.com/) 4.0.3
* [Django REST framework](https://www.django-rest-framework.org/) - Django 기반의 RESTful API 제작
* mysqlclient - DBMS로 MySQL 사용
* gunicorn - 배포 환경에서의 wsgi 서버
* [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/index.html) - DRF 코드를 바탕으로 swagger API 명세 생성
* [django-environ](https://django-environ.readthedocs.io/en/latest/) - `.env` 파일로 환경변수 관리
* [django-request-logging](https://github.com/Rhumbix/django-request-logging) - 로컬 및 배포 환경에서 log 출력 형식을 꾸밈

#### auth-server app

* [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html) - JWT기반의 사용자 인증 구현
* [djproxy](https://pypi.org/project/djproxy/#description) - reverse-proxy 서버 제작

#### user-api App

* [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html), [djang-storages](https://django-storages.readthedocs.io/en/latest/) - AWS S3에 이미지 파일 업로드
* (linux package) gdal-bin - MySQL 환경에서 GeoDjango를 사용하기 위한 기초 라이브러리

### CI/CD

* Dockerfile - django project 별로 docker image를 정의
* Docker Compose - 로컬 개발 환경에서 두 컨테이너를 통합하여 실행
* github action - 배포 작업(`.env.prod` 작성, docker image를 build하여 AWS ECR에 push)을 자동화, secrets를 효율적으로 관리

## See more

* [Baton](https://github.com/depromeet/Baton) (Android)
* [baton-search-api](https://github.com/depromeet/baton-search-api)
* [baton-chat-server](https://github.com/depromeet/baton-chat-server)
* [baton-infra](https://github.com/depromeet/baton-infra)

### Download at
![QR코드](https://user-images.githubusercontent.com/86508420/176703343-2a5030ba-f30c-407d-af3b-1797681bcaf7.png)
