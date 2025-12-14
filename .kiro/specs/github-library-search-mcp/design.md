# Design Document

## Overview

GitHub Library Search MCP는 Model Context Protocol을 구현한 FastAPI 기반 서버로, GitHub API를 통해 라이브러리를 검색하고 LLM을 활용하여 자동으로 사용법 문서를 생성합니다. 이 시스템은 세 가지 주요 컴포넌트로 구성됩니다: GitHub API 클라이언트, LLM 통합 모듈, 그리고 MCP 프로토콜 핸들러입니다.

## Architecture

시스템은 레이어드 아키텍처를 따르며 다음과 같이 구성됩니다:

```
┌─────────────────────────────────────┐
│     MCP Protocol Layer (FastAPI)    │
├─────────────────────────────────────┤
│        Service Layer                │
│  ┌──────────────┐  ┌─────────────┐ │
│  │ GitHub       │  │ LLM         │ │
│  │ Service      │  │ Service     │ │
│  └──────────────┘  └─────────────┘ │
├─────────────────────────────────────┤
│        Client Layer                 │
│  ┌──────────────┐  ┌─────────────┐ │
│  │ GitHub API   │  │ LLM API     │ │
│  │ Client       │  │ Client      │ │
│  └──────────────┘  └─────────────┘ │
├─────────────────────────────────────┤
│     File System & Configuration     │
└─────────────────────────────────────┘
```

### 주요 흐름

1. MCP 클라이언트가 도구 호출 요청을 FastAPI 엔드포인트로 전송
2. MCP 핸들러가 요청을 파싱하고 적절한 서비스로 라우팅
3. GitHub Service가 GitHub API를 통해 저장소 정보 조회
4. LLM Service가 저장소 정보를 분석하여 사용법 문서 생성
5. 생성된 마크다운 문서를 파일 시스템에 저장
6. 결과를 MCP 프로토콜 형식으로 반환

## Components and Interfaces

### 1. MCP Protocol Handler

FastAPI 라우터로 구현되며 MCP 프로토콜 요청을 처리합니다.

```python
class MCPRequest(BaseModel):
    method: str
    params: dict

class MCPResponse(BaseModel):
    result: Optional[dict]
    error: Optional[dict]

@app.post("/mcp")
async def handle_mcp_request(request: MCPRequest) -> MCPResponse:
    pass
```

**주요 메서드:**

- `list_tools()`: 사용 가능한 도구 목록 반환
- `call_tool(name: str, arguments: dict)`: 특정 도구 실행

### 2. GitHub Service

GitHub API와 상호작용하여 저장소 정보를 조회합니다.

```python
class GitHubService:
    def __init__(self, api_token: str):
        self.client = GitHubClient(api_token)

    async def search_repositories(self, query: str, limit: int = 10) -> List[Repository]:
        pass

    async def get_repository_details(self, owner: str, repo: str) -> RepositoryDetails:
        pass

    async def get_readme(self, owner: str, repo: str) -> str:
        pass
```

### 3. LLM Service

LLM API를 호출하여 문서를 생성합니다.

```python
class LLMService:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = LLMClient(api_key, model)

    async def generate_usage_guide(self, repo_info: RepositoryDetails, readme: str) -> str:
        pass
```

### 4. Document Generator

마크다운 문서를 생성하고 파일 시스템에 저장합니다.

```python
class DocumentGenerator:
    def __init__(self, output_dir: str = "./docs"):
        self.output_dir = output_dir

    def generate_markdown(self, content: str, metadata: dict) -> str:
        pass

    def save_document(self, filename: str, content: str, backup: bool = True) -> str:
        pass
```

### 5. Configuration Manager

환경 변수를 로드하고 검증합니다.

```python
class Config:
    GITHUB_TOKEN: str
    LLM_API_KEY: str
    LLM_MODEL: str = "gpt-4"
    OUTPUT_DIR: str = "./docs"
    PORT: int = 8000

    @classmethod
    def load_from_env(cls) -> "Config":
        pass

    def validate(self) -> None:
        pass
```

