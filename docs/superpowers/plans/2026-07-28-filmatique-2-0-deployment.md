# Filmatique 2.0 배포 구현 계획

> **에이전트 작업 필수 절차:** `superpowers:executing-plans`를 사용해 아래 작업을 순서대로 실행한다. 모든 단계는 체크박스로 추적한다.

**목표:** 수정된 테스트 DB를 보존하면서 마이페이지 오류와 운영 서버 설정을 고치고 `docker.io/dudcks9572/filmatique:2.0`을 Render에 배포한다.

**구조:** 검증된 `pybo.db`는 Git에 커밋하지 않고 로컬 Docker 빌드 입력으로만 사용한다. Flask-Migrate 기준 스키마를 저장소에서 관리하고, 컨테이너 시작 시 마이그레이션 성공 후 Gunicorn을 실행한다.

**기술 구성:** Python 3.13, Flask 3.1, Flask-SQLAlchemy, Flask-Migrate/Alembic, SQLite, pytest, Gunicorn, Docker, Render

## 전체 제약사항

- 배포 이미지 태그는 정확히 `dudcks9572/filmatique:2.0`을 사용한다.
- 검증된 `/Users/yycmac/Downloads/pybo.db`의 테스트 데이터를 보존한다.
- DB 파일과 회원 데이터는 Git에 커밋하지 않는다.
- Render 서비스는 삭제하지 않고 이미지 주소만 교체한다.
- Docker Hub 업로드 전 모든 로컬 테스트를 통과해야 한다.
- Render 무료 요금제의 SQLite 데이터는 재시작 또는 재배포 후 초기화될 수 있음을 유지 문서에 명시한다.

---

### 작업 1: 테스트 가능한 운영 설정

**파일:**
- 수정: `config.py:1-9`
- 수정: `.flaskenv:1-3`
- 수정: `requirements.txt:1-26`
- 생성: `tests/test_config.py`

**인터페이스:**
- 입력: `DATABASE_URL`, `SECRET_KEY`, `FLASK_DEBUG` 환경변수
- 출력: 환경변수 우선 DB 주소와 비밀키, 운영 환경의 비활성화된 디버그 모드

- [ ] **1단계: 설정 실패 테스트 작성**

```python
import importlib


def test_config_uses_database_url_from_environment(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:////tmp/filmatique-test.db")
    import config

    reloaded = importlib.reload(config)

    assert reloaded.SQLALCHEMY_DATABASE_URI == "sqlite:////tmp/filmatique-test.db"


def test_create_app_has_debug_disabled(monkeypatch):
    monkeypatch.setenv("FLASK_DEBUG", "0")
    from pybo import create_app

    app = create_app()

    assert app.debug is False
```

- [ ] **2단계: 테스트가 예상대로 실패하는지 확인**

실행:

```bash
pytest tests/test_config.py -v
```

예상: 첫 번째 테스트가 하드코딩된 SQLite 주소 때문에 실패한다.

- [ ] **3단계: 최소 설정 변경**

`config.py`에서 환경변수를 우선 사용한다.

```python
import os

BASE_DIR = os.path.dirname(__file__)
DEFAULT_DATABASE_URI = "sqlite:///{}".format(os.path.join(BASE_DIR, "pybo.db"))

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URI)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
```

`.flaskenv`는 운영 배포에서 디버거를 켜지 않도록 변경한다.

```text
FLASK_APP=pybo:create_app
FLASK_ENV=production
FLASK_DEBUG=False
```

`requirements.txt`에 다음을 추가한다.

```text
gunicorn==23.0.0
pytest==8.4.2
```

- [ ] **4단계: 설정 테스트 통과 확인**

```bash
pytest tests/test_config.py -v
```

예상: 2개 테스트 모두 통과.

- [ ] **5단계: 변경 커밋**

```bash
git add config.py .flaskenv requirements.txt tests/test_config.py
git commit -m "fix: configure Flask for production deployment"
```

