"""
question_maker - A project for transforming text from various sources into structured data
"""

__version__ = "0.1.0"

from .text_transformer import TextTransformer, extract_multiple_choice_questions
from .data_models import StructuredData, MultipleChoiceQuestion

__all__ = ["TextTransformer", "StructuredData", "MultipleChoiceQuestion", "extract_multiple_choice_questions"]
