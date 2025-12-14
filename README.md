# Gitrend

## 2. 작품 주제

GitHub API와 LLM을 활용한 라이브러리 검색 및 자동 문서 생성 MCP 서버

## 3. 주제 선정이유

개발자들이 새로운 라이브러리를 찾고 사용법을 학습하는 과정은 많은 시간이 소요됩니다. GitHub에서 라이브러리를 검색하고, README를 읽고, 사용법을 이해하는 일련의 과정을 자동화하여 개발 생산성을 향상시키고자 했습니다. 특히 MCP(Model Context Protocol)를 활용하여 LLM 클라이언트와 통합 가능한 도구를 제공함으로써, AI 기반 개발 워크플로우에 자연스럽게 통합될 수 있도록 설계했습니다.

## 4. 작품 링크

### 1) GitHub 링크

```
(GitHub 저장소 URL을 여기에 추가하세요)
```

### 2) 배포링크 (선택)

```
로컬 실행: http://localhost:8000
Health Check: http://localhost:8000/health
MCP Endpoint: http://localhost:8000/mcp
```

## 5. 프로젝트 설명

### 1) 개발기간

2024년 12월 (약 2주)

### 2) 팀 구성

개인 프로젝트

### 3) 기술 스택

#### Backend Framework

- **FastAPI 0.104.0+**: 비동기 웹 프레임워크, MCP 프로토콜 엔드포인트 구현
- **Uvicorn 0.24.0+**: ASGI 서버, FastAPI 애플리케이션 실행

#### API Integration

- **httpx 0.25.0+**: 비동기 HTTP 클라이언트, GitHub API 및 LLM API 호출
- **OpenAI API 1.0.0+**: GPT-4 모델을 활용한 문서 자동 생성

#### Data Validation & Configuration

- **Pydantic 2.0.0+**: 데이터 모델 정의 및 검증, MCP 프로토콜 메시지 구조화
- **python-dotenv 1.0.0+**: 환경 변수 관리, API 키 보안 처리

#### Testing

- **pytest 7.4.0+**: 단위 테스트 프레임워크
- **pytest-asyncio 0.21.0+**: 비동기 함수 테스트 지원
- **Hypothesis 6.90.0+**: 속성 기반 테스트 (Property-Based Testing)
- **pytest-mock 3.12.0+**: 모킹 및 스텁 생성

#### Architecture Pattern

- **레이어드 아키텍처**: Presentation(FastAPI) → Service → Client 계층 분리
- **의존성 주입**: 서비스 간 느슨한 결합
- **비동기 프로그래밍**: async/await를 활용한 동시성 처리

### 4) 주요 기능 및 실행 화면

#### 기능 1: 서버 Health Check

**엔드포인트**: `GET /health`

**기능 설명**:

- 서버 상태 확인
- 서비스 가용성 모니터링

**실행 예시**:

```bash
curl http://localhost:8000/health
```

**응답**:

```json
{
  "status": "healthy",
  "service": "github-library-search-mcp"
}
```

---

#### 기능 2: GitHub 라이브러리 검색

**도구명**: `search_github_library`

**기능 설명**:

- GitHub API를 통해 라이브러리 검색
- Star 수 기준 내림차순 정렬
- 저장소 이름, 설명, Star/Fork 수, 주요 언어 정보 제공

**실행 예시**:

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "search_github_library",
      "arguments": {
        "query": "fastapi",
        "limit": 5
      }
    }
  }'
```

**응답 예시**:

```json
{
  "result": {
    "content": [
      {
        "type": "text",
        "text": "검색 결과: 5개의 저장소를 찾았습니다.\n\n1. tiangolo/fastapi\n   ⭐ 75,000 | 🍴 6,300\n   FastAPI framework, high performance...\n\n2. ..."
      }
    ]
  }
}
```

---

#### 기능 3: 저장소 상세 정보 조회

**도구명**: `get_repository_details`

**기능 설명**:

- 특정 저장소의 상세 정보 조회
- README 내용 포함
- 토픽, 라이선스, 생성/수정 날짜 정보 제공

**실행 예시**:

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "get_repository_details",
      "arguments": {
        "owner": "tiangolo",
        "repo": "fastapi"
      }
    }
  }'
```

---

#### 기능 4: 사용법 문서 자동 생성

**도구명**: `generate_usage_guide`

**기능 설명**:

- LLM(GPT-4)을 활용한 한국어 사용법 문서 자동 생성
- 라이브러리 개요, 설치 방법, 사용 예제, 주요 기능 포함
- 마크다운 형식으로 저장
- LLM 실패 시 기본 템플릿으로 폴백

