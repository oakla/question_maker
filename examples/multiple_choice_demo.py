#!/usr/bin/env python3
"""
Example script demonstrating multiple-choice question extraction functionality
"""

from question_maker import TextTransformer, extract_multiple_choice_questions

# Sample biochemistry questions (as provided in the user request)
SAMPLE_QUESTIONS = """Which of the following is an essential amino acid in humans?
A Tyrosine
B Glutamine
C Glutamate
D Phenylalanine
E Lysine
The term "ketogenic" describes an amino acid that:
A is a precursor for glucose synthesis.
B forms oxaloacetate during catabolism.
C cannot be converted to ketone bodies.
D degrades to give a-ketoglutarate.
E is catabolised to yield acetyl CoA or acetoacetyl CoA.
Which of the following statements regarding glutamate dehydrogenase is INCORRECT?
A It can use either NAD+ or NADP+ as a coenzyme.
B It catalyses an essentially reversible reaction.
C When catalysing the conversion of glutamate to its carbon skeleton, the reaction involves deamination.
D It is not subject to allosteric regulation.
E It is located in the mitochondria.
How is glutamate useful in amino acid synthesis reactions?
A It activates glutaminase to release free glutamine.
B It can be reduced and cyclised to form glycine.
C It acts as an amino group donor for synthesis of nonessential amino acids.
D It is the main precursor of tyrosine synthesis.
E It is the main methyl group donor for essential amino acids.
Which of the following statements is correct?
A In humans, nonessential amino acids are exclusively synthesised from essential amino acids.
B Humans can attain nonessential amino acids from a protein-rich diet.
C Alanine is a common methyl group donor in human essential amino acid synthesis.
D In humans, aspartate is formed from pyruvate and is therefore a nonessential amino acid.
E All nonessential amino acids are catabolised to form acetoacetate."""


def main():
    """Demonstrate multiple-choice question extraction"""
    print("=== Multiple-Choice Question Extraction Demo ===\n")
    
    # Method 1: Using the processor directly
    print("Method 1: Using extract_multiple_choice_questions processor directly")
    print("-" * 60)
    
    result = extract_multiple_choice_questions(SAMPLE_QUESTIONS)
    
    print(f"Found {result['question_count']} multiple-choice questions")
    print(f"Questions with options: {result['questions_with_options']}")
    print()
    
    # Display each question
    for i, question_data in enumerate(result['multiple_choice_questions'], 1):
        print(f"Question {i}:")
        print(f"  Text: {question_data['question']}")
        print(f"  Options: {len(question_data['options'])}")
        for label, option in sorted(question_data['options'].items()):
            print(f"    {label}: {option}")
        print()
    
    print("\n" + "="*80 + "\n")
    
    # Method 2: Using TextTransformer
    print("Method 2: Using TextTransformer with multiple processors")
    print("-" * 60)
    
    transformer = TextTransformer()
    transformer.add_processor(extract_multiple_choice_questions)
    
    # You could add other processors too
    from question_maker.text_transformer import basic_stats_processor
    transformer.add_processor(basic_stats_processor)
    
    structured_data = transformer.transform(SAMPLE_QUESTIONS, source_type='string')
    
    print(f"Source: {structured_data.source}")
    print(f"Content length: {len(structured_data.content)} characters")
    print(f"Timestamp: {structured_data.timestamp}")
    
    # Multiple-choice questions data
    mc_data = structured_data.extracted_data
    print(f"\nExtracted {mc_data['question_count']} questions")
    print(f"Basic stats - Word count: {mc_data.get('word_count', 'N/A')}")
    
    # Show first two questions as examples
    print("\nFirst two questions:")
    for i, question_data in enumerate(mc_data['multiple_choice_questions'][:2], 1):
        print(f"\n{i}. {question_data['question']}")
        for label in sorted(question_data['options'].keys()):
            print(f"   {label}. {question_data['options'][label]}")
    
    print("\n" + "="*80 + "\n")
    
    # Method 3: Working with individual MultipleChoiceQuestion objects
    print("Method 3: Working with MultipleChoiceQuestion objects")
    print("-" * 60)
    
    from question_maker import MultipleChoiceQuestion
    
    # Create a question manually
    question = MultipleChoiceQuestion(
        question="What is the primary function of the urea cycle?",
        question_number=1
    )
    question.add_option("A", "produce ATP")
    question.add_option("B", "synthesise amino acids")
    question.add_option("C", "detoxify ammonia")
    question.add_option("D", "generate NADH")
    question.add_option("E", "produce urine")
    
    print("Manually created question:")
    print(question.get_full_text())
    print(f"\nOption labels: {question.get_option_labels()}")
    print(f"Question as dict: {question.to_dict()}")


if __name__ == "__main__":
    main()