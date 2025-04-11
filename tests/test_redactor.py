"""
Tests for the PDF redaction functionality.
"""

import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_pii_redactor.redactor import PDFRedactor
from pdf_pii_redactor.pdf_processor import PDFProcessor

from dotenv import load_dotenv

load_dotenv()


class TestRedactor(unittest.TestCase):
    """Test cases for the PDF redactor."""
    
    def setUp(self):
        """Set up test environment."""
        # Skip tests if no API key is available
        if "OPENAI_API_KEY" not in os.environ:
            self.skipTest("OPENAI_API_KEY environment variable not set")
        
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.redactor = PDFRedactor(openai_api_key=self.api_key, verbose=True)
    
    def test_pdf_extraction(self):
        """Test PDF text extraction."""
        # This test requires a sample PDF file
        # You should create a sample PDF with known content for testing
        sample_pdf_path = r"C:\Users\rossh\Documents\Projects\Coral Project\example_pdfs\example_3.pdf"
        
        # Skip if test file doesn't exist
        if not os.path.exists(sample_pdf_path):
            self.skipTest(f"Test file {sample_pdf_path} not found")
        
        processor = PDFProcessor(verbose=True)
        pages = processor.extract_text(sample_pdf_path)
        
        self.assertIsNotNone(pages)
        self.assertGreater(len(pages), 0)
        self.assertIn("text", pages[0])
    
    def test_redaction_process(self):
        """Test the complete redaction process."""
        # This test requires a sample PDF file with PII
        sample_pdf_path = r"C:\Users\rossh\Documents\Projects\Coral Project\example_pdfs\example_3.pdf"
        
        # Skip if test file doesn't exist
        if not os.path.exists(sample_pdf_path):
            self.skipTest(f"Test file {sample_pdf_path} not found")
        
        # Create a temporary file for the output
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            output_path = temp_file.name
        
        try:
            # Run the redaction process
            stats = self.redactor.redact_pdf(sample_pdf_path, output_path)
            
            # Check that the output file exists
            self.assertTrue(os.path.exists(output_path))
            
            # Check that we got some statistics back
            self.assertIn("redacted_items", stats)
            self.assertIn("pages_processed", stats)
            
        finally:
            # Clean up the temporary file
            if os.path.exists(output_path):
                os.unlink(output_path)


if __name__ == "__main__":
    unittest.main() 