**실행 예시**:

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "generate_usage_guide",
      "arguments": {
        "owner": "tiangolo",
        "repo": "fastapi",
        "output_path": "fastapi-guide.md"
      }
    }
  }'
```

**응답 예시**:

```json
{
  "result": {
    "content": [
      {
        "type": "text",
        "text": "✅ 사용법 문서가 생성되었습니다.\n파일 경로: ./docs/fastapi-guide.md"
      }
    ]
  }
}
```

**생성된 문서 예시**:

```markdown
# tiangolo/fastapi

## 라이브러리 개요

FastAPI는 Python 3.7+의 표준 타입 힌트를 기반으로 한
현대적이고 빠른 웹 프레임워크입니다...

## 설치 방법

pip install fastapi
pip install "uvicorn[standard]"

## 기본 사용 예제

...
```

---

#### 기능 5: MCP 도구 목록 조회

**메서드**: `tools/list`

**기능 설명**:

- 사용 가능한 모든 MCP 도구 목록 반환
- 각 도구의 이름, 설명, 입력 스키마 제공

**실행 예시**:

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/list",
    "params": {}
  }'
```

---

#### 기능 6: 오류 처리

**기능 설명**:

- GitHub API 오류 (인증 실패, Rate limit, 404)
- LLM API 오류 (인증 실패, Rate limit)
- 파일 시스템 오류 (권한, 디스크 공간)
- 검증 오류 (필수 매개변수 누락)

**오류 응답 형식**:

```json
{
  "error": {
    "code": "GITHUB_API_ERROR",
    "message": "Repository not found",
    "details": {
      "status_code": 404
    }
  }
}
```

## 6. 프로젝트 폴더 구조

```
github-library-search-mcp/
├── .env                          # 환경 변수 (API 키)
├── .env.example                  # 환경 변수 예제
├── .gitignore                    # Git 제외 파일
├── README.md                     # 프로젝트 문서
├── requirements.txt              # Python 의존성
├── answer.md                     # 프로젝트 보고서
│
├── .kiro/                        # Kiro IDE 설정
│   └── specs/
│       └── github-library-search-mcp/
│           ├── requirements.md   # 요구사항 명세
│           ├── design.md         # 설계 문서
│           └── tasks.md          # 작업 목록
│
├── src/                          # 소스 코드
│   ├── __init__.py
│   ├── main.py                   # 메인 엔트리 포인트
│   ├── app.py                    # FastAPI 애플리케이션
│   ├── config.py                 # 설정 관리
│   ├── models.py                 # Pydantic 데이터 모델
│   ├── error_handler.py          # 전역 오류 처리
│   │
│   ├── clients/                  # API 클라이언트 계층
│   │   ├── __init__.py
│   │   ├── github_client.py      # GitHub API 클라이언트
│   │   └── llm_client.py         # LLM API 클라이언트
│   │
│   ├── services/                 # 비즈니스 로직 계층
│   │   ├── __init__.py
│   │   ├── github.py             # GitHub 서비스
│   │   ├── llm.py                # LLM 서비스
│   │   └── document.py           # 문서 생성 서비스
│   │
│   └── mcp/                      # MCP 프로토콜 계층
│       ├── __init__.py
│       ├── handler.py            # MCP 요청 핸들러
│       └── tools.py              # MCP 도구 정의
│
└── tests/                        # 테스트 코드
    ├── __init__.py
    ├── unit/                     # 단위 테스트
    │   ├── __init__.py
    │   ├── test_config.py
    │   └── test_document_generator.py
    ├── property/                 # 속성 기반 테스트
    │   └── __init__.py
    └── integration/              # 통합 테스트
        └── __init__.py
```

## 7. 소스 코드

### 1) 전체 코드 구조

#### 핵심 파일 설명

**src/main.py** - 서버 시작점

```python
"""Main entry point for the MCP server"""
import uvicorn
from src.config import Config, ConfigurationError
from src.error_handler import log_startup_error

def main():
    """Start the MCP server"""
    try:
        config = Config.load_from_env()
        uvicorn.run(
            "src.app:app",
            host="0.0.0.0",
            port=config.PORT,
            log_level="info",
            reload=False
        )
    except ConfigurationError as e:
        log_startup_error(e)
        print(f"\n❌ Configuration Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
```

**src/app.py** - FastAPI 애플리케이션

- 서비스 초기화 및 생명주기 관리
- MCP 엔드포인트 라우팅
- 전역 예외 처리

**src/config.py** - 환경 변수 관리

```python
class Config:
    def __init__(self):
        load_dotenv()
        self.GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        self.LLM_API_KEY = os.getenv("LLM_API_KEY")
        self.LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
        self.OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./docs")
        self.PORT = int(os.getenv("PORT", "8000"))

    def validate(self):
        if not self.GITHUB_TOKEN or not self.LLM_API_KEY:
            raise ConfigurationError("Missing required API keys")
```

