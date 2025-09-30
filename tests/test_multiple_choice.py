"""Tests for multiple-choice question extraction"""

import pytest
from question_maker import TextTransformer, MultipleChoiceQuestion
from question_maker.text_transformer import extract_multiple_choice_questions


def test_multiple_choice_question_creation():
    """Test creating a MultipleChoiceQuestion"""
    question = MultipleChoiceQuestion(
        question="What is 2 + 2?",
        question_number=1
    )
    question.add_option("A", "3")
    question.add_option("B", "4")
    question.add_option("C", "5")
    
    assert question.question == "What is 2 + 2?"
    assert question.question_number == 1
    assert len(question.options) == 3
    assert question.options["B"] == "4"
    assert question.get_option_labels() == ["A", "B", "C"]


def test_multiple_choice_question_to_dict():
    """Test converting MultipleChoiceQuestion to dictionary"""
    question = MultipleChoiceQuestion(
        question="Test question?",
        question_number=1
    )
    question.add_option("A", "Option A")
    question.add_option("B", "Option B")
    
    result = question.to_dict()
    assert isinstance(result, dict)
    assert result['question'] == "Test question?"
    assert result['options']['A'] == "Option A"
    assert result['question_number'] == 1


def test_multiple_choice_question_full_text():
    """Test getting full text of a multiple-choice question"""
    question = MultipleChoiceQuestion(question="What color is the sky?")
    question.add_option("A", "Red")
    question.add_option("B", "Blue")
    question.add_option("C", "Green")
    
    full_text = question.get_full_text()
    expected = "What color is the sky?\nA Red\nB Blue\nC Green"
    assert full_text == expected


def test_extract_single_multiple_choice_question():
    """Test extracting a single multiple-choice question"""
    text = """Which of the following is an essential amino acid in humans?
A Tyrosine
B Glutamine
C Glutamate
D Phenylalanine
E Lysine"""
    
    result = extract_multiple_choice_questions(text)
    
    assert 'multiple_choice_questions' in result
    assert 'question_count' in result
    assert result['question_count'] == 1
    
    questions = result['multiple_choice_questions']
    assert len(questions) == 1
    
    question = questions[0]
    assert question['question'] == "Which of the following is an essential amino acid in humans?"
    assert len(question['options']) == 5
    assert question['options']['A'] == "Tyrosine"
    assert question['options']['E'] == "Lysine"


def test_extract_multiple_questions():
    """Test extracting multiple questions from text"""
    text = """Which of the following is an essential amino acid in humans?
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
E is catabolised to yield acetyl CoA or acetoacetyl CoA."""
    
    result = extract_multiple_choice_questions(text)
    
    assert result['question_count'] == 2
    questions = result['multiple_choice_questions']
    
    assert questions[0]['question'] == "Which of the following is an essential amino acid in humans?"
    assert questions[1]['question'] == 'The term "ketogenic" describes an amino acid that:'
    
    # Check that both questions have 5 options
    assert len(questions[0]['options']) == 5
    assert len(questions[1]['options']) == 5


def test_extract_questions_with_transformer():
    """Test using the multiple-choice processor with TextTransformer"""
    transformer = TextTransformer()
    transformer.add_processor(extract_multiple_choice_questions)
    
    text = """What is the capital of France?
A London
B Paris
C Berlin
D Madrid

Which planet is closest to the Sun?
A Venus
B Earth
C Mercury
D Mars"""
    
    result = transformer.transform(text, source_type='string')
    
    assert 'multiple_choice_questions' in result.extracted_data
    assert 'question_count' in result.extracted_data
    assert result.extracted_data['question_count'] == 2
    
    questions = result.extracted_data['multiple_choice_questions']
    assert questions[0]['question'] == "What is the capital of France?"
    assert questions[1]['question'] == "Which planet is closest to the Sun?"


def test_extract_questions_with_irregular_spacing():
    """Test extracting questions with irregular spacing and formatting"""
    text = """
    
What is 2 + 2?
A 3
B 4
C 5


Which programming language is this?
A Python
B Java
C JavaScript
    """
    
    result = extract_multiple_choice_questions(text)
    
    assert result['question_count'] == 2
    questions = result['multiple_choice_questions']
    
    assert questions[0]['question'] == "What is 2 + 2?"
    assert questions[1]['question'] == "Which programming language is this?"


def test_extract_questions_with_no_options():
    """Test handling text with question-like content but no options"""
    text = """This is just regular text.
It has some lines.
But no multiple choice questions.
What do you think?
Nothing with A B C format."""
    
    result = extract_multiple_choice_questions(text)
    
    # Should return empty results since no valid questions with options
    assert result['question_count'] == 0
    assert len(result['multiple_choice_questions']) == 0


def test_complex_question_text():
    """Test with the provided complex biochemistry text"""
    text = """Which of the following is an essential amino acid in humans?
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
E It is located in the mitochondria."""
    
    result = extract_multiple_choice_questions(text)
    
    assert result['question_count'] == 3
    questions = result['multiple_choice_questions']
    
    # Verify each question has the expected content
    assert "essential amino acid" in questions[0]['question']
    assert "ketogenic" in questions[1]['question']
    assert "glutamate dehydrogenase" in questions[2]['question']
    
    # Verify all questions have 5 options (A through E)
    for question in questions:
        assert len(question['options']) == 5
        assert all(label in question['options'] for label in ['A', 'B', 'C', 'D', 'E'])