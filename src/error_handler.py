"""Global error handling and logging"""
import logging
import sys
from typing import Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.clients.github_client import GitHubAPIError
from src.clients.llm_client import LLMAPIError
from src.services.document import DocumentGenerationError
from src.config import ConfigurationError


# Configure logging
def setup_logging(log_level: str = "INFO") -> None:
    """Setup application logging"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('mcp_server.log')
        ]
    )


logger = logging.getLogger(__name__)


def create_error_response(
    code: str,
    message: str,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    details: Optional[dict] = None
) -> JSONResponse:
    """Create standardized error response"""
    error_content = {
        "error": {
            "code": code,
            "message": message
        }
    }
    
    if details:
        error_content["error"]["details"] = details
    
    logger.error(f"Error {code}: {message}", extra={"details": details})
    
    return JSONResponse(
        status_code=status_code,
        content=error_content
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for FastAPI"""
    
    if isinstance(exc, GitHubAPIError):
        return create_error_response(
            code="GITHUB_API_ERROR",
            message=exc.message,
            status_code=exc.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"status_code": exc.status_code}
        )
    
    elif isinstance(exc, LLMAPIError):
        status_code = status.HTTP_401_UNAUTHORIZED if exc.is_auth_error else status.HTTP_500_INTERNAL_SERVER_ERROR
        return create_error_response(
            code="LLM_API_ERROR",
            message=exc.message,
            status_code=status_code
        )
    
    elif isinstance(exc, DocumentGenerationError):
        return create_error_response(
            code="DOCUMENT_ERROR",
            message=exc.args[0] if exc.args else "Document generation failed",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    elif isinstance(exc, ConfigurationError):
        return create_error_response(
            code="CONFIGURATION_ERROR",
            message=exc.args[0] if exc.args else "Configuration error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    elif isinstance(exc, ValueError):
        return create_error_response(
            code="VALIDATION_ERROR",
            message=str(exc),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    else:
        # Log unexpected errors
        logger.exception("Unexpected error occurred", exc_info=exc)
        return create_error_response(
            code="INTERNAL_ERROR",
            message="An unexpected error occurred",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"error_type": type(exc).__name__}
        )


def log_startup_error(error: Exception) -> None:
    """Log server startup errors"""
    logger.error(
        f"Server startup failed: {str(error)}",
        exc_info=error
    )
