"""MCP tool definitions"""
from typing import List
from src.models import ToolDefinition


def get_tool_definitions() -> List[ToolDefinition]:
    """Get list of available MCP tools"""
    return [
        ToolDefinition(
            name="search_github_library",
            description="Search for GitHub repositories by library name. Returns a list of repositories sorted by stars.",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Library name or search query"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 10)",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        ),
        ToolDefinition(
            name="get_repository_details",
            description="Get detailed information about a specific GitHub repository including README content.",
            input_schema={
                "type": "object",
                "properties": {
                    "owner": {
                        "type": "string",
                        "description": "Repository owner username"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name"
                    }
                },
                "required": ["owner", "repo"]
            }
        ),
        ToolDefinition(
            name="generate_usage_guide",
            description="Generate a comprehensive usage guide for a GitHub library using LLM and save it as a markdown file.",
            input_schema={
                "type": "object",
                "properties": {
                    "owner": {
                        "type": "string",
                        "description": "Repository owner username"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optional custom output path for the generated document",
                        "default": None
                    }
                },
                "required": ["owner", "repo"]
            }
        )
    ]


def list_tools() -> dict:
    """Return tools in MCP format"""
    tools = get_tool_definitions()
    return {
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            }
            for tool in tools
        ]
    }
