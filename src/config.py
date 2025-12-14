"""Configuration management module"""
import os
from typing import Optional
from dotenv import load_dotenv


class ConfigurationError(Exception):
    """Configuration validation error"""
    pass


class Config:
    """Application configuration loaded from environment variables"""
    
    def __init__(self):
        load_dotenv()
        
        self.GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
        self.LLM_API_KEY: Optional[str] = os.getenv("LLM_API_KEY")
        self.LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4")
        self.OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "./docs")
        self.PORT: int = int(os.getenv("PORT", "8000"))
        
    @classmethod
    def load_from_env(cls) -> "Config":
        """Load configuration from environment variables"""
        config = cls()
        config.validate()
        return config
    
    def validate(self) -> None:
        """Validate required environment variables"""
        missing = []
        
        if not self.GITHUB_TOKEN:
            missing.append("GITHUB_TOKEN")
        if not self.LLM_API_KEY:
            missing.append("LLM_API_KEY")
            
        if missing:
            raise ConfigurationError(
                f"Missing required environment variables: {', '.join(missing)}. "
                f"Please set them in your .env file."
            )
