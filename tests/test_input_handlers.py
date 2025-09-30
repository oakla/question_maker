"""Tests for input handlers"""

import pytest
import tempfile
import os
from pathlib import Path
from question_maker.input_handlers import (
    FileSource, StringSource, URLSource, create_source
)


def test_string_source():
    """Test StringSource"""
    text = "Hello, world!"
    source = StringSource(text)
    
    assert source.read() == text
    assert source.get_source_info() == "string"


def test_file_source():
    """Test FileSource"""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Test content from file")
        temp_file = f.name
    
    try:
        source = FileSource(temp_file)
        content = source.read()
        
        assert content == "Test content from file"
        assert temp_file in source.get_source_info()
    finally:
        os.unlink(temp_file)


def test_file_source_not_found():
    """Test FileSource with non-existent file"""
    with pytest.raises(FileNotFoundError):
        FileSource("/nonexistent/file.txt")


def test_create_source_string():
    """Test create_source with string"""
    source = create_source("Simple text", source_type='string')
    assert isinstance(source, StringSource)
    assert source.read() == "Simple text"


def test_create_source_file():
    """Test create_source with file"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("File content")
        temp_file = f.name
    
    try:
        source = create_source(temp_file, source_type='file')
        assert isinstance(source, FileSource)
        assert source.read() == "File content"
    finally:
        os.unlink(temp_file)


def test_create_source_auto_detect_file():
    """Test create_source auto-detection for file"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Auto-detected file")
        temp_file = f.name
    
    try:
        # Should auto-detect as file since it exists
        source = create_source(temp_file)
        assert isinstance(source, FileSource)
    finally:
        os.unlink(temp_file)


def test_create_source_auto_detect_url():
    """Test create_source auto-detection for URL"""
    source = create_source("https://example.com/page")
    assert isinstance(source, URLSource)
    
    source = create_source("http://example.com/page")
    assert isinstance(source, URLSource)


def test_create_source_auto_detect_string():
    """Test create_source auto-detection for string"""
    # Non-existent file path should be treated as string
    source = create_source("/nonexistent/path.txt")
    assert isinstance(source, StringSource)