**src/models.py** - 데이터 모델

- Repository: GitHub 저장소 정보
- RepositoryDetails: 상세 저장소 정보
- MCPRequest/MCPResponse: MCP 프로토콜 메시지
- ToolDefinition/ToolResult: 도구 정의 및 결과

**src/clients/github_client.py** - GitHub API 클라이언트

- 비동기 HTTP 요청 처리
- 인증 헤더 관리
- Rate limit 처리
- 오류 처리 및 재시도 로직

**src/clients/llm_client.py** - LLM API 클라이언트

- OpenAI API 통합
- 프롬프트 전송 및 응답 처리
- 토큰 관리

**src/services/github.py** - GitHub 서비스

- 저장소 검색 (Star 수 정렬)
- 저장소 상세 정보 조회
- README 내용 가져오기

**src/services/llm.py** - LLM 서비스

- 사용법 문서 생성 프롬프트 구성
- LLM 호출 및 응답 처리
- 실패 시 폴백 템플릿 제공

**src/services/document.py** - 문서 생성 서비스

- 마크다운 문서 생성
- 파일 저장 및 백업
- 디렉토리 관리

**src/mcp/handler.py** - MCP 프로토콜 핸들러

- MCP 요청 파싱
- 도구 라우팅
- 응답 형식화

**src/mcp/tools.py** - MCP 도구 정의

- search_github_library
- get_repository_details
- generate_usage_guide

**src/error_handler.py** - 오류 처리

- 전역 예외 핸들러
- 표준화된 오류 응답
- 로깅 설정

### 2) Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY .env.example .env

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "-m", "src.main"]
```

### 3) requirements.txt

```
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0.0
httpx>=0.25.0
python-dotenv>=1.0.0
openai>=1.0.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
hypothesis>=6.90.0
pytest-mock>=3.12.0
```

## 8. Trouble Shooting

### 문제 1: GitHub API Rate Limit 초과

**발생한 문제**:
개발 중 GitHub API를 반복적으로 호출하다가 Rate Limit(시간당 60회)에 도달하여 API 호출이 실패하는 문제가 발생했습니다.

**해결 방법**:

1. Personal Access Token을 발급받아 인증된 요청으로 변경 (시간당 5,000회로 증가)
2. 환경 변수로 토큰을 관리하여 보안 유지
3. 오류 응답에서 Rate Limit 정보를 파싱하여 사용자에게 명확한 메시지 제공

**학습 내용**:

- GitHub API의 Rate Limit 정책 이해
- 인증된 요청과 비인증 요청의 차이
- HTTP 헤더를 통한 Rate Limit 정보 확인 방법

---

### 문제 2: 비동기 프로그래밍 오류

**발생한 문제**:
FastAPI의 비동기 엔드포인트에서 동기 함수를 호출하여 `RuntimeWarning: coroutine was never awaited` 경고가 발생했습니다.

**해결 방법**:

1. 모든 I/O 작업(API 호출, 파일 저장)을 비동기 함수로 변경
2. `httpx.AsyncClient`를 사용하여 비동기 HTTP 요청 처리
3. `async/await` 키워드를 일관되게 사용

**학습 내용**:

- Python의 asyncio 이벤트 루프 동작 원리
- 동기/비동기 함수 혼용 시 발생하는 문제
- FastAPI의 비동기 처리 메커니즘

**코드 예시**:

```python
# Before (동기)
def search_repositories(self, query: str):
    response = requests.get(url)
    return response.json()