## Data Models

### Repository

```python
class Repository(BaseModel):
    name: str
    full_name: str
    description: Optional[str]
    stars: int
    forks: int
    language: Optional[str]
    url: str
```

### RepositoryDetails

```python
class RepositoryDetails(BaseModel):
    repository: Repository
    readme: Optional[str]
    topics: List[str]
    license: Optional[str]
    homepage: Optional[str]
    created_at: str
    updated_at: str
```

### Tool Definition

```python
class ToolDefinition(BaseModel):
    name: str
    description: str
    input_schema: dict

class ToolResult(BaseModel):
    content: List[dict]
    isError: bool = False
```

## Correctness Properties

_A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees._

### Property Reflection

prework 분석 결과를 검토한 결과, 다음과 같은 중복성을 발견했습니다:

1. **오류 처리 속성 통합**: 1.3, 2.4, 4.5, 5.3, 5.5는 모두 오류 상황에서 명확한 오류 메시지를 반환하는지 확인합니다. 이들을 하나의 포괄적인 속성으로 통합할 수 있습니다.
2. **API 호출 성공 속성**: 1.2는 일반적인 성공 응답 규칙이지만, 더 구체적인 속성들(2.1, 3.2)에 의해 암시적으로 검증됩니다.
3. **환경 변수 로드**: 6.1과 6.2는 동일한 동작(환경 변수 로드)을 테스트하므로 하나로 통합할 수 있습니다.

### Correctness Properties

**Property 1: GitHub API 호출 시 검색 수행**
_For any_ 유효한 라이브러리 이름, 검색 함수를 호출하면 GitHub API가 호출되어야 합니다.
**Validates: Requirements 1.1**

**Property 2: 검색 결과 정렬**
_For any_ 검색 결과 목록, 반환된 저장소들은 star 수를 기준으로 내림차순 정렬되어야 합니다.
**Validates: Requirements 1.5**

**Property 3: 저장소 정보 필수 필드 포함**
_For any_ 저장소 조회, 반환된 정보는 이름, 설명, star 수, fork 수, 주요 언어를 포함해야 합니다.
**Validates: Requirements 2.1**

**Property 4: README 조회**
_For any_ README가 존재하는 저장소, 저장소 정보 조회 시 README 내용이 반환되어야 합니다.
**Validates: Requirements 2.2**

**Property 5: LLM 호출**
_For any_ 라이브러리 정보, 문서 생성 요청 시 LLM이 호출되어야 합니다.
**Validates: Requirements 3.1**

**Property 6: 마크다운 형식 생성**
_For any_ LLM 출력, 생성된 문서는 유효한 마크다운 형식이어야 합니다.
**Validates: Requirements 3.2**

**Property 7: 문서 필수 섹션 포함**
_For any_ 생성된 문서, 라이브러리 개요, 설치 방법, 기본 사용 예제, 주요 기능 섹션을 포함해야 합니다.
**Validates: Requirements 3.3**

**Property 8: LLM 실패 시 폴백**
_For any_ LLM 호출 실패 상황, 시스템은 기본 템플릿을 사용하여 문서를 생성해야 합니다.
**Validates: Requirements 3.4**

**Property 9: 성공 응답에 파일 경로 포함**
_For any_ 성공적인 문서 생성, 응답에 저장된 파일 경로가 포함되어야 합니다.
**Validates: Requirements 3.5**

**Property 10: 파일 저장 경로**
_For any_ 지정된 경로, 문서는 해당 경로에 .md 확장자로 저장되어야 합니다.
**Validates: Requirements 4.1**

**Property 11: 파일 이름 생성**
_For any_ 라이브러리 이름, 파일 이름이 제공되지 않으면 라이브러리 이름을 기반으로 유효한 파일 이름이 생성되어야 합니다.
**Validates: Requirements 4.3**

