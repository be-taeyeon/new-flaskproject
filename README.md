# 0. Getting Started (시작하기)
```bash
$ GPT 시작해줘~^^
```
[서비스 링크]

<br/>
<br/>

# 1. Project Overview (프로젝트 개요)
- 프로젝트 이름: 남자어/여자어 능력고사!!
- 프로젝트 설명: 남자어와 여자어에 대해 어느정도 알고 있는지 테스트해보는 사이트 입니다.

<br/>
<br/>

# 2. Team Members (팀원 및 팀 소개)
| 김태연 | 최규호 | 이유진 | 김상협 |
|:------:|:------:|:------:|:------:|
| <img src="https://github.com/user-attachments/assets/c1c2b1e3-656d-4712-98ab-a15e91efa2da" alt="김태연" width="150"> | <img src="https://github.com/user-attachments/assets/78ec4937-81bb-4637-975d-631eb3c4601e" alt="최규호" width="150"> | <img src="https://github.com/user-attachments/assets/78ce1062-80a0-4edb-bf6b-5efac9dd992e" alt="이유진" width="150"> | <img src="https://github.com/user-attachments/assets/beea8c64-19de-4d91-955f-ed24b813a638" alt="김상협" width="150"> |
| 대표 | 노예 | 노예 | 노예 |
| [GitHub](https://github.com/be-taeyeon) | [GitHub](https://github.com/gyuho231) | [GitHub](NOT YET) | [GitHub](https://github.com/harry99990) |

<br/>
<br/>

# 3. Key Features (주요 기능)
- **회원가입**:
  - 회원가입 시 DB에 유저정보가 등록됩니다.

- **로그인**:
  - 사용자 인증 정보를 통해 로그인합니다.

- **설문 테스트**:
  - 사용자의 성별에따라 선택하여 설문을 시작할수있습니다.

- **결과**:
  - 테스트 종료후 결과를 볼수있습니다.



<!-- - **설문 조사하기**:
  - 캘린더 UI를 통해 동아리 관련 일정 추가&삭제가 가능합니다.
  - 체크박스를 통해 종료되거나 이미 수행한 일정을 표시할 수 있습니다.

 -->

<br/>
<br/>

# 4. Tasks & Responsibilities (작업 및 역할 분담)
|  |  |  |
|-----------------|-----------------|-----------------|
| 김태연    |  <img src="https://github.com/user-attachments/assets/c1c2b1e3-656d-4712-98ab-a15e91efa2da" alt="이동규" width="100"> | <ul><li>팀장</li><li>유저 함수 코딩, 질문 정리</li><li>피피티준비및 발표</li></ul>     |
| 최규호   |  <img src="https://github.com/user-attachments/assets/78ec4937-81bb-4637-975d-631eb3c4601e" alt="신유승" width="100">| <ul><li>전체뼈대 흐름 구축</li><li>사이트 배포</li><li>ORM활용한 함수</li></ul> |
| 이유진   |  <img src="https://github.com/user-attachments/assets/78ce1062-80a0-4edb-bf6b-5efac9dd992e" alt="김나연" width="100">    |<ul><li>유일한 여성</li><li>이미지 파일 과 그 상황에 맞게 로직 구축</li><li>초이스 함수및 css담당</li></ul>  |
| 김상협    |  <img src="https://github.com/user-attachments/assets/beea8c64-19de-4d91-955f-ed24b813a638" alt="이승준" width="100">    | <ul><li>코딩 아재</li><li>질문 함수 코딩및 전반적인 연결 로직구축</li><li>데이터 베이스 연결</li></ul>    |

<br/>
<br/>



# 5. Project Structure (프로젝트 구조)
```oz_form/                        # 프로젝트 폴더
├── .venv                       # 가상환경   
├── app/                        # Flask 애플리케이션 코드 폴더
│   ├── __init__.py             # 앱 초기화 및 설정 파일
│   ├── sevices/                # DB 상호작용 orm 코드 폴더
│   │   ├── users.py            # users 테이블 관련 orm 함수
│   │   ├── questions.py        # quetions 테이블 관련 orm 함수
│   │   ├── choices.py          # choices 테이블 관련 orm 함수
│   │   ├── images.py           # images 테이블 관련 orm 함수
│   │   └── answers.py          # answers 테이블 관련 orm 함수
│   ├── models.py               # SQLAlchemy 모델 정의
│   ├── routes.py               # 뷰 및 라우트 정의
├── config.py                   # Flask 및 데이터베이스 설정 파일
├── requirements.txt            # 필요한 Python 패키지 목록
├── run.py                      # 개발환경에서 테스트 하는 실행 파일
├── wsgi.py                     # 배포환경에서의 실행 파일
└── migrations/                 # Flask-Migrate를 위한 DB 마이그레이션 파일
                                # 추후 자동으로 생성됩니다!
```

<br/>
<br/>

# 6. Development Workflow (개발 워크플로우)
## 브랜치 전략 (Branch Strategy)
우리의 브랜치 전략은 Git Project 를 기반으로 하며, 다음과 같은 브랜치를 사용합니다.

- Main Branch
  - 배포 가능한 상태의 코드를 유지합니다.
  - 모든 배포는 이 브랜치에서 이루어집니다.

- Develop Branch
  - 중간 단계의 브랜치로 메인브랜치로 합병하기
  - 전에 최대한 충돌을 방지하기 위한 브랜치입니다.
  
- {name} Branch
  - 팀원 각자의 개발 브랜치입니다.
  - 모든 기능 개발은 이 브랜치에서 이루어집니다.

<br/>
<br/>


# 7. 커밋 컨벤션
## 기본 구조
```
type : subject

body 
```

<br/>

## 커밋 종류
```
feat : 새로운 기능 추가
fix : 버그 수정
docs : 문서 수정
style : 코드 포맷팅, 세미콜론 누락, 코드 변경이 없는 경우
refactor : 코드 리펙토링
test : 테스트 코드, 리펙토링 테스트 코드 추가
chore : 빌드 업무 수정, 패키지 매니저 수정
```

<br/>

## 커밋 이모지
```
== 코드 관련
📝	코드 작성
🔥	코드 제거
🔨	코드 리팩토링
💄	UI / style 변경

== 문서&파일
📰	새 파일 생성
🔥	파일 제거
📚	문서 작성

== 버그
🐛	버그 리포트
🚑	버그를 고칠 때

== 기타
🐎	성능 향상
✨	새로운 기능 구현
💡	새로운 아이디어
🚀	배포
```

<br/>

## 커밋 예시
```
== ex1
✨Feat: "회원 가입 기능 구현"

SMS, 이메일 중복확인 API 개발

== ex2
📚chore: styled-components 라이브러리 설치

UI개발을 위한 라이브러리 styled-components 설치
```