### 작업 2: DB 마이그레이션 기준선 추가

**파일:**
- 수정: `.gitignore:1-6`
- 생성: `migrations/`
- 생성: `tests/test_migrations.py`

**인터페이스:**
- 입력: 빈 SQLite DB와 Flask-Migrate 명령
- 출력: 현재 SQLAlchemy 모델과 동일한 전체 DB 스키마

- [ ] **1단계: 빈 DB 마이그레이션 실패 테스트 작성**

```python
import os
import sqlite3
import subprocess
import sys


def test_migrations_create_reservation_status(tmp_path):
    database_path = tmp_path / "migration.db"
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{database_path}"
    env["FLASK_APP"] = "pybo:create_app"

    result = subprocess.run(
        [sys.executable, "-m", "flask", "db", "upgrade"],
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    with sqlite3.connect(database_path) as connection:
        columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(reservation)")
        }
    assert "status" in columns
```

- [ ] **2단계: 마이그레이션이 없어서 실패하는지 확인**

```bash
pytest tests/test_migrations.py -v
```

예상: `migrations` 설정을 찾지 못해 실패.

- [ ] **3단계: 마이그레이션 폴더를 Git 관리 대상으로 변경**

`.gitignore`에서 다음 줄만 제거한다.

```text
migrations/
```

- [ ] **4단계: 빈 임시 DB를 대상으로 최초 마이그레이션 생성**

```bash
DATABASE_URL=sqlite:////tmp/filmatique-empty.db flask db init
DATABASE_URL=sqlite:////tmp/filmatique-empty.db flask db migrate -m "initial schema"
```

생성된 마이그레이션에서 모든 현재 모델 테이블과
`reservation.status VARCHAR(20)`이 포함됐는지 검토한다.

- [ ] **5단계: 마이그레이션 테스트 통과 확인**

```bash
pytest tests/test_migrations.py -v
```

예상: 통과하고 생성된 `reservation` 테이블에 `status`가 존재한다.

- [ ] **6단계: 변경 커밋**

```bash
git add .gitignore migrations tests/test_migrations.py
git commit -m "fix: track initial database migration"
```

### 작업 3: 배포 DB 검증과 마이페이지 회귀 테스트

**파일:**
- 로컬 배치만 수행: `pybo.db`
- 생성: `tests/test_release_database.py`
- 생성: `tests/test_mypage.py`

**인터페이스:**
- 입력: `/Users/yycmac/Downloads/pybo.db`
- 출력: 무결성이 검증된 빌드용 `pybo.db`, 로그인 세션의 정상 마이페이지 응답

- [ ] **1단계: 수정 전 실패하는 배포 DB 테스트 작성**

```python
import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parents[1] / "pybo.db"


def test_release_database_is_valid():
    assert DATABASE_PATH.exists()
    with sqlite3.connect(DATABASE_PATH) as connection:
        assert connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(reservation)")
        }
        missing_statuses = connection.execute(
            "SELECT COUNT(*) FROM reservation WHERE status IS NULL"
        ).fetchone()[0]
    assert "status" in columns
    assert missing_statuses == 0
```

- [ ] **2단계: 프로젝트에 DB가 없어 실패하는지 확인**

```bash
pytest tests/test_release_database.py -v
```

예상: `pybo.db`가 존재하지 않아 실패.

- [ ] **3단계: 검증된 DB를 빌드 위치에 복사**

```bash
cp /Users/yycmac/Downloads/pybo.db ./pybo.db
```

`pybo.db`가 `.gitignore`의 `*.db` 규칙으로 계속 제외되는지 확인한다.

- [ ] **4단계: DB 검증 테스트 통과 확인**

```bash
pytest tests/test_release_database.py -v
git status --short
```

예상: 테스트 통과, `pybo.db`는 Git 변경 목록에 없음.

