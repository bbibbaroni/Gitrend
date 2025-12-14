"""Unit tests for configuration module"""
import pytest
import os
from src.config import Config, ConfigurationError


def test_config_validation_missing_github_token(monkeypatch):
    """Test that missing GITHUB_TOKEN raises ConfigurationError"""
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("LLM_API_KEY", "test_key")
    
    with pytest.raises(ConfigurationError) as exc_info:
        Config.load_from_env()
    
    assert "GITHUB_TOKEN" in str(exc_info.value)


def test_config_validation_missing_llm_api_key(monkeypatch):
    """Test that missing LLM_API_KEY raises ConfigurationError"""
    monkeypatch.setenv("GITHUB_TOKEN", "test_token")
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    
    with pytest.raises(ConfigurationError) as exc_info:
        Config.load_from_env()
    
    assert "LLM_API_KEY" in str(exc_info.value)


def test_config_validation_success(monkeypatch):
    """Test that valid configuration loads successfully"""
    monkeypatch.setenv("GITHUB_TOKEN", "test_token")
    monkeypatch.setenv("LLM_API_KEY", "test_key")
    
    config = Config.load_from_env()
    
    assert config.GITHUB_TOKEN == "test_token"
    assert config.LLM_API_KEY == "test_key"
    assert config.LLM_MODEL == "gpt-4"
    assert config.OUTPUT_DIR == "./docs"
    assert config.PORT == 8000


def test_config_custom_values(monkeypatch):
    """Test that custom configuration values are loaded"""
    monkeypatch.setenv("GITHUB_TOKEN", "test_token")
    monkeypatch.setenv("LLM_API_KEY", "test_key")
    monkeypatch.setenv("LLM_MODEL", "gpt-3.5-turbo")
    monkeypatch.setenv("OUTPUT_DIR", "./custom_docs")
    monkeypatch.setenv("PORT", "9000")
    
    config = Config.load_from_env()
    
    assert config.LLM_MODEL == "gpt-3.5-turbo"
    assert config.OUTPUT_DIR == "./custom_docs"
    assert config.PORT == 9000
