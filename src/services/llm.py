"""LLM service layer"""
from src.clients.llm_client import LLMClient, LLMAPIError
from src.models import RepositoryDetails


class LLMService:
    """Service for LLM operations"""
    
    PROMPT_TEMPLATE = """You are a technical documentation expert. Based on the following GitHub repository information, create a comprehensive usage guide in Korean.

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

Make sure the guide is practical, clear, and includes code examples where appropriate."""

    FALLBACK_TEMPLATE = """# {repo_name}

## 라이브러리 개요

{description}

**주요 정보:**
- 언어: {language}
- Stars: {stars}
- 저장소: {url}

## 설치 방법

저장소를 방문하여 설치 방법을 확인하세요: {url}

## 기본 사용 예제

자세한 사용 예제는 README를 참조하세요.

## 주요 기능

이 라이브러리의 주요 기능은 README 문서에서 확인할 수 있습니다.

## 추가 리소스

- GitHub 저장소: {url}
- README: 저장소에서 확인
"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = LLMClient(api_key, model)
    
    async def generate_usage_guide(self, repo_info: RepositoryDetails) -> str:
        """Generate usage guide using LLM"""
        try:
            # Prepare prompt
            prompt = self.PROMPT_TEMPLATE.format(
                repo_name=repo_info.repository.full_name,
                description=repo_info.repository.description or "No description available",
                language=repo_info.repository.language or "Unknown",
                stars=repo_info.repository.stars,
                readme=repo_info.readme or "No README available"
            )
            
            # Generate with LLM
            result = await self.client.generate_completion(prompt)
            return result
            
        except LLMAPIError:
            # Fallback to template
            return self._generate_fallback_template(repo_info)
    
    def _generate_fallback_template(self, repo_info: RepositoryDetails) -> str:
        """Generate fallback template when LLM fails"""
        return self.FALLBACK_TEMPLATE.format(
            repo_name=repo_info.repository.full_name,
            description=repo_info.repository.description or "설명 없음",
            language=repo_info.repository.language or "알 수 없음",
            stars=repo_info.repository.stars,
            url=repo_info.repository.url
        )
