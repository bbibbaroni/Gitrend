"""LLM API client"""
import asyncio
from typing import Optional
from openai import AsyncOpenAI, AuthenticationError, RateLimitError, APIError


class LLMAPIError(Exception):
    """LLM API error"""
    def __init__(self, message: str, is_auth_error: bool = False):
        self.message = message
        self.is_auth_error = is_auth_error
        super().__init__(self.message)


class LLMClient:
    """Client for LLM API interactions"""
    
    MAX_RETRIES = 2
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def generate_completion(
        self, 
        prompt: str, 
        retry_count: int = 0
    ) -> str:
        """Generate completion from LLM"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            return content or ""
            
        except AuthenticationError:
            raise LLMAPIError(
                "LLM API authentication failed. Please check your API key.",
                is_auth_error=True
            )
        except RateLimitError:
            if retry_count < self.MAX_RETRIES:
                await asyncio.sleep(2 ** retry_count)
                return await self.generate_completion(prompt, retry_count + 1)
            raise LLMAPIError("LLM API rate limit exceeded after retries.")
        except APIError as e:
            if retry_count < self.MAX_RETRIES:
                await asyncio.sleep(2 ** retry_count)
                return await self.generate_completion(prompt, retry_count + 1)
            raise LLMAPIError(f"LLM API error: {str(e)}")
        except Exception as e:
            raise LLMAPIError(f"Unexpected LLM error: {str(e)}")
