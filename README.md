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
![image](https://github.com/user-attachments/assets/46501415-2656-4924-8588-7e872be2dd64)

### ERD
![image](https://github.com/user-attachments/assets/ad487190-e000-4433-ba9d-84e8bfaf6bf1)

### Service Architecture
![image](https://github.com/user-attachments/assets/9aef30b3-91df-48a0-b7ec-461977e25a1b)


### 디렉토리 구조

<details>
<summary>Directory Structure</summary>
<div markdown="1">
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
│   ├── config
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── asgi.py
│   │   ├── authentication.py
│   │   ├── models.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   ├── province
│   │   ├── __init__.py
│   │   ├── admin
│   │   │   ├── __init__.py
│   │   │   └── province_admin.py
│   │   ├── apps.py
│   │   ├─+ migrations
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── province.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── province_serializers.py
│   │   ├── urls.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── province_list_view.py
│   ├── restaurant
│   │   ├── __init__.py
│   │   ├── admin
│   │   │   ├── __init__.py
│   │   │   ├── raw_data_restaurant.py
│   │   │   └── restaurant_admin.py
│   │   ├── apps.py
│   │   ├─+ migrations
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── raw_data_restaurant.py
│   │   │   └── restaurant.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   ├── restaurant_detail_serializer.py
│   │   │   └── restaurant_list_serializer.py
│   │   ├── urls.py
│   │   ├── utils
│   │   │   ├── discord_webhook.py
│   │   │   ├── geo_distance.py
│   │   │   └── lunch_recommender.py
│   │   └── views
│   │       ├── __init__.py
│   │       ├── restaurant_detail_view.py
│   │       └── restaurant_list_view.py
│   ├── review
│   │   ├── __init__.py
│   │   ├── admin
│   │   │   ├── __init__.py
│   │   │   └── review_admin.py
│   │   ├── apps.py
│   │   ├─+ migrations
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── review.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── review_serializer.py
│   │   ├── tests
│   │   │   └── __init__.py
│   │   ├── urls.py
│   │   ├── utils
│   │   │   └── update_restaurant_rating.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── review_view.py
│   ├── script
│   │   ├── data_collection.py
│   │   ├── data_preprocessing.py
│   │   └── lunch_rec_scheduler.py
│   └── user
│       ├── __init__.py
│       ├── admin
│       │   ├── __init__.py
│       │   └── user_admin.py
│       ├── apps.py
│       ├─+ migrations
│       ├── models
│       │   ├── __init__.py
│       │   └── user.py
│       ├── serializers
│       │   ├── __init__.py
│       │   ├── user_serializer.py
│       │   └── user_signup_serializer.py
│       ├── tests.py
│       ├── urls.py
│       └── views
│           ├── __init__.py
│           ├── user_login_view.py
│           ├── user_logout_view.py
│           ├── user_me_view.py
│           └── user_signup_view.py
```
</div>
</details>

### Setting Guide (Docker)
* 루트 디렉토리에 `.env` 밑처럼 세팅
```
SECRET_KEY= // 자체 입력
POSTGRES_DB=feedflowdb
POSTGRESQL_HOST=postgres => 해당 부분은 무조건 고정
POSTGRES_USER= // 자체 입력
POSTGRES_PASSWORD= // 자체 입력
TZ=Asia/Seoul
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

- [API 명세서 노션 링크](https://www.notion.so/034179/FeedFlow-2af2b82c6acc4ae3af8a0c593225ccc4?pvs=4#f5f3c11a023a47bd9a99f4e30335e029)


### 프로젝트 폴더 바로 아래에 .env 파일을 만들고 아래 내용을 넣어주세요.
```
SECRET_KEY=your-secret-key
```

### 프로젝트 환경설정
아래의 명령어를 순서대로 실행해주세요.
```shell
# 1. 가상환경 만들기 (초기 설정 시 1회 실행)
> pipenv install
> pipenv install --dev

# 2. 가상환경 실행
> pipenv shell

# 3. pre-commit 실행 (초기 설정 시 1회 실행)
> pipenv run pre-commit install

# 4. django 실행하기
> src 폴더내에서 진행합니다
> python manage.py migrate
> python manage.py runserver
```


### Docker를 이용한 개발 환경 구성

1. 아래 환경변수를 .env파일에 추가로 넣어주세요.

```
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

2. `docker-compose up -d --build`


### 개발 명령어 모음

```shell
# formatter 실행
> black .

# linter 실행
> flake8

# 가상환경 종료
> deactivate

# 가상환경 삭제
> pipenv --rm

# 추가 패키지 설치 (가상환경 활성화 후 실행)
> pipenv install 패키지명

# 패키지 라이브러리 버전 확인
> pip show 패키지

# 관리자 계정 생성
> python manage.py createsuperuser
```

### Conventional Commits
```markdown
- feat: 새로운 기능을 추가할 때 사용.
- fix: 버그를 수정할 때 사용.
- docs: 문서에 대한 변경 사항을 기록할 때 사용 (코드 변경 없음).
- style: 코드의 의미에 영향을 주지 않는 변경 사항 (포맷팅, 세미콜론 누락 등).
- refactor: 코드 리팩토링 (기능 추가나 버그 수정 없음).
- test: 테스트 추가나 기존 테스트 수정.
- chore: 빌드 프로세스나 패키지 매니저 설정 등, 그 외의 변경 사항.
```


## 문서화 확인하는 방법
- [127.0.0.1:8000/swagger](127.0.0.1:8000/swagger) 또는 [127.0.0.1:8000/redoc](127.0.0.1:8000/redoc) 접속하기





