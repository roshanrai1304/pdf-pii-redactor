"""
Tests for the language detection functionality.
"""

import os
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_pii_redactor.language_detector import LanguageDetector


class TestLanguageDetector(unittest.TestCase):
    """Test cases for the language detector."""
    
    def setUp(self):
        """Set up test environment."""
        self.detector = LanguageDetector(verbose=True)
    
    def test_detect_language_empty_text(self):
        """Test language detection with empty text."""
        result = self.detector.detect_language("")
        self.assertEqual(result, "en")  # Default to English for empty text
    
    def test_detect_language_short_text(self):
        """Test language detection with very short text."""
        result = self.detector.detect_language("Hi")
        self.assertEqual(result, "en")  # Default to English for very short text
    
    def test_detect_language_english(self):
        """Test language detection with English text."""
        text = "This is a sample text in English language. It contains multiple sentences to ensure accurate detection."
        result = self.detector.detect_language(text)
        self.assertEqual(result, "en")
    
    def test_detect_language_spanish(self):
        """Test language detection with Spanish text."""
        text = "Este es un texto de ejemplo en español. Contiene varias frases para asegurar una detección precisa."
        result = self.detector.detect_language(text)
        self.assertEqual(result, "es")
    
    def test_detect_language_french(self):
        """Test language detection with French text."""
        text = "Ceci est un exemple de texte en français. Il contient plusieurs phrases pour assurer une détection précise."
        result = self.detector.detect_language(text)
        self.assertEqual(result, "fr")
    
    def test_detect_language_german(self):
        """Test language detection with German text."""
        text = "Dies ist ein Beispieltext in deutscher Sprache. Er enthält mehrere Sätze, um eine genaue Erkennung zu gewährleisten."
        result = self.detector.detect_language(text)
        self.assertEqual(result, "de")
    
    def test_detect_document_language(self):
        """Test document language detection with multiple pages."""
        pages = [
            {"page_num": 0, "text": "This is page one in English."},
            {"page_num": 1, "text": "This is page two, also in English."},
            {"page_num": 2, "text": "This is the third page of the document."}
        ]
        result = self.detector.detect_document_language(pages)
        self.assertEqual(result, "en")
    
    def test_detect_document_language_empty(self):
        """Test document language detection with empty pages list."""
        result = self.detector.detect_document_language([])
        self.assertEqual(result, "en")  # Default to English for empty document


if __name__ == "__main__":
    unittest.main() 