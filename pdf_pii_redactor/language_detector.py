"""
Language detection for PDF documents.
"""

import logging
from typing import Dict, List, Any
from langdetect import detect, LangDetectException

logger = logging.getLogger(__name__)

class LanguageDetector:
    """
    Detects the language of text content.
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the language detector.
        
        Args:
            verbose: Whether to enable verbose logging
        """
        self.verbose = verbose
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of a text.
        
        Args:
            text: Text to analyze
            
        Returns:
            ISO 639-1 language code (e.g., 'en', 'fr', 'es')
        """
        try:
            if not text or len(text.strip()) < 10:
                # Default to English for very short texts
                return "en"
            
            lang = detect(text)
            
            if self.verbose:
                logger.info(f"Detected language: {lang}")
            
            return lang
        except LangDetectException as e:
            logger.warning(f"Language detection failed: {str(e)}. Defaulting to English.")
            return "en"
    
    def detect_document_language(self, pages: List[Dict[str, Any]]) -> str:
        """
        Detect the primary language of a document.
        
        Args:
            pages: List of page dictionaries with text content
            
        Returns:
            ISO 639-1 language code
        """
        if not pages:
            return "en"
        
        # Concatenate a sample of text from each page
        sample_text = ""
        for page in pages[:min(5, len(pages))]:  # Use up to 5 pages for detection
            page_text = page.get("text", "")
            # Take first 1000 characters from each page
            sample_text += page_text[:1000] + " "
        
        return self.detect_language(sample_text) 