- [ ] **5단계: 마이페이지 실패 회귀 테스트 작성**

```python
import importlib


def test_authenticated_user_can_open_mypage(monkeypatch, tmp_path):
    release_db = tmp_path / "pybo.db"
    release_db.write_bytes(
        (__import__("pathlib").Path(__file__).parents[1] / "pybo.db").read_bytes()
    )
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{release_db}")

    import config
    importlib.reload(config)
    from pybo import create_app

    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()
    with client.session_transaction() as session:
        session["user_id"] = 1

    response = client.get("/film/mypage")

    assert response.status_code == 200
    assert b"OperationalError" not in response.data
```

- [ ] **6단계: 마이페이지 테스트 통과 확인**

```bash
pytest tests/test_mypage.py -v
```

예상: `/film/mypage` HTTP 200.

- [ ] **7단계: 테스트 코드만 커밋**

```bash
git add tests/test_release_database.py tests/test_mypage.py
git commit -m "test: cover release database and mypage"
```

### 작업 4: 안전한 Docker 이미지 구성

**파일:**
- 수정: `Dockerfile:1-30`
- 생성: `.dockerignore`
- 생성: `tests/test_docker_config.py`

**인터페이스:**
- 입력: 애플리케이션 코드, 마이그레이션, 검증된 `pybo.db`, Render의 `PORT`
- 출력: 마이그레이션 후 Gunicorn으로 실행되는 운영 이미지

- [ ] **1단계: Docker 설정 실패 테스트 작성**

```python
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_dockerfile_runs_migrations_then_gunicorn():
    dockerfile = (ROOT / "Dockerfile").read_text()
    assert "flask db upgrade" in dockerfile
    assert "gunicorn" in dockerfile
    assert "${PORT:-5000}" in dockerfile
    assert 'CMD ["flask", "run"' not in dockerfile


def test_dockerignore_excludes_sensitive_local_files():
    dockerignore = (ROOT / ".dockerignore").read_text()
    assert ".git" in dockerignore
    assert "test keys.txt" in dockerignore
    assert ".flaskenv" in dockerignore
```

- [ ] **2단계: 기존 Dockerfile 때문에 실패하는지 확인**

```bash
pytest tests/test_docker_config.py -v
```

예상: 마이그레이션, Gunicorn, `.dockerignore` 조건이 없어 실패.

- [ ] **3단계: Docker 빌드 제외 목록 작성**

```text
.git
.gitignore
.venv
__pycache__
*.pyc
.flaskenv
test keys.txt
docs
tests
```

`pybo.db`는 이미지에 포함해야 하므로 제외하지 않는다.

- [ ] **4단계: Dockerfile을 운영 실행 방식으로 변경**

```dockerfile
FROM python:3.13-slim

ENV TZ=Asia/Seoul \
    FLASK_APP=pybo:create_app \
    FLASK_ENV=production \
    FLASK_DEBUG=0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN flask db stamp head

EXPOSE 5000

CMD ["sh", "-c", "flask db upgrade && exec gunicorn --bind 0.0.0.0:${PORT:-5000} 'pybo:create_app()'"]
```

- [ ] **5단계: Docker 설정 테스트 통과 확인**

```bash
pytest tests/test_docker_config.py -v
```

예상: 모두 통과.

- [ ] **6단계: 전체 Python 테스트 실행**

```bash
pytest -v
```

예상: 전체 통과.

- [ ] **7단계: 변경 커밋**

```bash
git add Dockerfile .dockerignore tests/test_docker_config.py
git commit -m "fix: run production container with migrations"
```

### 작업 5: 이미지 2.0 빌드와 로컬 검증

**파일:**
- 생성하지 않음
- 생성되는 로컬 아티팩트: Docker 이미지 `dudcks9572/filmatique:2.0`

**인터페이스:**
- 입력: 작업 1~4의 커밋과 로컬 `pybo.db`
- 출력: 로컬에서 검증된 Docker 이미지

