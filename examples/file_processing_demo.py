#!/usr/bin/env python3
"""
Demo script that processes an input text file containing multiple-choice questions
and saves the structured results to an output file for inspection.
"""

import json
import os
from datetime import datetime
from pathlib import Path

from question_maker import TextTransformer
from question_maker.text_transformer import (
    basic_stats_processor,
    extract_multiple_choice_questions,
    extract_sentences,
    extract_paragraphs
)


def process_file_demo():
    """
    Process the AA-metabolism.txt file and save results to output files
    """
    # Define file paths
    script_dir = Path(__file__).parent
    input_file = script_dir / "inputs" / "AA-metabolism.txt"
    output_dir = script_dir / "outputs"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Check if input file exists
    if not input_file.exists():
        print(f"Error: Input file not found at {input_file}")
        return
    
    print("=== File Processing Demo ===")
    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Create transformer with multiple processors
    transformer = TextTransformer()
    transformer.add_processor(basic_stats_processor)
    transformer.add_processor(extract_multiple_choice_questions)
    transformer.add_processor(extract_sentences)
    transformer.add_processor(extract_paragraphs)
    
    # Process the file
    print("Processing file...")
    result = transformer.transform(str(input_file), source_type='file')
    
    # Display summary
    print(f"✓ File processed successfully!")
    print(f"  Source: {result.source}")
    print(f"  Content length: {len(result.content):,} characters")
    print(f"  Processing timestamp: {result.timestamp}")
    print()
    
    # Extract key metrics
    data = result.extracted_data
    print("=== Processing Results ===")
    print(f"Multiple-choice questions found: {data.get('question_count', 0)}")
    print(f"Questions with options: {data.get('questions_with_options', 0)}")
    print(f"Total words: {data.get('word_count', 0):,}")
    print(f"Total sentences: {data.get('sentence_count', 0)}")
    print(f"Total paragraphs: {data.get('paragraph_count', 0)}")
    print(f"Average word length: {data.get('avg_word_length', 0):.1f} characters")
    print()
    
    # Save complete results as JSON
    json_output_file = output_dir / f"AA-metabolism_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    print(f"Saving complete results to: {json_output_file.name}")
    with open(json_output_file, 'w', encoding='utf-8') as f:
        json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
    
    # Save human-readable summary
    summary_file = output_dir / f"AA-metabolism_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    print(f"Saving human-readable summary to: {summary_file.name}")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("AMINO ACID METABOLISM - MULTIPLE CHOICE QUESTIONS ANALYSIS\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"File processed: {input_file.name}\n")
        f.write(f"Processing date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Content length: {len(result.content):,} characters\n\n")
        
        f.write("SUMMARY STATISTICS:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total questions found: {data.get('question_count', 0)}\n")
        f.write(f"Questions with options: {data.get('questions_with_options', 0)}\n")
        f.write(f"Word count: {data.get('word_count', 0):,}\n")
        f.write(f"Sentence count: {data.get('sentence_count', 0)}\n")
        f.write(f"Paragraph count: {data.get('paragraph_count', 0)}\n")
        f.write(f"Average word length: {data.get('avg_word_length', 0):.2f} characters\n\n")
        
        # Write all questions in detail
        f.write("EXTRACTED QUESTIONS:\n")
        f.write("=" * 20 + "\n\n")
        
        questions = data.get('multiple_choice_questions', [])
        for i, question_data in enumerate(questions, 1):
            f.write(f"QUESTION {i}:\n")
            f.write(f"{question_data['question']}\n\n")
            
            f.write("OPTIONS:\n")
            for label in sorted(question_data['options'].keys()):
                f.write(f"  {label}. {question_data['options'][label]}\n")
            
            f.write(f"\nQuestion number: {question_data.get('question_number', 'N/A')}\n")
            f.write(f"Text position: {question_data.get('start_position', 0)}-{question_data.get('end_position', 0)}\n")
            f.write("\n" + "-" * 50 + "\n\n")
    
    # Save questions in a simple format for easy review
    simple_format_file = output_dir / f"AA-metabolism_questions_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    print(f"Saving simple question format to: {simple_format_file.name}")
    with open(simple_format_file, 'w', encoding='utf-8') as f:
        f.write("AMINO ACID METABOLISM QUESTIONS - SIMPLE FORMAT\n")
        f.write("=" * 50 + "\n\n")
        
        questions = data.get('multiple_choice_questions', [])
        for i, question_data in enumerate(questions, 1):
            f.write(f"{i}. {question_data['question']}\n")
            for label in sorted(question_data['options'].keys()):
                f.write(f"   {label}) {question_data['options'][label]}\n")
            f.write("\n")
    
    # Create a CSV file with question data for spreadsheet analysis
    csv_file = output_dir / f"AA-metabolism_questions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    print(f"Saving CSV format to: {csv_file.name}")
    import csv
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(['Question_Number', 'Question_Text', 'Option_A', 'Option_B', 'Option_C', 'Option_D', 'Option_E', 'Start_Position', 'End_Position'])
        
        # Write question data
        questions = data.get('multiple_choice_questions', [])
        for question_data in questions:
            options = question_data['options']
            row = [
                question_data.get('question_number', ''),
                question_data['question'],
                options.get('A', ''),
                options.get('B', ''),
                options.get('C', ''),
                options.get('D', ''),
                options.get('E', ''),
                question_data.get('start_position', ''),
                question_data.get('end_position', '')
            ]
            writer.writerow(row)
    
    print("\n=== Files Created ===")
    print(f"1. Complete JSON results: {json_output_file.name}")
    print(f"2. Human-readable summary: {summary_file.name}")
    print(f"3. Simple question format: {simple_format_file.name}")
    print(f"4. CSV for spreadsheet analysis: {csv_file.name}")
    print(f"\nAll files saved to: {output_dir}")
    
    # Display first few questions as preview
    print("\n=== PREVIEW (First 3 Questions) ===")
    questions = data.get('multiple_choice_questions', [])
    for i, question_data in enumerate(questions[:3], 1):
        print(f"\n{i}. {question_data['question']}")
        for label in sorted(question_data['options'].keys()):
            print(f"   {label}) {question_data['options'][label]}")
    
    if len(questions) > 3:
        print(f"\n... and {len(questions) - 3} more questions")


if __name__ == "__main__":
    process_file_demo()