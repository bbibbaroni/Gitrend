"""GitHub service layer"""
from typing import List
from src.clients.github_client import GitHubClient
from src.models import Repository, RepositoryDetails


class GitHubService:
    """Service for GitHub operations"""
    
    def __init__(self, api_token: str):
        self.client = GitHubClient(api_token)
    
    async def search_repositories(self, query: str, limit: int = 10) -> List[Repository]:
        """Search repositories and return sorted by stars"""
        results = await self.client.search_repositories(query, limit)
        
        # Parse results into Repository models
        repositories = []
        for item in results:
            repo = Repository(
                name=item.get("name", ""),
                full_name=item.get("full_name", ""),
                description=item.get("description"),
                stargazers_count=item.get("stargazers_count", 0),
                forks_count=item.get("forks_count", 0),
                language=item.get("language"),
                html_url=item.get("html_url", "")
            )
            repositories.append(repo)
        
        # Sort by stars (descending)
        repositories.sort(key=lambda r: r.stars, reverse=True)
        
        return repositories
    
    async def get_repository_details(self, owner: str, repo: str) -> RepositoryDetails:
        """Get detailed repository information"""
        repo_data = await self.client.get_repository(owner, repo)
        readme = await self.client.get_readme(owner, repo)
        
        # Create Repository model
        repository = Repository(
            name=repo_data.get("name", ""),
            full_name=repo_data.get("full_name", ""),
            description=repo_data.get("description"),
            stargazers_count=repo_data.get("stargazers_count", 0),
            forks_count=repo_data.get("forks_count", 0),
            language=repo_data.get("language"),
            html_url=repo_data.get("html_url", "")
        )
        
        # Extract license info
        license_info = repo_data.get("license")
        license_name = license_info.get("name") if license_info else None
        
        # Create RepositoryDetails
        details = RepositoryDetails(
            repository=repository,
            readme=readme,
            topics=repo_data.get("topics", []),
            license=license_name,
            homepage=repo_data.get("homepage"),
            created_at=repo_data.get("created_at", ""),
            updated_at=repo_data.get("updated_at", "")
        )
        
        return details
    
    async def get_readme(self, owner: str, repo: str) -> str:
        """Get repository README"""
        readme = await self.client.get_readme(owner, repo)
        return readme or ""
