# Implementation Plan

- [x] 1. 프로젝트 구조 및 기본 설정

  - 디렉토리 구조 생성 (src/, tests/, docs/)
  - requirements.txt 작성 및 의존성 정의
  - .gitignore 파일 생성 (.env, **pycache**, docs/ 등)
  - _Requirements: 7.1_

- [x] 2. 설정 관리 구현

  - Config 클래스 작성 (환경 변수 로드 및 검증)
  - .env 파일 템플릿 생성
  - 환경 변수 검증 로직 구현
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ]\* 2.1 환경 변수 로드 테스트 작성

  - **Property 16: 환경 변수 검증**
  - **Validates: Requirements 6.3**

- [ ]\* 2.2 정상 서버 시작 테스트 작성

  - **Property 17: 정상 서버 시작**
  - **Validates: Requirements 6.4**

- [x] 3. 데이터 모델 정의

  - Pydantic 모델 작성 (Repository, RepositoryDetails, ToolDefinition, ToolResult)
  - MCPRequest, MCPResponse 모델 작성
  - 입력 검증 규칙 정의
  - _Requirements: 5.4_

- [ ]\* 3.1 매개변수 검증 속성 테스트 작성

  - **Property 14: 매개변수 검증**
  - **Validates: Requirements 5.4**

- [x] 4. GitHub API 클라이언트 구현

  - GitHubClient 클래스 작성
  - 저장소 검색 메서드 구현
  - 저장소 상세 정보 조회 메서드 구현
  - README 가져오기 메서드 구현
  - 재시도 로직 및 오류 처리 구현
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.4_

- [ ]\* 4.1 GitHub API 호출 속성 테스트 작성

  - **Property 1: GitHub API 호출 시 검색 수행**
  - **Validates: Requirements 1.1**

- [ ]\* 4.2 저장소 정보 필수 필드 속성 테스트 작성

  - **Property 3: 저장소 정보 필수 필드 포함**
  - **Validates: Requirements 2.1**

- [ ]\* 4.3 README 조회 속성 테스트 작성

  - **Property 4: README 조회**
  - **Validates: Requirements 2.2**

- [x] 5. GitHub Service 구현

  - GitHubService 클래스 작성
  - search_repositories 메서드 구현 (정렬 포함)
  - get_repository_details 메서드 구현
  - get_readme 메서드 구현
  - _Requirements: 1.1, 1.4, 1.5, 2.1, 2.2, 2.3_

- [ ]\* 5.1 검색 결과 정렬 속성 테스트 작성

  - **Property 2: 검색 결과 정렬**
  - **Validates: Requirements 1.5**

- [x] 6. LLM API 클라이언트 구현

  - LLMClient 클래스 작성 (OpenAI 또는 Anthropic)
  - API 호출 메서드 구현
  - 재시도 로직 및 오류 처리 구현
  - _Requirements: 3.1, 6.5_

- [ ]\* 6.1 인증 오류 처리 속성 테스트 작성

  - **Property 18: 인증 오류 처리**
  - **Validates: Requirements 6.5**

- [x] 7. LLM Service 구현

  - LLMService 클래스 작성
  - 프롬프트 템플릿 작성
  - generate_usage_guide 메서드 구현
  - 폴백 템플릿 구현 (LLM 실패 시)
  - _Requirements: 3.1, 3.2, 3.4_

- [ ]\* 7.1 LLM 호출 속성 테스트 작성

  - **Property 5: LLM 호출**
  - **Validates: Requirements 3.1**

- [ ]\* 7.2 LLM 실패 시 폴백 속성 테스트 작성

  - **Property 8: LLM 실패 시 폴백**
  - **Validates: Requirements 3.4**

- [x] 8. Document Generator 구현

  - DocumentGenerator 클래스 작성
  - 마크다운 생성 메서드 구현
  - 파일 이름 생성 로직 구현
  - 파일 저장 메서드 구현 (백업 포함)
  - 디렉토리 생성 로직 구현
  - _Requirements: 3.2, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ]\* 8.1 마크다운 형식 검증 속성 테스트 작성

  - **Property 6: 마크다운 형식 생성**
  - **Validates: Requirements 3.2**

