"""Unit tests for document generator"""
import pytest
import os
import tempfile
import shutil
from src.services.document import DocumentGenerator, DocumentGenerationError


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests"""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


def test_sanitize_filename():
    """Test filename sanitization"""
    generator = DocumentGenerator()
    
    assert generator._sanitize_filename("simple-name") == "simple-name"
    assert generator._sanitize_filename("name with spaces") == "name-with-spaces"
    assert generator._sanitize_filename("owner/repo") == "owner-repo"
    assert generator._sanitize_filename("name<>:") == "name"
    assert generator._sanitize_filename("") == "document"


def test_generate_filename():
    """Test filename generation from library name"""
    generator = DocumentGenerator()
    
    assert generator.generate_filename("fastapi") == "fastapi.md"
    assert generator.generate_filename("tiangolo/fastapi") == "tiangolo-fastapi.md"
    assert generator.generate_filename("my library") == "my-library.md"


def test_save_document(temp_dir):
    """Test document saving"""
    generator = DocumentGenerator(temp_dir)
    content = "# Test Document\n\nThis is a test."
    
    filepath = generator.save_document("test.md", content, backup=False)
    
    assert os.path.exists(filepath)
    assert filepath == os.path.join(temp_dir, "test.md")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        assert f.read() == content


def test_save_document_with_backup(temp_dir):
    """Test document saving with backup"""
    generator = DocumentGenerator(temp_dir)
    filepath = os.path.join(temp_dir, "test.md")
    
    # Create initial file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("Original content")
    
    # Save new content with backup
    new_content = "New content"
    generator.save_document("test.md", new_content, backup=True)
    
    # Check new content
    with open(filepath, 'r', encoding='utf-8') as f:
        assert f.read() == new_content
    
    # Check backup exists
    backup_files = [f for f in os.listdir(temp_dir) if f.startswith("test.md.backup_")]
    assert len(backup_files) == 1


def test_save_document_adds_md_extension(temp_dir):
    """Test that .md extension is added if missing"""
    generator = DocumentGenerator(temp_dir)
    content = "# Test"
    
    filepath = generator.save_document("test", content, backup=False)
    
    assert filepath.endswith(".md")
    assert os.path.exists(filepath)


def test_ensure_directory_exists(temp_dir):
    """Test directory creation"""
    nested_dir = os.path.join(temp_dir, "nested", "path")
    generator = DocumentGenerator(nested_dir)
    
    generator._ensure_directory_exists(nested_dir)
    
    assert os.path.exists(nested_dir)
    assert os.path.isdir(nested_dir)
