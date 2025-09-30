"""
Text transformation engine for converting text into structured data
"""

from typing import Dict, Any, List, Optional
from .data_models import StructuredData, TextSegment
from .input_handlers import TextSource, create_source


class TextTransformer:
    """
    Main class for transforming text into structured data
    """
    
    def __init__(self):
        self.processors: List[callable] = []
    
    def add_processor(self, processor: callable) -> None:
        """
        Add a text processor function
        
        Args:
            processor: A function that takes text and returns Dict[str, Any]
        """
        self.processors.append(processor)
    
    def transform(self, input_data: str, source_type: Optional[str] = None) -> StructuredData:
        """
        Transform text from any source into structured data
        
        Args:
            input_data: File path, URL, or text string
            source_type: Optional type hint ('file', 'url', 'string')
        
        Returns:
            StructuredData object containing extracted information
        """
        # Get text from source
        source = create_source(input_data, source_type)
        text = source.read()
        source_info = source.get_source_info()
        
        # Create structured data object
        structured_data = StructuredData(
            source=source_info,
            content=text
        )
        
        # Apply processors
        for processor in self.processors:
            result = processor(text)
            if isinstance(result, dict):
                structured_data.extracted_data.update(result)
        
        # Add basic metadata
        structured_data.metadata['text_length'] = len(text)
        structured_data.metadata['processor_count'] = len(self.processors)
        
        return structured_data
    
    def transform_batch(self, inputs: List[tuple], source_type: Optional[str] = None) -> List[StructuredData]:
        """
        Transform multiple texts into structured data
        
        Args:
            inputs: List of (input_data, optional_source_type) tuples
            source_type: Default source type if not specified in tuple
        
        Returns:
            List of StructuredData objects
        """
        results = []
        for input_item in inputs:
            if isinstance(input_item, tuple):
                input_data, item_source_type = input_item[0], input_item[1] if len(input_item) > 1 else source_type
            else:
                input_data, item_source_type = input_item, source_type
            
            results.append(self.transform(input_data, item_source_type))
        
        return results


# Built-in processors
def basic_stats_processor(text: str) -> Dict[str, Any]:
    """Extract basic statistics from text"""
    words = text.split()
    lines = text.split('\n')
    
    return {
        'word_count': len(words),
        'line_count': len(lines),
        'char_count': len(text),
        'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0
    }


def extract_sentences(text: str) -> Dict[str, Any]:
    """Extract sentences from text (simple implementation)"""
    # Simple sentence splitting on period, exclamation, question mark
    import re
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return {
        'sentences': sentences,
        'sentence_count': len(sentences)
    }


def extract_paragraphs(text: str) -> Dict[str, Any]:
    """Extract paragraphs from text"""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    return {
        'paragraphs': paragraphs,
        'paragraph_count': len(paragraphs)
    }


def extract_multiple_choice_questions(text: str) -> Dict[str, Any]:
    """
    Extract multiple-choice questions from text
    
    Expects questions in the format:
    Question text?
    A Option 1
    B Option 2
    C Option 3
    ...
    
    Returns:
        Dictionary containing extracted questions and metadata
    """
    import re
    from .data_models import MultipleChoiceQuestion
    
    questions = []
    lines = text.split('\n')
    current_question = None
    current_position = 0
    line_position = 0
    question_number = 1
    
    for i, line in enumerate(lines):
        line = line.strip()
        line_position += len(lines[i]) + 1  # +1 for newline character
        
        if not line:
            continue
            
        # Check if line is an option (starts with single letter followed by space)
        option_match = re.match(r'^([A-Z])\s+(.+)$', line)
        
        if option_match:
            if current_question is not None:
                label, option_text = option_match.groups()
                current_question.add_option(label, option_text)
        else:
            # This is likely a new question
            if current_question is not None:
                # Finalize the previous question
                current_question.end_position = line_position - len(line) - 1
                if current_question.options:  # Only add if it has options
                    questions.append(current_question)
            
            # Start a new question
            current_question = MultipleChoiceQuestion(
                question=line,
                question_number=question_number,
                start_position=line_position - len(line) - 1
            )
            question_number += 1
    
    # Don't forget the last question
    if current_question is not None and current_question.options:
        current_question.end_position = len(text)
        questions.append(current_question)
    
    # Convert questions to dictionaries for serialization
    questions_data = [q.to_dict() for q in questions]
    
    return {
        'multiple_choice_questions': questions_data,
        'question_count': len(questions_data),
        'questions_with_options': sum(1 for q in questions_data if q.get('options'))
    }