- [ ] **1단계: Docker Desktop 실행 상태 확인**

```bash
docker version
```

예상: Client와 Server 버전이 모두 표시됨.

- [ ] **2단계: 이미지 빌드**

```bash
docker build -t dudcks9572/filmatique:2.0 .
```

예상: 빌드 성공 및 마이그레이션 버전 stamp 성공.

- [ ] **3단계: 컨테이너 실행**

```bash
docker run --rm -d --name filmatique-2-test -p 5050:5000 \
  -e SECRET_KEY=filmatique-local-smoke-test \
  dudcks9572/filmatique:2.0
```

- [ ] **4단계: 시작 로그 확인**

```bash
docker logs filmatique-2-test
```

예상: 마이그레이션 성공, Gunicorn worker 시작, Werkzeug 디버거 미노출.

- [ ] **5단계: 서비스와 마이페이지 자동 검증**

```bash
curl -f http://127.0.0.1:5050/
docker exec filmatique-2-test python -c "from pybo import create_app; app=create_app(); app.config['TESTING']=True; client=app.test_client(); tx=client.session_transaction(); session=tx.__enter__(); session['user_id']=1; tx.__exit__(None,None,None); response=client.get('/film/mypage'); assert response.status_code == 200, response.status_code"
```

예상: 홈페이지 응답 성공, 로그인 세션의 `/film/mypage` HTTP 200.

- [ ] **6단계: 테스트 컨테이너 종료**

```bash
docker stop filmatique-2-test
```

### 작업 6: Docker Hub 및 Render 배포

**파일:**
- 수정하지 않음

**인터페이스:**
- 입력: 검증된 `dudcks9572/filmatique:2.0`
- 출력: Docker Hub 이미지와 해당 이미지를 실행하는 Render 서비스

- [ ] **1단계: Docker Hub 로그인 상태 확인**

```bash
docker info
```

로그인이 없으면 사용자가 Docker Hub 로그인을 완료한 뒤 진행한다. 비밀번호나
토큰을 코드·로그·대화에 출력하지 않는다.

- [ ] **2단계: Docker Hub에 이미지 업로드**

```bash
docker push dudcks9572/filmatique:2.0
```

예상: 모든 레이어 업로드 후 `2.0` digest 표시.

- [ ] **3단계: Docker Hub 태그 확인**

Docker Hub의 `dudcks9572/filmatique` 저장소에서 `2.0` 태그와 방금 출력된
digest가 일치하는지 확인한다.

- [ ] **4단계: Render 이미지 주소 변경**

Render 서비스의 이미지 주소를 다음 값으로 변경한다.

```text
docker.io/dudcks9572/filmatique:2.0
```

현재 서비스를 삭제하거나 새 서비스를 만들지 않는다.

- [ ] **5단계: Render 운영 비밀키 설정**

Render 환경변수 `SECRET_KEY`에 새로 생성한 충분히 긴 무작위 값을 설정한다.
비밀키 값을 코드·로그·대화에 출력하지 않는다. 키가 변경되면 기존 로그인
세션은 만료되므로 배포 후 다시 로그인한다.

- [ ] **6단계: Render 배포 로그 확인**

마이그레이션 성공, Gunicorn 시작, 포트 바인딩 성공을 확인한다. 오류가 발생하면
서비스 URL 검증으로 넘어가지 않고 로그 원인을 먼저 해결한다.

- [ ] **7단계: 운영 서비스 확인**

```text
https://filmatique-vfst.onrender.com/
https://filmatique-vfst.onrender.com/film/mypage
```

로그인 후 마이페이지 HTTP 200, 기존 예약 표시, 디버거 미노출을 확인한다.

- [ ] **8단계: 배포 결과 기록**

Docker Hub 이미지 digest, Render 배포 시각, 검증한 기능과 알려진 무료
SQLite 제한을 최종 인수인계에 기록한다.
