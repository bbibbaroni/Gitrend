"""Document generation service"""
import os
import re
import shutil
from datetime import datetime
from typing import Dict, Any


class DocumentGenerationError(Exception):
    """Document generation error"""
    pass


class DocumentGenerator:
    """Service for generating and saving markdown documents"""
    
    def __init__(self, output_dir: str = "./docs"):
        self.output_dir = output_dir
    
    def generate_markdown(self, content: str, metadata: Dict[str, Any]) -> str:
        """Generate markdown document with metadata"""
        # Content is already in markdown format from LLM
        return content
    
    def _sanitize_filename(self, name: str) -> str:
        """Generate valid filename from library name"""
        # Replace spaces and slashes with hyphens first
        sanitized = name.replace(' ', '-').replace('/', '-')
        # Remove invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '', sanitized)
        # Remove multiple consecutive hyphens
        sanitized = re.sub(r'-+', '-', sanitized)
        # Remove leading/trailing hyphens
        sanitized = sanitized.strip('-')
        # Ensure it's not empty
        if not sanitized:
            sanitized = "document"
        return sanitized
    
    def _ensure_directory_exists(self, directory: str) -> None:
        """Ensure output directory exists"""
        try:
            os.makedirs(directory, exist_ok=True)
        except Exception as e:
            raise DocumentGenerationError(
                f"Failed to create directory {directory}: {str(e)}"
            )
    
    def _backup_existing_file(self, filepath: str) -> None:
        """Create backup of existing file"""
        if os.path.exists(filepath):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{filepath}.backup_{timestamp}"
            try:
                shutil.copy2(filepath, backup_path)
            except Exception as e:
                raise DocumentGenerationError(
                    f"Failed to create backup: {str(e)}"
                )
    
    def save_document(
        self, 
        filename: str, 
        content: str, 
        backup: bool = True
    ) -> str:
        """Save document to file system"""
        try:
            # Ensure directory exists
            self._ensure_directory_exists(self.output_dir)
            
            # Sanitize filename if needed
            if not filename:
                filename = "document"
            
            # Ensure .md extension
            if not filename.endswith('.md'):
                filename = f"{filename}.md"
            
            # Full file path
            filepath = os.path.join(self.output_dir, filename)
            
            # Backup existing file if requested
            if backup and os.path.exists(filepath):
                self._backup_existing_file(filepath)
            
            # Write content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return filepath
            
        except DocumentGenerationError:
            raise
        except Exception as e:
            raise DocumentGenerationError(
                f"Failed to save document: {str(e)}"
            )
    
    def generate_filename(self, library_name: str) -> str:
        """Generate filename from library name"""
        sanitized = self._sanitize_filename(library_name)
        return f"{sanitized}.md"
