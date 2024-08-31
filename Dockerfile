FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요 라이브러리 설치를 위한 패키지 복사
COPY Pipfile Pipfile.lock ./

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

# pipenv 설치
RUN pip install pipenv

# Python 버전 확인 및 패키지 설치
RUN python --version
RUN pipenv --python /usr/local/bin/python3.10 install --deploy --ignore-pipfile

# 소스 코드 복사
COPY src/ src/
COPY .env .env
COPY nginx.conf /etc/nginx/nginx.conf


# 작업 디렉토리 변경
WORKDIR /app/src

# 포트 개방
EXPOSE 8000