**Property 12: 파일 백업**
_For any_ 기존 파일이 존재하는 경우, 덮어쓰기 전에 백업 파일이 생성되어야 합니다.
**Validates: Requirements 4.4**

**Property 13: MCP 프로토콜 응답 형식**
_For any_ 도구 호출, 응답은 MCP 프로토콜 형식(result 또는 error 필드 포함)을 따라야 합니다.
**Validates: Requirements 5.2**

**Property 14: 매개변수 검증**
_For any_ 필수 매개변수가 누락된 도구 호출, 명확한 검증 오류가 반환되어야 합니다.
**Validates: Requirements 5.4**

**Property 15: 오류 메시지 반환**
_For any_ 오류 상황(API 실패, 잘못된 도구 이름, 파일 저장 실패, 실행 오류), 시스템은 명확한 오류 메시지를 반환해야 합니다.
**Validates: Requirements 1.3, 2.4, 4.5, 5.3, 5.5**

**Property 16: 환경 변수 검증**
_For any_ 필수 환경 변수(GITHUB_TOKEN, LLM_API_KEY)가 누락된 경우, 서버는 명확한 오류 메시지와 함께 시작을 중단해야 합니다.
**Validates: Requirements 6.3**

**Property 17: 정상 서버 시작**
_For any_ 올바른 환경 변수 설정, 서버는 정상적으로 시작되어야 합니다.
**Validates: Requirements 6.4**

**Property 18: 인증 오류 처리**
_For any_ 유효하지 않은 API 키, 첫 API 호출 시 인증 오류가 반환되어야 합니다.
**Validates: Requirements 6.5**

**Property 19: 요청 라우팅**
_For any_ MCP 요청, FastAPI는 요청을 적절한 핸들러로 라우팅해야 합니다.
**Validates: Requirements 7.3**

**Property 20: 서버 시작 실패 로깅**
_For any_ 서버 시작 실패, 명확한 오류 메시지가 로그에 기록되어야 합니다.
**Validates: Requirements 7.4**

## Error Handling

### Error Categories

1. **API Errors**

   - GitHub API 인증 실패 (401)
   - Rate limit 초과 (403)
   - 저장소를 찾을 수 없음 (404)
   - 네트워크 타임아웃

2. **LLM Errors**

   - API 키 유효하지 않음
   - Rate limit 초과
   - 응답 생성 실패
   - 타임아웃

3. **File System Errors**

   - 디렉토리 생성 실패
   - 파일 쓰기 권한 없음
   - 디스크 공간 부족

4. **Validation Errors**
   - 필수 매개변수 누락
   - 잘못된 매개변수 타입
   - 잘못된 도구 이름

### Error Response Format

모든 오류는 다음 형식으로 반환됩니다:

```python
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error message",
        "details": {
            # Additional context
        }
    }
}
```

### Retry Strategy

- GitHub API: 3회 재시도 (exponential backoff)
- LLM API: 2회 재시도
- File operations: 재시도 없음 (즉시 실패)

## Testing Strategy

### Unit Testing

pytest를 사용하여 다음 컴포넌트에 대한 단위 테스트를 작성합니다:

1. **Configuration Manager**

   - 환경 변수 로드 및 검증
   - 기본값 설정

2. **GitHub Service**

   - API 클라이언트 모킹
   - 검색 결과 파싱
   - 오류 처리

3. **LLM Service**

   - API 클라이언트 모킹
   - 프롬프트 생성
   - 응답 파싱

4. **Document Generator**

   - 마크다운 생성
   - 파일 저장 및 백업
   - 파일 이름 생성

5. **MCP Handler**
   - 요청 파싱
   - 도구 라우팅
   - 응답 형식화

### Property-Based Testing

Hypothesis 라이브러리를 사용하여 속성 기반 테스트를 작성합니다:

