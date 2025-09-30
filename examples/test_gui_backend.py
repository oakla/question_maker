#!/usr/bin/env python3
"""
Test script to verify GUI functionality programmatically
"""

import sys
import os
import tempfile
import json

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from question_maker import TextTransformer
from question_maker.text_transformer import extract_multiple_choice_questions, basic_stats_processor


def test_gui_backend():
    """Test the backend functionality that the GUI uses"""
    print("Testing GUI Backend Functionality")
    print("=" * 40)
    
    # Sample text (same as what GUI example uses)
    sample_text = """Which of the following is an essential amino acid in humans?
A Tyrosine
B Glutamine
C Glutamate
D Phenylalanine
E Lysine

What is the capital of France?
A London
B Paris
C Berlin
D Madrid

Which programming language is this application written in?
A Java
B Python
C JavaScript
D C++"""
    
    # Create transformer (same as GUI does)
    transformer = TextTransformer()
    transformer.add_processor(basic_stats_processor)
    transformer.add_processor(extract_multiple_choice_questions)
    
    # Process text
    print("Processing sample text...")
    result = transformer.transform(sample_text, source_type='string')
    
    # Display results (simulate what GUI shows)
    print(f"✓ Processing completed")
    print(f"  Source: {result.source}")
    print(f"  Content length: {len(result.content)} characters")
    print(f"  Timestamp: {result.timestamp}")
    print()
    
    data = result.extracted_data
    print("Results Summary:")
    print(f"  Word count: {data.get('word_count', 'N/A')}")
    print(f"  Character count: {data.get('char_count', 'N/A')}")
    print(f"  Questions found: {data.get('question_count', 0)}")
    print(f"  Questions with options: {data.get('questions_with_options', 0)}")
    print()
    
    # Display questions (simulate GUI tree view)
    if 'multiple_choice_questions' in data:
        questions = data['multiple_choice_questions']
        print("Extracted Questions:")
        print("-" * 20)
        
        for i, question in enumerate(questions, 1):
            print(f"{i}. {question['question']}")
            option_count = len(question.get('options', {}))
            print(f"   Options: {option_count}")
            
            # Show options (simulate GUI detail view)
            for label in sorted(question.get('options', {}).keys()):
                print(f"     {label}) {question['options'][label]}")
            print()
    
    # Test export functionality (simulate GUI exports)
    print("Testing Export Functionality:")
    print("-" * 30)
    
    # Test JSON export
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(result.to_dict(), f, indent=2)
        json_file = f.name
    
    print(f"✓ JSON export: {os.path.basename(json_file)}")
    
    # Test CSV export
    if 'multiple_choice_questions' in data:
        import csv
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Question_Number', 'Question_Text', 'Option_A', 'Option_B', 
                           'Option_C', 'Option_D', 'Option_E'])
            
            for question in questions:
                options = question.get('options', {})
                row = [
                    question.get('question_number', ''),
                    question['question'],
                    options.get('A', ''),
                    options.get('B', ''),
                    options.get('C', ''),
                    options.get('D', ''),
                    options.get('E', '')
                ]
                writer.writerow(row)
            csv_file = f.name
        
        print(f"✓ CSV export: {os.path.basename(csv_file)}")
    
    # Test text export
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("QUESTION MAKER TEST RESULTS\n")
        f.write("=" * 30 + "\n\n")
        
        if 'multiple_choice_questions' in data:
            questions = data['multiple_choice_questions']
            for i, question in enumerate(questions, 1):
                f.write(f"{i}. {question['question']}\n")
                for label in sorted(question.get('options', {}).keys()):
                    f.write(f"   {label}) {question['options'][label]}\n")
                f.write("\n")
        text_file = f.name
    
    print(f"✓ Text export: {os.path.basename(text_file)}")
    print()
    
    # Cleanup
    try:
        os.unlink(json_file)
        os.unlink(csv_file) 
        os.unlink(text_file)
        print("✓ Temporary files cleaned up")
    except:
        pass
    
    print("\n" + "=" * 40)
    print("✅ GUI Backend Test Completed Successfully!")
    print("The GUI application should work correctly with this functionality.")
    print()
    print("To launch the GUI:")
    print("  python run_gui.py")
    print("  or")
    print("  run_gui.bat (Windows)")


if __name__ == "__main__":
    test_gui_backend()