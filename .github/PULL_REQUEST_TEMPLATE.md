## 📝작업 내용
> : 개발에 필요한 환경을 설정하였습니다.
- 라이브러리 설치
  - 개발 환경에만 필요한 라이브러리를 `dev-packages`로 분리하여 관리하도록 설정
- swagger 설정
   - Swagger를 설정하여 API 문서화를 자동화
- 코드 포매팅 및 린팅 설정
   - `black`을 사용하여 코드 포매팅을 자동화
   - `flake8`을 사용하여 코드 스타일 및 린팅 검사를 추가
   - `pre-commit` 훅을 설정하여 커밋 전에 자동으로 포매팅 및 린팅 검사를 수행하도록 구성
- BaseModel 설정
  - `created_at`, `updated_at` 필드를 포함한 추상 클래스 정의
  - 공통 필드를 여러 모델에서 재사용하여 코드 중복을 줄이고, 일관된 데이터 관리가 가능하도록 하기 위함
- Issues, PR template 설정

### 스크린샷 (선택)

## 💬리뷰 요구사항(선택)
> 리뷰어가 특별히 봐주었으면 하는 부분이 있다면 작성해주세요
>
> ex) 메서드 XXX의 이름을 더 잘 짓고 싶은데 혹시 좋은 명칭이 있을까요?


## ⌘관련 이슈
- [[Setting] 개발 환경 설정](https://github.com/wanted-pre-onboarding-backend-django/feed-flow/issues/1)