- 각 속성 기반 테스트는 최소 100회 반복 실행됩니다
- 각 테스트는 디자인 문서의 correctness property를 명시적으로 참조합니다
- 테스트 태그 형식: `# Feature: github-library-search-mcp, Property {number}: {property_text}`

**테스트 대상 속성:**

1. 검색 결과 정렬 (Property 2)
2. 저장소 정보 필수 필드 (Property 3)
3. 마크다운 형식 검증 (Property 6)
4. 문서 필수 섹션 (Property 7)
5. 파일 이름 생성 (Property 11)
6. MCP 응답 형식 (Property 13)
7. 매개변수 검증 (Property 14)
8. 오류 메시지 반환 (Property 15)

### Integration Testing

실제 API를 사용하지 않고 모킹된 서비스를 사용하여 전체 흐름을 테스트합니다:

1. 라이브러리 검색 → 문서 생성 → 파일 저장
2. 오류 시나리오 (API 실패, LLM 실패, 파일 저장 실패)
3. MCP 프로토콜 통신

### Test Environment

- Python 3.9+
- pytest
- pytest-asyncio (비동기 테스트)
- Hypothesis (속성 기반 테스트)
- pytest-mock (모킹)
- httpx (HTTP 클라이언트 테스트)

## Implementation Notes

### Dependencies

```
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0.0
httpx>=0.25.0
python-dotenv>=1.0.0
openai>=1.0.0  # or anthropic, depending on LLM choice
pytest>=7.4.0
pytest-asyncio>=0.21.0
hypothesis>=6.90.0
pytest-mock>=3.12.0
```

### Directory Structure

```
github-library-search-mcp/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── github.py        # GitHub service
│   │   ├── llm.py           # LLM service
│   │   └── document.py      # Document generator
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── github_client.py
│   │   └── llm_client.py
│   └── mcp/
│       ├── __init__.py
│       ├── handler.py       # MCP protocol handler
│       └── tools.py         # Tool definitions
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_config.py
│   │   ├── test_github_service.py
│   │   ├── test_llm_service.py
│   │   ├── test_document_generator.py
│   │   └── test_mcp_handler.py
│   ├── property/
│   │   ├── test_properties.py
│   │   └── strategies.py    # Hypothesis strategies
│   └── integration/
│       └── test_integration.py
├── docs/                    # Generated documentation output
├── .env                     # Environment variables
├── requirements.txt
└── README.md
```

### MCP Tools

서버는 다음 도구들을 제공합니다:

1. **search_github_library**

   - 입력: `query` (string), `limit` (int, optional)
   - 출력: 저장소 목록

2. **get_repository_details**

   - 입력: `owner` (string), `repo` (string)
   - 출력: 상세 저장소 정보

3. **generate_usage_guide**
   - 입력: `owner` (string), `repo` (string), `output_path` (string, optional)
   - 출력: 생성된 문서 경로

### LLM Prompt Template

```
You are a technical documentation expert. Based on the following GitHub repository information, create a comprehensive usage guide in Korean.

Repository: {repo_name}
Description: {description}
Language: {language}
Stars: {stars}

README Content:
{readme}

Please create a markdown document with the following sections:
1. 라이브러리 개요 (Library Overview)
2. 설치 방법 (Installation)
3. 기본 사용 예제 (Basic Usage Examples)
4. 주요 기능 (Key Features)
5. 추가 리소스 (Additional Resources)

Make sure the guide is practical, clear, and includes code examples where appropriate.
```

### Performance Considerations

- GitHub API rate limit: 5000 requests/hour (authenticated)
- LLM API rate limit: varies by provider
- 비동기 처리를 통한 동시 요청 지원
- 응답 캐싱 고려 (선택사항)

### Security Considerations

- API 키는 환경 변수로만 관리
- .env 파일은 .gitignore에 추가
- API 키는 로그에 기록하지 않음
- 입력 검증을 통한 injection 공격 방지
