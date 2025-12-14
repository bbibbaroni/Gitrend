# GitHub Library Search MCP

GitHub API를 활용하여 라이브러리를 검색하고, LLM을 통해 검색 결과를 분석하여 사용법을 포함한 마크다운 문서를 자동으로 생성하는 MCP(Model Context Protocol) 서버입니다.

## 주요 기능

- 🔍 GitHub 저장소 검색 (star 수 기준 정렬)
- 📊 저장소 상세 정보 조회 (README 포함)
- 🤖 LLM을 활용한 사용법 문서 자동 생성
- 📝 마크다운 형식의 문서 저장
- 🔄 MCP 프로토콜 지원

## 설치

### 1. 저장소 클론

```bash
git clone <repository-url>
cd github-library-search-mcp
```

### 2. 가상 환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

## 설정

### 1. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성합니다:

```bash
cp .env.example .env
```

### 2. API 키 설정

`.env` 파일을 열어 다음 값들을 설정합니다:

```env
# GitHub API Token
GITHUB_TOKEN=your_github_token_here

# LLM API Key (OpenAI)
LLM_API_KEY=your_openai_api_key_here

# Optional settings
LLM_MODEL=gpt-4
OUTPUT_DIR=./docs
PORT=8000
```

#### GitHub Token 발급

1. GitHub 설정 페이지 방문: https://github.com/settings/tokens
2. "Generate new token" 클릭
3. 필요한 권한 선택 (public_repo 권한 필요)
4. 생성된 토큰을 `.env` 파일에 추가

#### OpenAI API Key 발급

1. OpenAI 플랫폼 방문: https://platform.openai.com/api-keys
2. "Create new secret key" 클릭
3. 생성된 키를 `.env` 파일에 추가

## 사용법

### 서버 시작

```bash
python -m src.main
```

서버가 시작되면 다음 주소에서 접근할 수 있습니다:

- 기본 주소: http://localhost:8000
- Health Check: http://localhost:8000/health
- MCP 엔드포인트: http://localhost:8000/mcp

### MCP 도구

서버는 다음 3가지 도구를 제공합니다:

#### 1. search_github_library

GitHub 저장소를 검색합니다.

```json
{
  "method": "tools/call",
  "params": {
    "name": "search_github_library",
    "arguments": {
      "query": "fastapi",
      "limit": 10
    }
  }
}
```

#### 2. get_repository_details

특정 저장소의 상세 정보를 조회합니다.

```json
{
  "method": "tools/call",
  "params": {
    "name": "get_repository_details",
    "arguments": {
      "owner": "tiangolo",
      "repo": "fastapi"
    }
  }
}
```

#### 3. generate_usage_guide

저장소의 사용법 문서를 자동으로 생성합니다.

```json
{
  "method": "tools/call",
  "params": {
    "name": "generate_usage_guide",
    "arguments": {
      "owner": "tiangolo",
      "repo": "fastapi",
      "output_path": "fastapi-guide.md"
    }
  }
}
```

### 도구 목록 조회

```json
{
  "method": "tools/list",
  "params": {}
}
```

## API 예제

### cURL 예제

```bash
# 저장소 검색
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

# 사용법 문서 생성
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "generate_usage_guide",
      "arguments": {
        "owner": "tiangolo",
        "repo": "fastapi"
      }
    }
  }'
```

### Python 예제

```python
import httpx
import asyncio

async def search_library():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/mcp",
            json={
                "method": "tools/call",
                "params": {
                    "name": "search_github_library",
                    "arguments": {
                        "query": "fastapi",
                        "limit": 5
                    }
                }
            }
        )
        print(response.json())

asyncio.run(search_library())
```

## 프로젝트 구조

```
github-library-search-mcp/
├── src/
│   ├── __init__.py
│   ├── main.py              # 메인 엔트리 포인트
│   ├── app.py               # FastAPI 애플리케이션
│   ├── config.py            # 설정 관리
│   ├── models.py            # 데이터 모델
│   ├── error_handler.py     # 오류 처리
│   ├── clients/
│   │   ├── github_client.py # GitHub API 클라이언트
│   │   └── llm_client.py    # LLM API 클라이언트
│   ├── services/
│   │   ├── github.py        # GitHub 서비스
│   │   ├── llm.py           # LLM 서비스
│   │   └── document.py      # 문서 생성 서비스
│   └── mcp/
│       ├── handler.py       # MCP 프로토콜 핸들러
│       └── tools.py         # 도구 정의
├── tests/                   # 테스트
├── docs/                    # 생성된 문서
├── .env                     # 환경 변수
├── .env.example             # 환경 변수 예제
├── requirements.txt         # 의존성
└── README.md
```

## 오류 처리

서버는 다음과 같은 오류 상황을 처리합니다:

- **GitHub API 오류**: 인증 실패, Rate limit 초과, 저장소를 찾을 수 없음
- **LLM API 오류**: API 키 유효하지 않음, Rate limit 초과
- **파일 시스템 오류**: 디렉토리 생성 실패, 파일 쓰기 권한 없음
- **검증 오류**: 필수 매개변수 누락, 잘못된 매개변수 타입

모든 오류는 표준화된 형식으로 반환됩니다:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

## 개발

### 테스트 실행

```bash
pytest
```

### 속성 기반 테스트 실행

```bash
pytest tests/property/
```

## 라이선스

MIT License

## 기여

이슈와 풀 리퀘스트를 환영합니다!
