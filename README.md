# question_maker

A Python project for transforming text from various sources into structured data.

## Features

### 🖥️ **GUI Application**
- **User-Friendly Interface**: Modern tabbed interface with intuitive design
- **Multiple Input Methods**: File browser, URL input, or direct text entry
- **Real-Time Processing**: Progress bars and status updates
- **Interactive Results**: Tree view for browsing questions, detailed preview
- **Multiple Export Formats**: JSON, CSV, and formatted text export
- **Configurable Processing**: Choose which analysis processors to run

### 🔧 **Core Library**
- **Multiple Input Sources**: Read text from files, URLs, or strings
- **Flexible Processing**: Add custom processors to extract specific information
- **Built-in Processors**: Extract statistics, sentences, paragraphs, and multiple-choice questions
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

### GUI Application (Recommended)
Launch the user-friendly graphical interface:
```bash
python run_gui.py
```
Or on Windows, double-click: `run_gui.bat`

### Command Line/Programming
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
- `extract_multiple_choice_questions`: Extract multiple-choice questions from text in the format:
  ```
  Question text?
  A Option 1
  B Option 2
  C Option 3
  ```

### Multiple-Choice Question Extraction

The `extract_multiple_choice_questions` processor can identify and structure multiple-choice questions from text:

```python
from question_maker import TextTransformer
from question_maker.text_transformer import extract_multiple_choice_questions

transformer = TextTransformer()
transformer.add_processor(extract_multiple_choice_questions)

quiz_text = """What is the capital of France?
A London
B Paris
C Berlin
D Madrid

Which programming language is this?
A Java
B Python
C JavaScript
D C++"""

result = transformer.transform(quiz_text, source_type='string')

# Access extracted questions
questions = result.extracted_data['multiple_choice_questions']
print(f"Found {result.extracted_data['question_count']} questions")

for question in questions:
    print(f"Q: {question['question']}")
    for label, option in sorted(question['options'].items()):
        print(f"  {label}: {option}")
```

### MultipleChoiceQuestion Data Model

Each extracted question is represented using the `MultipleChoiceQuestion` class:

```python
from question_maker import MultipleChoiceQuestion

# Create a question manually
question = MultipleChoiceQuestion(
    question="What is 2 + 2?",
    question_number=1
)
question.add_option("A", "3")
question.add_option("B", "4")
question.add_option("C", "5")

# Get full formatted text
print(question.get_full_text())
# Output:
# What is 2 + 2?
# A 3
# B 4
# C 5

# Convert to dictionary
question_dict = question.to_dict()
```

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

## GUI Usage

### Launching the Application
```bash
# Method 1: Python launcher
python run_gui.py

# Method 2: Windows batch file
run_gui.bat

# Method 3: Direct execution
python gui_app.py
```

### Using the Interface
1. **Input Tab**: Choose your text source
   - **File**: Browse and select text files
   - **URL**: Enter web page URLs
   - **Text Input**: Type or paste text directly
   
2. **Settings Tab**: Configure processors
   - Enable/disable analysis features
   - Choose export options and location
   - Set custom export directory
   
3. **Results Tab**: View and export results
   - Summary statistics
   - Interactive question browser
   - Multiple export formats with location selection

### Export Options
- **JSON**: Complete structured data for programming
- **CSV**: Spreadsheet-compatible format  
- **Text**: Human-readable formatted output
- **Auto-Export**: Automatically save timestamped files
- **Custom Location**: Choose where files are saved
- **Quick Access**: Open export folder directly from GUI

## Examples

See the `examples/` directory for more detailed examples:
- `basic_usage.py`: Basic usage examples with different sources and processors
- `multiple_choice_demo.py`: Comprehensive demonstration of multiple-choice question extraction
- `test_user_text.py`: Test with real-world biochemistry exam questions
- `file_processing_demo.py`: Batch processing and multiple output formats
- `gui_features_demo.py`: Overview of GUI capabilities and features
- `export_location_demo.py`: New export location selection features

## License

MIT