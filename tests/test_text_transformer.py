"""Tests for text transformer"""

import pytest
import tempfile
import os
from question_maker import TextTransformer
from question_maker.text_transformer import (
    basic_stats_processor, 
    extract_sentences, 
    extract_paragraphs
)
from question_maker.data_models import StructuredData


def test_text_transformer_creation():
    """Test creating a TextTransformer"""
    transformer = TextTransformer()
    assert transformer is not None
    assert transformer.processors == []


def test_add_processor():
    """Test adding a processor to TextTransformer"""
    transformer = TextTransformer()
    
    def dummy_processor(text):
        return {"test": "value"}
    
    transformer.add_processor(dummy_processor)
    assert len(transformer.processors) == 1


def test_transform_string():
    """Test transforming a simple string"""
    transformer = TextTransformer()
    transformer.add_processor(basic_stats_processor)
    
    text = "Hello world! This is a test."
    result = transformer.transform(text, source_type='string')
    
    assert isinstance(result, StructuredData)
    assert result.source == "string"
    assert result.content == text
    assert 'word_count' in result.extracted_data
    assert result.extracted_data['word_count'] == 6


def test_transform_file():
    """Test transforming from a file"""
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Test file content with multiple words.")
        temp_file = f.name
    
    try:
        transformer = TextTransformer()
        transformer.add_processor(basic_stats_processor)
        
        result = transformer.transform(temp_file, source_type='file')
        
        assert isinstance(result, StructuredData)
        assert temp_file in result.source
        assert 'word_count' in result.extracted_data
        assert result.extracted_data['word_count'] == 6
    finally:
        os.unlink(temp_file)


def test_basic_stats_processor():
    """Test basic_stats_processor"""
    text = "Hello world! This is a test with multiple words."
    result = basic_stats_processor(text)
    
    assert 'word_count' in result
    assert 'line_count' in result
    assert 'char_count' in result
    assert 'avg_word_length' in result
    assert result['word_count'] == 9
    assert result['char_count'] == len(text)


def test_extract_sentences():
    """Test extract_sentences processor"""
    text = "First sentence. Second sentence! Third sentence?"
    result = extract_sentences(text)
    
    assert 'sentences' in result
    assert 'sentence_count' in result
    assert result['sentence_count'] == 3
    assert len(result['sentences']) == 3


def test_extract_paragraphs():
    """Test extract_paragraphs processor"""
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
    result = extract_paragraphs(text)
    
    assert 'paragraphs' in result
    assert 'paragraph_count' in result
    assert result['paragraph_count'] == 3
    assert len(result['paragraphs']) == 3


def test_multiple_processors():
    """Test using multiple processors together"""
    transformer = TextTransformer()
    transformer.add_processor(basic_stats_processor)
    transformer.add_processor(extract_sentences)
    
    text = "Hello! This is a test. How are you?"
    result = transformer.transform(text, source_type='string')
    
    assert 'word_count' in result.extracted_data
    assert 'sentences' in result.extracted_data
    assert 'sentence_count' in result.extracted_data


def test_custom_processor():
    """Test adding a custom processor"""
    transformer = TextTransformer()
    
    def count_exclamations(text):
        return {'exclamation_count': text.count('!')}
    
    transformer.add_processor(count_exclamations)
    
    text = "Hello! World! Test!"
    result = transformer.transform(text, source_type='string')
    
    assert 'exclamation_count' in result.extracted_data
    assert result.extracted_data['exclamation_count'] == 3


def test_transform_batch():
    """Test batch transformation"""
    transformer = TextTransformer()
    transformer.add_processor(basic_stats_processor)
    
    inputs = [
        ("First text", "string"),
        ("Second text with more words", "string"),
    ]
    
    results = transformer.transform_batch(inputs)
    
    assert len(results) == 2
    assert all(isinstance(r, StructuredData) for r in results)
    assert results[0].extracted_data['word_count'] == 2
    assert results[1].extracted_data['word_count'] == 5


def test_metadata_added():
    """Test that metadata is added to results"""
    transformer = TextTransformer()
    transformer.add_processor(basic_stats_processor)
    
    result = transformer.transform("Test", source_type='string')
    
    assert 'text_length' in result.metadata
    assert 'processor_count' in result.metadata
    assert result.metadata['text_length'] == 4
    assert result.metadata['processor_count'] == 1
