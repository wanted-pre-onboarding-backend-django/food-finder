## Food Finder

#### **위치 기반 맛집 추천 웹 서비스**
[[원티드 백엔드 프리온보딩 인턴십]](https://www.wanted.co.kr/events/pre_ob_be_1_seoul) - 기업 실무 프로젝트 2차 과제

> 언어 및 프레임워크 : Python 3.10 & Django 5.0, DRF 3.15
RDBMS: PostgreSQL 16.0 \
Server: Nginx, Uvicorn, Gunicorn\
ETC Tools: Docker(Compose), Git & Github, Notion, Discord
Cache & Messaging: Redis
Task Queue: Celery
Scheduler: APScheduler

- 기간: 24.08.27 ~ 24.09.02

<br>

**목차**
1. [프로젝트 소개](#프로젝트-소개)
2. [프로젝트 구조 및 설계](#프로젝트-구조-및-설계)
3. [주요 기능](#주요-기능)
4. [API 명세서](#API-명세서)

<br>

## 프로젝트 소개
경기도 지역 맛집 공공데이터 중식, 일식, 패스트푸드 등을 활용하여 음식점 목록을 자동으로 업데이트 하고 이를 활용합니다. \
사용자 위치에 맞게 맛집 및 메뉴를 추천할수 있으며, 사용자는 맛집 별 평점을 등록 할 수 있습니다. \
이를 통해 더 나은 다양한 음식 경험을 제공하고, 맛집을 좋아하는 사람들 간의 소통과 공유를 활성화 합니다. 

## 프로젝트 구조 및 설계
#### 개발 환경 및 기술 스택
| 카테고리   | 항목                                                      |
|----------------|--------------------------------------------------------------|
| Back-end   | - Python 3.10.11                                             |
|                | - Django 5.0.7                                               |
|                | - Django Rest Framework 3.15.2                               |
|                | - flake8 & black & pre-commit                                |
| DB         | - PostgreSQL 16.0                                            |
|                | - Redis                                                      |
| Server     | - Nginx                                                      |
|                | - Uvicorn                                                    |
|                | - Gunicorn                                                   |
| Task Queue & Scheduler | - Celery                                          |
|                | - APScheduler                                                |
| ETC Tools  | - Docker(Compose)                                            |
|                | - Git & Github                                               |
|                | - Notion                                                     |
|                | - Discord                                                    |

### ERD
![ERD](https://github.com/user-attachments/assets/f8c8206e-18c6-43cc-8057-dbf455dbaa18)

### Service Architecture
![Food Finder Structure](https://private-user-images.githubusercontent.com/64644262/363689166-26fcb683-a2e0-46e6-b70a-299910fa48c9.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjUyODA3NDYsIm5iZiI6MTcyNTI4MDQ0NiwicGF0aCI6Ii82NDY0NDI2Mi8zNjM2ODkxNjYtMjZmY2I2ODMtYTJlMC00NmU2LWI3MGEtMjk5OTEwZmE0OGM5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA5MDIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTAyVDEyMzQwNlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTMzODViYjZkMmNiODQ5Njc3MDdkZDMyZDNmOWZhYWEzNzkyZWVkNjY1ZGZiMjdmODc2YzU5ZWZjOGExM2IyYjAmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.hDEEHm1Ezp-V0NM9afn6yV3ZvZfttTmvnoElyWwrKIU)


### 디렉토리 구조

<details>
<summary>Directory Structure</summary>

```
├── .env
├── .flake8
├── .gitignore
├── Dockerfile
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── db.sqlite3
├── docker-compose.yml
├── nginx.conf
├── src
│   ├── config
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── asgi.py
│   │   ├── authentication.py
│   │   ├── models.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   ├── province
│   │   ├── __init__.py
│   │   ├── admin
│   │   │   ├── __init__.py
│   │   │   └── province_admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── province.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── province_serializers.py
│   │   ├── urls.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── province_list_view.py
│   ├── restaurant
│   │   ├── __init__.py
│   │   ├── admin
│   │   │   ├── __init__.py
│   │   │   ├── raw_data_restaurant.py
│   │   │   └── restaurant_admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── raw_data_restaurant.py
│   │   │   └── restaurant.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   ├── restaurant_detail_serializer.py
│   │   │   └── restaurant_list_serializer.py
│   │   ├── urls.py
│   │   ├── utils
│   │   │   ├── discord_webhook.py
│   │   │   ├── geo_distance.py
│   │   │   └── lunch_recommender.py
│   │   └── views
│   │       ├── __init__.py
│   │       ├── restaurant_detail_view.py
│   │       └── restaurant_list_view.py
│   ├── review
│   │   ├── __init__.py
│   │   ├── admin
│   │   │   ├── __init__.py
│   │   │   └── review_admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── review.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── review_serializer.py
│   │   ├── tests
│   │   │   └── __init__.py
│   │   ├── urls.py
│   │   ├── utils
│   │   │   └── update_restaurant_rating.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── review_view.py
│   ├── script
│   │   ├── data_collection.py
│   │   ├── data_preprocessing.py
│   │   └── lunch_rec_scheduler.py
│   └── user
│       ├── __init__.py
│       ├── admin
│       │   ├── __init__.py
│       │   └── user_admin.py
│       ├── apps.py
│       ├── migrations
│       ├── models
│       │   ├── __init__.py
│       │   └── user.py
│       ├── serializers
│       │   ├── __init__.py
│       │   ├── user_serializer.py
│       │   └── user_signup_serializer.py
│       ├── tests.py
│       ├── urls.py
│       └── views
│           ├── __init__.py
│           ├── user_login_view.py
│           ├── user_logout_view.py
│           ├── user_me_view.py
│           └── user_signup_view.py
```

</details>

### Setting Guide (Docker)
* 루트 디렉토리에 `.env` 밑처럼 세팅
```
SECRET_KEY= // 자체 입력
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/   #디스코드 팀채널에서 복사하세요 
TZ=Asia/Seoul

# DOCKERIZE SETTINGS
# PORT=1234
# USE_DOCKER=True

## POSTGRES SETTINGS
POSTGRES_DB=postgres
POSTGRES_NAME=postgres
POSTGRES_PORT=5123
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# CELERY
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

```

* Ubuntu (Debian Linux) 기준
```
-- 프로젝트 경로로 이동
cd [프로젝트 경로]

-- Docker Compose build & 실행 (=> http://127.0.0.1:8000/ 경로로 접속)
docker-compose up --build

-- 컨테이너 중지 및 생성된 컨테이너 삭제
docker-compose down

-- 로컬 도커 이미지 전체 삭제
docker rmi $(docker images -q)
```

### Developing Guide
[Developing Guide Link](https://github.com/wanted-pre-onboarding-backend-django/food-finder/wiki/Develop-Guide)

## 주요 기능
- **회원가입 및 인증**: 계정 생성, JWT를 통한 인증 및 보안 유지.
- **데이터 파이프라인**: 공공데이터 오픈 API 활용하여 데이터를 수집하고 전처리 후 저장 합니다.
- **자동화**: 스케쥴러로 데이터를 주기적으로 업데이트 합니다. 
- **맛집 조회 및 필터링**: 사용자의 위치 및 지역명을 기반으로 맛집을 조회합니다. 
- **맛집 평가**: 사용자가 해당 맛집을 평가하면 평점을 업데이트 합니다.
- **대규모 트래픽 대비 캐싱**: 레디스를 연동하여 데이터를 캐싱합니다.
- **점심 추천 서비스**: 디스코드 웹훅을 활용하여 사용자에게 주기적으로 맛집을 추천 합니다.

## API 명세서

| API 명칭                | HTTP 메서드 | 엔드포인트                                    | 설명                                                       |
|------------------------|-------------|-----------------------------------------------|------------------------------------------------------------|
| 사용자 회원가입        | POST        | /signup/                                      | 새로운 사용자를 등록합니다.                                  |
| 사용자 로그인          | POST        | /login/                                       | 사용자를 로그인시킵니다.                                     |
| 사용자 로그아웃        | POST        | /logout/                                      | 사용자를 로그아웃시킵니다.                                   |
| 시군구 목록 조회       | GET         | /provinces/                                   | 시군구 목록을 조회합니다.                                    |
| 맛집 목록 조회         | GET         | /restaurants/                                 | 등록된 모든 맛집 목록을 조회합니다.                           |
| 맛집 상세 조회         | GET         | /restaurants/{unique_code}/                   | 특정 맛집의 상세 정보를 조회합니다.                          |
| 맛집 평가 생성         | POST        | /restaurants/{unique_code}/reviews/           | 특정 맛집에 대한 사용자의 평가를 생성합니다.                   |
| 사용자 프로필 조회     | GET         | /users/me/                                    | 현재 로그인된 사용자의 위치정보를 조회합니다.                     |
| 사용자 정보 업데이트   | PUT         | /users/me/                                    | 현재 로그인된 사용자의 위치정보를 업데이트합니다.                 |