- [ ]\* 8.2 문서 필수 섹션 속성 테스트 작성

  - **Property 7: 문서 필수 섹션 포함**
  - **Validates: Requirements 3.3**

- [ ]\* 8.3 파일 이름 생성 속성 테스트 작성

  - **Property 11: 파일 이름 생성**
  - **Validates: Requirements 4.3**

- [ ]\* 8.4 파일 백업 속성 테스트 작성

  - **Property 12: 파일 백업**
  - **Validates: Requirements 4.4**

- [ ]\* 8.5 파일 저장 경로 속성 테스트 작성

  - **Property 10: 파일 저장 경로**
  - **Validates: Requirements 4.1**

- [x] 9. MCP 도구 정의

  - Tool 정의 작성 (search_github_library, get_repository_details, generate_usage_guide)
  - 각 도구의 input schema 정의
  - 도구 목록 반환 함수 구현
  - _Requirements: 5.1_

- [x] 10. MCP Protocol Handler 구현

  - MCP 요청 파싱 로직 구현
  - 도구 라우팅 로직 구현
  - MCP 응답 형식화 로직 구현
  - 오류 응답 생성 로직 구현
  - _Requirements: 5.2, 5.3, 5.5_

- [ ]\* 10.1 MCP 프로토콜 응답 형식 속성 테스트 작성

  - **Property 13: MCP 프로토콜 응답 형식**
  - **Validates: Requirements 5.2**

- [ ]\* 10.2 요청 라우팅 속성 테스트 작성

  - **Property 19: 요청 라우팅**
  - **Validates: Requirements 7.3**

- [x] 11. 통합 오류 처리 구현

  - 전역 오류 핸들러 작성
  - 오류 응답 형식 표준화
  - 로깅 설정
  - _Requirements: 1.3, 2.4, 3.4, 4.5, 5.3, 5.5, 7.4_

- [ ]\* 11.1 오류 메시지 반환 속성 테스트 작성

  - **Property 15: 오류 메시지 반환**
  - **Validates: Requirements 1.3, 2.4, 4.5, 5.3, 5.5**

- [ ]\* 11.2 서버 시작 실패 로깅 속성 테스트 작성

  - **Property 20: 서버 시작 실패 로깅**
  - **Validates: Requirements 7.4**

- [x] 12. FastAPI 애플리케이션 구현

  - FastAPI 앱 초기화
  - MCP 엔드포인트 구현 (/mcp)
  - 헬스 체크 엔드포인트 구현 (/health)
  - 서비스 의존성 주입 설정
  - 시작 및 종료 이벤트 핸들러 구현
  - _Requirements: 7.1, 7.2, 7.3, 7.5_

- [ ]\* 12.1 성공 응답에 파일 경로 포함 속성 테스트 작성

  - **Property 9: 성공 응답에 파일 경로 포함**
  - **Validates: Requirements 3.5**

- [x] 13. 메인 엔트리 포인트 작성

  - main.py 작성
  - uvicorn 서버 설정
  - 환경 변수 로드 및 검증
  - 서버 시작 로직
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 7.1_

- [x] 14. Checkpoint - 모든 테스트 통과 확인

  - 모든 테스트가 통과하는지 확인하고, 문제가 있으면 사용자에게 질문합니다.

- [x] 15. README 및 문서 작성

  - README.md 작성 (설치, 설정, 사용법)
  - .env.example 파일 작성
  - API 문서 작성
  - _Requirements: 6.1, 6.2_

- [ ] 16. 최종 통합 테스트
  - 전체 워크플로우 테스트 (검색 → 문서 생성 → 저장)
  - 오류 시나리오 테스트
  - MCP 프로토콜 통신 테스트
  - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.2_
