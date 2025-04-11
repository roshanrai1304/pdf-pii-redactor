"""
Tests for the PDF processing functionality.
"""

import os
import tempfile
import unittest
import fitz 
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_pii_redactor.pdf_processor import PDFProcessor


class TestPDFProcessor(unittest.TestCase):
    """Test cases for the PDF processor."""
    
    def setUp(self):
        """Set up test environment."""
        self.processor = PDFProcessor(verbose=True)
        
        # Create a simple test PDF
        self.test_pdf_path = self._create_test_pdf()
    
    def tearDown(self):
        """Clean up after tests."""
        if hasattr(self, 'test_pdf_path') and os.path.exists(self.test_pdf_path):
            os.unlink(self.test_pdf_path)
    
    def _create_test_pdf(self):
        """Create a simple PDF for testing."""
        pdf_path = tempfile.mktemp(suffix=".pdf")
        
        # Create a new PDF with some text
        doc = fitz.open()
        page = doc.new_page()
        
        # Add some text with PII
        text = "Hello, my name is John Doe. My email is john.doe@example.com and my phone is (555) 123-4567."
        page.insert_text((50, 50), text)
        
        # Add a second page
        page = doc.new_page()
        page.insert_text((50, 50), "This is page 2 with no PII.")
        
        # Save the document
        doc.save(pdf_path)
        doc.close()
        
        return pdf_path
    
    def test_extract_text(self):
        """Test text extraction from PDF."""
        pages = self.processor.extract_text(self.test_pdf_path)
        
        self.assertEqual(len(pages), 2)
        self.assertIn("John Doe", pages[0]["text"])
        self.assertIn("john.doe@example.com", pages[0]["text"])
        self.assertIn("page 2", pages[1]["text"])
    
    def test_find_text_instances(self):
        """Test finding text instances in PDF."""
        instances = self.processor.find_text_instances(self.test_pdf_path, "John Doe")
        
        self.assertGreater(len(instances), 0)
        self.assertEqual(instances[0]["page_num"], 0)
        self.assertEqual(instances[0]["text"], "John Doe")
    
    def test_apply_redactions(self):
        """Test applying redactions to PDF."""
        # Define redactions
        redactions = [
            {
                "page_num": 0,
                "x0": 50,
                "y0": 40,
                "x1": 150,
                "y1": 60,
                "text": "John Doe",
                "type": "name"
            }
        ]
        
        # Create output path
        output_path = tempfile.mktemp(suffix=".pdf")
        
        try:
            # Apply redactions
            self.processor.apply_redactions(self.test_pdf_path, output_path, redactions)
            
            # Check that output file exists
            self.assertTrue(os.path.exists(output_path))
            
            # Extract text from redacted PDF
            doc = fitz.open(output_path)
            text = doc[0].get_text()
            doc.close()
            
            # Check that the name was redacted
            self.assertNotIn("John Doe", text)
            
        finally:
            # Clean up
            if os.path.exists(output_path):
                os.unlink(output_path)


if __name__ == "__main__":
    unittest.main() 