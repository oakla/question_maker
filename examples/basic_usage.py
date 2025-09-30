"""
Basic example of using question_maker to transform text into structured data
"""
import os

from question_maker import TextTransformer
from question_maker.text_transformer import (
    basic_stats_processor, 
    extract_sentences, 
    extract_paragraphs,
    extract_multiple_choice_questions
)


def main():
    # Create a transformer
    transformer = TextTransformer()
    
    # Add built-in processors
    transformer.add_processor(basic_stats_processor)
    transformer.add_processor(extract_sentences)
    transformer.add_processor(extract_paragraphs)
    
    # Example 1: Transform a simple string
    print("=" * 60)
    print("Example 1: Transform a simple string")
    print("=" * 60)
    
    text = """
    Hello, world! This is a simple example.
    It demonstrates how to use question_maker to transform text into structured data.
    
    The library can extract various features from text.
    This includes word counts, sentences, and paragraphs.
    """
    
    result = transformer.transform(text, source_type='string')
    
    print(f"Source: {result.source}")
    print(f"Text length: {len(result.content)}")
    print(f"\nExtracted data:")
    for key, value in result.extracted_data.items():
        if isinstance(value, list):
            print(f"  {key}: {len(value)} items")
        else:
            print(f"  {key}: {value}")
    
    # Example 2: Transform from a file
    print("\n" + "=" * 60)
    print("Example 2: Transform from a file")
    print("=" * 60)
    
    # Create a sample file
    import tempfile
    sample_file = os.path.join(tempfile.gettempdir(), 'sample_text.txt')
    with open(sample_file, 'w') as f:
        f.write("""Python is a high-level programming language.
It is widely used for web development, data analysis, and machine learning.

Python emphasizes code readability and simplicity.
This makes it an excellent choice for beginners and experts alike!""")
    
    result = transformer.transform(sample_file, source_type='file')
    
    print(f"Source: {result.source}")
    print(f"\nExtracted data:")
    for key, value in result.extracted_data.items():
        if isinstance(value, list):
            print(f"  {key}: {len(value)} items")
            if key == 'sentences' and value:
                print(f"    First sentence: {value[0]}")
        else:
            print(f"  {key}: {value}")
    
    # Example 3: Custom processor
    print("\n" + "=" * 60)
    print("Example 3: Custom processor")
    print("=" * 60)
    
    def count_questions(text):
        """Count question marks in text"""
        return {'question_count': text.count('?')}
    
    # Create a new transformer with custom processor
    custom_transformer = TextTransformer()
    custom_transformer.add_processor(basic_stats_processor)
    custom_transformer.add_processor(count_questions)
    
    question_text = "What is Python? How does it work? Why is it popular?"
    result = custom_transformer.transform(question_text, source_type='string')
    
    print(f"Text: {question_text}")
    print(f"\nExtracted data:")
    for key, value in result.extracted_data.items():
        print(f"  {key}: {value}")
    
    # Example 4: Multiple-choice question extraction
    print("\n" + "=" * 60)
    print("Example 4: Multiple-choice question extraction")
    print("=" * 60)
    
    mc_transformer = TextTransformer()
    mc_transformer.add_processor(extract_multiple_choice_questions)
    mc_transformer.add_processor(basic_stats_processor)
    
    quiz_text = """What is the capital of France?
A London
B Paris
C Berlin
D Madrid

Which programming language is this example written in?
A Java
B Python
C JavaScript
D C++"""
    
    mc_result = mc_transformer.transform(quiz_text, source_type='string')
    
    print(f"Found {mc_result.extracted_data['question_count']} multiple-choice questions")
    print(f"Total words: {mc_result.extracted_data['word_count']}")
    
    for i, question in enumerate(mc_result.extracted_data['multiple_choice_questions'], 1):
        print(f"\nQuestion {i}: {question['question']}")
        for label, option in sorted(question['options'].items()):
            print(f"  {label}: {option}")
    
    # Example 5: Export to dictionary
    print("\n" + "=" * 60)
    print("Example 5: Export to dictionary/JSON")
    print("=" * 60)
    
    import json
    result_dict = result.to_dict()
    print(json.dumps(result_dict, indent=2, default=str))


if __name__ == '__main__':
    main()
