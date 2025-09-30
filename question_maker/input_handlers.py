"""
Input handlers for various text sources
"""

import os
from typing import Optional
from pathlib import Path
import requests


class TextSource:
    """Base class for text sources"""
    
    def read(self) -> str:
        """Read and return text content"""
        raise NotImplementedError("Subclasses must implement read()")
    
    def get_source_info(self) -> str:
        """Return information about the source"""
        raise NotImplementedError("Subclasses must implement get_source_info()")


class FileSource(TextSource):
    """Read text from a file"""
    
    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        self.file_path = Path(file_path)
        self.encoding = encoding
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
    
    def read(self) -> str:
        """Read text from file"""
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            return f.read()
    
    def get_source_info(self) -> str:
        """Return file path as source info"""
        return str(self.file_path.absolute())


class URLSource(TextSource):
    """Read text from a URL"""
    
    def __init__(self, url: str, timeout: int = 30):
        self.url = url
        self.timeout = timeout
    
    def read(self) -> str:
        """Fetch text from URL"""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch URL {self.url}: {str(e)}")
    
    def get_source_info(self) -> str:
        """Return URL as source info"""
        return self.url


class StringSource(TextSource):
    """Read text from a string"""
    
    def __init__(self, text: str):
        self.text = text
    
    def read(self) -> str:
        """Return the string content"""
        return self.text
    
    def get_source_info(self) -> str:
        """Return 'string' as source info"""
        return "string"


def create_source(input_data: str, source_type: Optional[str] = None) -> TextSource:
    """
    Factory function to create appropriate text source
    
    Args:
        input_data: File path, URL, or text string
        source_type: Optional type hint ('file', 'url', 'string')
    
    Returns:
        Appropriate TextSource instance
    """
    if source_type == 'file' or (source_type is None and os.path.exists(input_data)):
        return FileSource(input_data)
    elif source_type == 'url' or (source_type is None and input_data.startswith(('http://', 'https://'))):
        return URLSource(input_data)
    else:
        return StringSource(input_data)
