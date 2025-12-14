"""FastAPI application"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.config import Config
from src.models import MCPRequest, MCPResponse
from src.services.github import GitHubService
from src.services.llm import LLMService
from src.services.document import DocumentGenerator
from src.mcp.handler import MCPHandler
from src.error_handler import global_exception_handler, setup_logging, log_startup_error
import logging


logger = logging.getLogger(__name__)


# Global services
github_service: GitHubService = None
llm_service: LLMService = None
document_generator: DocumentGenerator = None
mcp_handler: MCPHandler = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for FastAPI app"""
    global github_service, llm_service, document_generator, mcp_handler
    
    try:
        # Setup logging
        setup_logging()
        logger.info("Starting GitHub Library Search MCP Server...")
        
        # Load configuration
        config = Config.load_from_env()
        logger.info("Configuration loaded successfully")
        
        # Initialize services
        github_service = GitHubService(config.GITHUB_TOKEN)
        llm_service = LLMService(config.LLM_API_KEY, config.LLM_MODEL)
        document_generator = DocumentGenerator(config.OUTPUT_DIR)
        
        # Initialize MCP handler
        mcp_handler = MCPHandler(github_service, llm_service, document_generator)
        
        logger.info(f"Server started successfully on port {config.PORT}")
        
        yield
        
        # Cleanup
        logger.info("Shutting down server...")
        
    except Exception as e:
        log_startup_error(e)
        raise


# Create FastAPI app
app = FastAPI(
    title="GitHub Library Search MCP",
    description="MCP server for searching GitHub libraries and generating usage guides",
    version="0.1.0",
    lifespan=lifespan
)


# Register global exception handler
app.add_exception_handler(Exception, global_exception_handler)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "github-library-search-mcp"}


@app.post("/mcp", response_model=MCPResponse)
async def handle_mcp_request(request: MCPRequest) -> MCPResponse:
    """Handle MCP protocol requests"""
    return await mcp_handler.handle_request(request)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "GitHub Library Search MCP",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "mcp": "/mcp"
        }
    }
