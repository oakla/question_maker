"""Tests for data models"""

import pytest
from question_maker.data_models import StructuredData, TextSegment


def test_structured_data_creation():
    """Test basic creation of StructuredData"""
    data = StructuredData(
        source="test.txt",
        content="Test content"
    )
    
    assert data.source == "test.txt"
    assert data.content == "Test content"
    assert isinstance(data.extracted_data, dict)
    assert isinstance(data.metadata, dict)
    assert data.timestamp is not None


def test_structured_data_add_field():
    """Test adding fields to StructuredData"""
    data = StructuredData(source="test", content="content")
    
    data.add_field("key1", "value1")
    data.add_field("key2", 123)
    
    assert data.get_field("key1") == "value1"
    assert data.get_field("key2") == 123
    assert data.get_field("nonexistent", "default") == "default"


def test_structured_data_to_dict():
    """Test converting StructuredData to dictionary"""
    data = StructuredData(
        source="test.txt",
        content="Test content"
    )
    data.add_field("test_field", "test_value")
    
    result = data.to_dict()
    
    assert isinstance(result, dict)
    assert result["source"] == "test.txt"
    assert result["content"] == "Test content"
    assert result["extracted_data"]["test_field"] == "test_value"


def test_text_segment_creation():
    """Test TextSegment creation"""
    segment = TextSegment(
        text="Hello, world!",
        start_position=0,
        end_position=13,
        category="greeting"
    )
    
    assert segment.text == "Hello, world!"
    assert segment.start_position == 0
    assert segment.end_position == 13
    assert segment.category == "greeting"


def test_text_segment_to_dict():
    """Test converting TextSegment to dictionary"""
    segment = TextSegment(text="Test", start_position=0, end_position=4)
    result = segment.to_dict()
    
    assert isinstance(result, dict)
    assert result["text"] == "Test"
    assert result["start_position"] == 0
    assert result["end_position"] == 4
