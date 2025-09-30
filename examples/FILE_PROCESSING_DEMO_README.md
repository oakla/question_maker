# File Processing Demo Results

## Overview
This demo processed the `AA-metabolism.txt` file containing biochemistry multiple-choice questions and generated multiple output formats for easy inspection and analysis.

## Input File
- **File**: `examples/inputs/AA-metabolism.txt`
- **Content**: 12 amino acid metabolism multiple-choice questions
- **Size**: 3,670 characters (645 words)

## Processing Results
- ✅ **12 questions extracted** (all with complete A-E options)
- ✅ **645 words** analyzed
- ✅ **56 sentences** identified
- ✅ **Average word length**: 4.7 characters

## Output Files Generated

### 1. JSON Results (`AA-metabolism_results_YYYYMMDD_HHMMSS.json`)
- **Purpose**: Complete structured data in JSON format
- **Contains**: Full `StructuredData` object with all extracted information
- **Use case**: Programmatic access, API integration, data processing pipelines

### 2. Human-Readable Summary (`AA-metabolism_summary_YYYYMMDD_HHMMSS.txt`)
- **Purpose**: Detailed, formatted report for human review
- **Contains**: 
  - Processing statistics
  - Each question with full details
  - Text position information
  - Question numbering
- **Use case**: Manual review, documentation, detailed analysis

### 3. Simple Format (`AA-metabolism_questions_simple_YYYYMMDD_HHMMSS.txt`)
- **Purpose**: Clean, easy-to-read question format
- **Contains**: Questions with numbered options (1-12 format)
- **Use case**: Quick review, printing, sharing with others

### 4. CSV Format (`AA-metabolism_questions_YYYYMMDD_HHMMSS.csv`)
- **Purpose**: Spreadsheet-compatible data
- **Contains**: Tabular data with columns for:
  - Question number
  - Question text
  - All options (A-E)
  - Text positions
- **Use case**: Excel analysis, database import, statistical analysis

## File Locations
All output files are saved in: `examples/outputs/`

## Usage Examples

### For Developers
```python
# Load JSON results for programmatic use
import json
with open('AA-metabolism_results_YYYYMMDD_HHMMSS.json', 'r') as f:
    data = json.load(f)
    
questions = data['extracted_data']['multiple_choice_questions']
for q in questions:
    print(f"Q: {q['question']}")
    for opt in q['options']:
        print(f"  {opt}: {q['options'][opt]}")
```

### For Educators
- Use the **simple format** for creating study materials
- Use the **CSV format** for creating question banks in learning management systems
- Use the **summary format** for detailed question analysis

### For Data Analysis
- Import **CSV format** into Excel or statistical software
- Use **JSON format** for automated processing pipelines
- Text position data enables source tracking and verification

## Features Demonstrated
1. **File input processing** - Reading from text files
2. **Multiple output formats** - JSON, TXT, CSV for different use cases
3. **Comprehensive analysis** - Statistics, positions, numbering
4. **Error handling** - Graceful handling of file operations
5. **Timestamp tracking** - Processing time and date recording

## Next Steps
- Process additional question files
- Integrate with quiz generation systems
- Add answer key functionality
- Create batch processing for multiple files