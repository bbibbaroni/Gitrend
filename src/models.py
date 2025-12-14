"""Pydantic data models"""
from typing import Optional, List, Any
from pydantic import BaseModel, Field


class Repository(BaseModel):
    """GitHub repository model"""
    name: str
    full_name: str
    description: Optional[str] = None
    stars: int = Field(alias="stargazers_count", default=0)
    forks: int = Field(alias="forks_count", default=0)
    language: Optional[str] = None
    url: str = Field(alias="html_url")
    
    class Config:
        populate_by_name = True


class RepositoryDetails(BaseModel):
    """Detailed repository information"""
    repository: Repository
    readme: Optional[str] = None
    topics: List[str] = Field(default_factory=list)
    license: Optional[str] = None
    homepage: Optional[str] = None
    created_at: str
    updated_at: str


class ToolDefinition(BaseModel):
    """MCP tool definition"""
    name: str
    description: str
    input_schema: dict


class ToolResult(BaseModel):
    """MCP tool execution result"""
    content: List[dict]
    isError: bool = False


class MCPRequest(BaseModel):
    """MCP protocol request"""
    method: str
    params: dict = Field(default_factory=dict)


class MCPResponse(BaseModel):
    """MCP protocol response"""
    result: Optional[dict] = None
    error: Optional[dict] = None
