"""MCP protocol handler"""
from typing import Dict, Any, Optional
from src.models import MCPRequest, MCPResponse, ToolResult
from src.services.github import GitHubService
from src.services.llm import LLMService
from src.services.document import DocumentGenerator
from src.mcp.tools import list_tools
from src.clients.github_client import GitHubAPIError
from src.clients.llm_client import LLMAPIError


class MCPHandler:
    """Handler for MCP protocol requests"""
    
    def __init__(
        self,
        github_service: GitHubService,
        llm_service: LLMService,
        document_generator: DocumentGenerator
    ):
        self.github_service = github_service
        self.llm_service = llm_service
        self.document_generator = document_generator
    
    def _create_error_response(self, code: str, message: str, details: Optional[Dict] = None) -> MCPResponse:
        """Create error response"""
        error = {
            "code": code,
            "message": message
        }
        if details:
            error["details"] = details
        
        return MCPResponse(error=error)
    
    def _create_success_response(self, content: Any) -> MCPResponse:
        """Create success response"""
        return MCPResponse(result={"content": content})
    
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle MCP request and route to appropriate handler"""
        try:
            method = request.method
            params = request.params
            
            if method == "tools/list":
                return self._create_success_response(list_tools())
            
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if not tool_name:
                    return self._create_error_response(
                        "INVALID_PARAMS",
                        "Tool name is required"
                    )
                
                return await self._call_tool(tool_name, arguments)
            
            else:
                return self._create_error_response(
                    "METHOD_NOT_FOUND",
                    f"Unknown method: {method}"
                )
                
        except Exception as e:
            return self._create_error_response(
                "INTERNAL_ERROR",
                f"Internal error: {str(e)}"
            )
    
    async def _call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> MCPResponse:
        """Call specific tool"""
        try:
            if tool_name == "search_github_library":
                return await self._search_github_library(arguments)
            
            elif tool_name == "get_repository_details":
                return await self._get_repository_details(arguments)
            
            elif tool_name == "generate_usage_guide":
                return await self._generate_usage_guide(arguments)
            
            else:
                return self._create_error_response(
                    "TOOL_NOT_FOUND",
                    f"Unknown tool: {tool_name}"
                )
                
        except GitHubAPIError as e:
            return self._create_error_response(
                "GITHUB_API_ERROR",
                e.message,
                {"status_code": e.status_code}
            )
        except LLMAPIError as e:
            return self._create_error_response(
                "LLM_API_ERROR",
                e.message
            )
        except Exception as e:
            return self._create_error_response(
                "TOOL_EXECUTION_ERROR",
                f"Tool execution failed: {str(e)}"
            )
    
    async def _search_github_library(self, arguments: Dict[str, Any]) -> MCPResponse:
        """Handle search_github_library tool"""
        query = arguments.get("query")
        if not query:
            return self._create_error_response(
                "MISSING_PARAMETER",
                "Required parameter 'query' is missing"
            )
        
        limit = arguments.get("limit", 10)
        
        repositories = await self.github_service.search_repositories(query, limit)
        
        result = [
            {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "stars": repo.stars,
                "forks": repo.forks,
                "language": repo.language,
                "url": repo.url
            }
            for repo in repositories
        ]
        
        return self._create_success_response(result)
    
    async def _get_repository_details(self, arguments: Dict[str, Any]) -> MCPResponse:
        """Handle get_repository_details tool"""
        owner = arguments.get("owner")
        repo = arguments.get("repo")
        
        if not owner:
            return self._create_error_response(
                "MISSING_PARAMETER",
                "Required parameter 'owner' is missing"
            )
        if not repo:
            return self._create_error_response(
                "MISSING_PARAMETER",
                "Required parameter 'repo' is missing"
            )
        
        details = await self.github_service.get_repository_details(owner, repo)
        
        result = {
            "repository": {
                "name": details.repository.name,
                "full_name": details.repository.full_name,
                "description": details.repository.description,
                "stars": details.repository.stars,
                "forks": details.repository.forks,
                "language": details.repository.language,
                "url": details.repository.url
            },
            "readme": details.readme,
            "topics": details.topics,
            "license": details.license,
            "homepage": details.homepage,
            "created_at": details.created_at,
            "updated_at": details.updated_at
        }
        
        return self._create_success_response(result)
    
    async def _generate_usage_guide(self, arguments: Dict[str, Any]) -> MCPResponse:
        """Handle generate_usage_guide tool"""
        owner = arguments.get("owner")
        repo = arguments.get("repo")
        output_path = arguments.get("output_path")
        
        if not owner:
            return self._create_error_response(
                "MISSING_PARAMETER",
                "Required parameter 'owner' is missing"
            )
        if not repo:
            return self._create_error_response(
                "MISSING_PARAMETER",
                "Required parameter 'repo' is missing"
            )
        
        # Get repository details
        details = await self.github_service.get_repository_details(owner, repo)
        
        # Generate usage guide with LLM
        guide_content = await self.llm_service.generate_usage_guide(details)
        
        # Generate filename
        if not output_path:
            output_path = self.document_generator.generate_filename(details.repository.full_name)
        
        # Save document
        filepath = self.document_generator.save_document(output_path, guide_content)
        
        result = {
            "message": "Usage guide generated successfully",
            "filepath": filepath,
            "repository": details.repository.full_name
        }
        
        return self._create_success_response(result)
