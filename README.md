# question_maker

A Python project for transforming text from various sources into structured data.

## Features

- **Multiple Input Sources**: Read text from files, URLs, or strings
- **Flexible Processing**: Add custom processors to extract specific information
- **Built-in Processors**: Extract statistics, sentences, paragraphs, and more
- **Structured Output**: Convert unstructured text into organized, structured data
- **Easy to Extend**: Simple API for adding custom text processing logic

## Installation

```bash
pip install -e .
```

For development:
```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from question_maker import TextTransformer
from question_maker.text_transformer import basic_stats_processor, extract_sentences

# Create a transformer
transformer = TextTransformer()

# Add processors
transformer.add_processor(basic_stats_processor)
transformer.add_processor(extract_sentences)

# Transform text from any source
text = "Hello, world! This is a test. It works great!"
result = transformer.transform(text, source_type='string')

# Access structured data
print(f"Word count: {result.extracted_data['word_count']}")
print(f"Sentences: {result.extracted_data['sentences']}")
```

## Usage Examples

### Transform from Different Sources

```python
# From a string
result = transformer.transform("Your text here", source_type='string')

# From a file
result = transformer.transform("path/to/file.txt", source_type='file')

# From a URL
result = transformer.transform("https://example.com/text", source_type='url')

# Auto-detection (based on input format)
result = transformer.transform("path/to/file.txt")  # Detected as file
```

### Custom Processors

```python
def extract_keywords(text):
    """Custom processor to extract keywords"""
    words = text.lower().split()
    keywords = [w for w in words if len(w) > 5]
    return {'keywords': keywords}

transformer.add_processor(extract_keywords)
result = transformer.transform("Your text here")
```

### Batch Processing

```python
# Process multiple texts at once
inputs = [
    ("text1.txt", "file"),
    ("https://example.com/page", "url"),
    ("Direct text string", "string")
]

results = transformer.transform_batch(inputs)
```

### Export Results

```python
# Convert to dictionary
data_dict = result.to_dict()

# Export to JSON
import json
json_output = json.dumps(result.to_dict(), indent=2)
```

## Built-in Processors

- `basic_stats_processor`: Extract word count, line count, character count, and average word length
- `extract_sentences`: Split text into sentences
- `extract_paragraphs`: Split text into paragraphs

## API Reference

### TextTransformer

The main class for transforming text into structured data.

**Methods:**
- `add_processor(processor)`: Add a text processor function
- `transform(input_data, source_type=None)`: Transform text from any source
- `transform_batch(inputs, source_type=None)`: Transform multiple texts

### StructuredData

Data model for structured output.

**Attributes:**
- `source`: The source of the text
- `content`: The original text content
- `extracted_data`: Dictionary containing extracted information
- `metadata`: Additional metadata about the extraction
- `timestamp`: When the data was extracted

**Methods:**
- `to_dict()`: Convert to dictionary representation
- `add_field(key, value)`: Add a field to extracted_data
- `get_field(key, default=None)`: Get a field from extracted_data

## Development

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=question_maker
```

## Examples

See the `examples/` directory for more detailed examples:
- `basic_usage.py`: Basic usage examples with different sources and processors

## License

MIT