# After (비동기)
async def search_repositories(self, query: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

---

### 문제 3: Pydantic 모델 필드 매핑

**발생한 문제**:
GitHub API 응답의 필드명(`stargazers_count`)과 내부 모델의 필드명(`stars`)이 달라 데이터 매핑이 실패했습니다.

**해결 방법**:

1. Pydantic의 `Field` 클래스에서 `alias` 매개변수 사용
2. `Config.populate_by_name = True` 설정으로 양방향 매핑 지원

**학습 내용**:

- Pydantic의 필드 별칭(alias) 기능
- API 응답과 내부 모델 간 데이터 변환 패턴
- 데이터 검증 및 직렬화/역직렬화

**코드 예시**:

```python
class Repository(BaseModel):
    stars: int = Field(alias="stargazers_count", default=0)
    forks: int = Field(alias="forks_count", default=0)

    class Config:
        populate_by_name = True
```

---

### 문제 4: LLM API 비용 및 타임아웃

**발생한 문제**:
GPT-4 API 호출 시 응답 시간이 길어지고 비용이 증가하는 문제가 발생했습니다.

**해결 방법**:

1. LLM 호출 실패 시 기본 템플릿으로 폴백하는 로직 구현
2. 프롬프트 최적화로 토큰 사용량 감소
3. 타임아웃 설정으로 무한 대기 방지
4. 환경 변수로 모델 선택 가능하게 하여 GPT-3.5 등 저렴한 모델 사용 옵션 제공

**학습 내용**:

- LLM API의 비용 구조 (입력/출력 토큰 기반)
- 프롬프트 엔지니어링 기법
- 폴백 패턴을 통한 시스템 안정성 향상

---

### 문제 5: 환경 변수 누락 시 서버 시작 실패

**발생한 문제**:
`.env` 파일이 없거나 필수 환경 변수가 누락된 경우 서버가 시작 후 첫 API 호출 시점에 오류가 발생하여 디버깅이 어려웠습니다.

**해결 방법**:

1. `Config` 클래스에 `validate()` 메서드 추가
2. 서버 시작 시점에 환경 변수 검증 수행
3. 누락된 변수를 명확히 표시하는 오류 메시지 제공
4. `.env.example` 파일로 필요한 환경 변수 가이드 제공

**학습 내용**:

- Fail-fast 원칙의 중요성
- 명확한 오류 메시지의 가치
- 환경 변수 관리 베스트 프랙티스

**코드 예시**:

```python
def validate(self):
    missing = []
    if not self.GITHUB_TOKEN:
        missing.append("GITHUB_TOKEN")
    if not self.LLM_API_KEY:
        missing.append("LLM_API_KEY")

    if missing:
        raise ConfigurationError(
            f"Missing required environment variables: {', '.join(missing)}"
        )
```

---

### 문제 6: MCP 프로토콜 응답 형식 불일치

**발생한 문제**:
MCP 클라이언트가 기대하는 응답 형식과 서버가 반환하는 형식이 달라 통신이 실패했습니다.

**해결 방법**:

1. MCP 프로토콜 스펙 문서를 상세히 검토
2. Pydantic 모델로 응답 형식을 엄격하게 정의
3. 모든 도구 결과를 `ToolResult` 모델로 표준화
4. 단위 테스트로 응답 형식 검증

**학습 내용**:

- 프로토콜 스펙 준수의 중요성
- 타입 안정성을 통한 버그 예방
- 계약 기반 API 설계

---

### 문제 7: 파일 저장 시 디렉토리 미존재

**발생한 문제**:
문서를 저장할 때 출력 디렉토리가 존재하지 않아 `FileNotFoundError`가 발생했습니다.

**해결 방법**:

1. 파일 저장 전 디렉토리 존재 여부 확인
2. `os.makedirs(exist_ok=True)`로 디렉토리 자동 생성
3. 파일 저장 실패 시 명확한 오류 메시지 반환

**학습 내용**:

- 파일 시스템 작업의 방어적 프로그래밍
- 경로 처리 시 고려사항
- 오류 처리의 세분화

---

### 기술적 성과

1. **레이어드 아키텍처 구현**: 관심사 분리를 통한 유지보수성 향상
2. **비동기 프로그래밍**: FastAPI와 httpx를 활용한 고성능 I/O 처리
3. **타입 안정성**: Pydantic을 통한 런타임 데이터 검증
4. **오류 처리**: 전역 예외 핸들러와 표준화된 오류 응답
5. **테스트 전략**: 단위 테스트, 속성 기반 테스트, 통합 테스트 구현
6. **보안**: 환경 변수를 통한 API 키 관리
7. **확장성**: MCP 프로토콜을 통한 LLM 클라이언트 통합 가능

---

## 9. 실행 방법

### 환경 설정

```bash
# 1. 저장소 클론
git clone <repository-url>
cd github-library-search-mcp

# 2. 가상 환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 GITHUB_TOKEN과 LLM_API_KEY 설정

# 5. 서버 시작
python -m src.main
```

### 테스트 실행

```bash
# 전체 테스트
pytest

# 단위 테스트만
pytest tests/unit/

# 속성 기반 테스트만
pytest tests/property/
```

---

## 10. 향후 개선 방향

1. **캐싱 구현**: Redis를 활용한 API 응답 캐싱으로 성능 향상
2. **데이터베이스 연동**: 생성된 문서 메타데이터 저장 및 검색 기능
3. **웹 UI 추가**: 사용자 친화적인 웹 인터페이스 제공
4. **다국어 지원**: 영어, 일본어 등 다양한 언어로 문서 생성
5. **배치 처리**: 여러 라이브러리를 한 번에 처리하는 기능
6. **통계 대시보드**: 사용 통계 및 인기 라이브러리 분석
