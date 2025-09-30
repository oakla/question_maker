"""
Data models for structured data representation
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class StructuredData:
    """
    Represents structured data extracted from text
    
    Attributes:
        source: The source of the text (file path, URL, or 'string')
        content: The original text content
        extracted_data: Dictionary containing extracted structured information
        metadata: Additional metadata about the extraction
        timestamp: When the data was extracted
    """
    source: str
    content: str
    extracted_data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return asdict(self)
    
    def add_field(self, key: str, value: Any) -> None:
        """Add a field to extracted_data"""
        self.extracted_data[key] = value
    
    def get_field(self, key: str, default: Any = None) -> Any:
        """Get a field from extracted_data"""
        return self.extracted_data.get(key, default)


@dataclass
class TextSegment:
    """
    Represents a segment of text with metadata
    
    Attributes:
        text: The text content
        start_position: Starting position in original text
        end_position: Ending position in original text
        category: Category or type of segment
    """
    text: str
    start_position: int = 0
    end_position: int = 0
    category: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return asdict(self)
