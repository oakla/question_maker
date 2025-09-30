# Copilot Instructions for question_maker

## Project Overview
This is a Python text processing library that transforms unstructured text from various sources (files, URLs, strings) into structured data using a processor-based architecture.

## Core Architecture

### Three-Layer Design Pattern
- **Input Layer**: `input_handlers.py` - Source abstraction with auto-detection (`FileSource`, `URLSource`, `StringSource`)
- **Processing Layer**: `text_transformer.py` - Processor registry and orchestration (`TextTransformer` class)
- **Data Layer**: `data_models.py` - Structured output models (`StructuredData`, `TextSegment`)

### Key Pattern: Processor Functions
Processors are simple functions that take text and return `Dict[str, Any]`:
```python
def custom_processor(text: str) -> Dict[str, Any]:
    return {'key': value}
```

Built-in processors: `basic_stats_processor`, `extract_sentences`, `extract_paragraphs`

## Development Workflow

### Installation & Setup
```bash
pip install -e .          # Basic install
pip install -e ".[dev]"   # With dev dependencies
```

### Testing
- Uses pytest with comprehensive test coverage
- Test pattern: `test_*.py` files in `tests/` directory
- Run: `pytest` or `pytest --cov=question_maker`

### Project Structure Conventions
- Main API exports in `__init__.py`: `TextTransformer`, `StructuredData`
- Examples in `examples/basic_usage.py` demonstrate all major features
- Quick start script in `bin/quick_start.py` for minimal usage

## Key Integration Points

### Source Auto-Detection Logic
The `create_source()` function in `input_handlers.py` uses this precedence:
1. Explicit `source_type` parameter
2. File existence check (`os.path.exists()`)
3. URL pattern matching (`http://`, `https://`)
4. Fallback to string source

### Data Flow Pattern
`input_data` → `TextSource.read()` → `processor(text)` → `StructuredData.extracted_data`

### Error Handling Approach
- `FileNotFoundError` for missing files
- `requests.RequestException` wrapped as `ValueError` for URL failures
- **Processors should return empty dict `{}` on failure, not raise exceptions**
- For malformed input, processors should gracefully degrade (e.g., return partial results or safe defaults)

## Code Style & Patterns

### Dataclass Usage
Use `@dataclass` with `field(default_factory=dict)` for mutable defaults. All data models include `to_dict()` method for serialization.

### Type Hints
- Use `Optional[str]` for source_type parameters
- Use `Dict[str, Any]` for processor return types
- Use `List[StructuredData]` for batch operations

### Metadata Pattern
Always populate `StructuredData.metadata` with processing context:
- `text_length`: Character count
- `processor_count`: Number of processors applied

## Future Architecture

### Planned GUI Integration
A GUI component will be added to the project. When working on GUI-related features:
- Keep the core text processing logic separate from UI concerns
- Ensure `TextTransformer` remains UI-agnostic for headless usage
- Consider how batch processing and real-time feedback will work in GUI context

When adding new processors, follow the established pattern in `text_transformer.py` and add corresponding tests in `tests/test_text_transformer.py`.