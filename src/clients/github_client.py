"""GitHub API client"""
import asyncio
import base64
from typing import List, Optional, Dict, Any
import httpx
from src.models import Repository, RepositoryDetails


class GitHubAPIError(Exception):
    """GitHub API error"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class GitHubClient:
    """Client for GitHub API interactions"""
    
    BASE_URL = "https://api.github.com"
    MAX_RETRIES = 3
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {
            "Authorization": f"token {api_token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=params,
                    timeout=30.0
                )
                
                if response.status_code == 401:
                    raise GitHubAPIError(
                        "GitHub API authentication failed. Please check your token.",
                        status_code=401
                    )
                elif response.status_code == 403:
                    raise GitHubAPIError(
                        "GitHub API rate limit exceeded.",
                        status_code=403
                    )
                elif response.status_code == 404:
                    raise GitHubAPIError(
                        "Repository not found.",
                        status_code=404
                    )
                elif response.status_code >= 400:
                    raise GitHubAPIError(
                        f"GitHub API error: {response.text}",
                        status_code=response.status_code
                    )
                
                return response.json()
                
        except httpx.TimeoutException:
            if retry_count < self.MAX_RETRIES:
                await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                return await self._make_request(method, endpoint, params, retry_count + 1)
            raise GitHubAPIError("GitHub API request timed out after retries.")
        except httpx.RequestError as e:
            if retry_count < self.MAX_RETRIES:
                await asyncio.sleep(2 ** retry_count)
                return await self._make_request(method, endpoint, params, retry_count + 1)
            raise GitHubAPIError(f"GitHub API request failed: {str(e)}")
    
    async def search_repositories(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for repositories"""
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": limit
        }
        
        result = await self._make_request("GET", "/search/repositories", params)
        return result.get("items", [])
    
    async def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository details"""
        return await self._make_request("GET", f"/repos/{owner}/{repo}")
    
    async def get_readme(self, owner: str, repo: str) -> Optional[str]:
        """Get repository README content"""
        try:
            result = await self._make_request("GET", f"/repos/{owner}/{repo}/readme")
            
            # Decode base64 content
            content = result.get("content", "")
            if content:
                decoded = base64.b64decode(content).decode("utf-8")
                return decoded
            return None
            
        except GitHubAPIError as e:
            if e.status_code == 404:
                return None
            raise
