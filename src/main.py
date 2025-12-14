"""Main entry point for the MCP server"""
import uvicorn
from src.config import Config, ConfigurationError
from src.error_handler import log_startup_error


def main():
    """Start the MCP server"""
    try:
        # Load configuration
        config = Config.load_from_env()
        
        # Run server
        uvicorn.run(
            "src.app:app",
            host="0.0.0.0",
            port=config.PORT,
            log_level="info",
            reload=False
        )
        
    except ConfigurationError as e:
        log_startup_error(e)
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure your .env file contains:")
        print("  - GITHUB_TOKEN")
        print("  - LLM_API_KEY")
        print("\nSee .env.example for reference.")
        exit(1)
        
    except Exception as e:
        log_startup_error(e)
        print(f"\n❌ Server startup failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
