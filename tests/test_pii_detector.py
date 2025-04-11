"""
Tests for the PII detection functionality.
"""

import os
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_pii_redactor.pii_detector import PIIDetector

from dotenv import load_dotenv

load_dotenv()


class TestPIIDetector(unittest.TestCase):
    """Test cases for the PII detector."""
    
    def setUp(self):
        """Set up test environment."""
        # Skip tests if no API key is available
        if "OPENAI_API_KEY" not in os.environ:
            self.skipTest("OPENAI_API_KEY environment variable not set")
        
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.detector = PIIDetector(api_key=self.api_key, verbose=True)
    
    def test_detect_pii_empty_text(self):
        """Test PII detection with empty text."""
        result = self.detector.detect_pii("")
        self.assertEqual(len(result), 0)
    
    def test_detect_pii_no_pii(self):
        """Test PII detection with text containing no PII."""
        text = "This is a sample text with no personally identifiable information."
        result = self.detector.detect_pii(text)
        self.assertEqual(len(result), 0)
    
    def test_detect_pii_with_email(self):
        """Test PII detection with text containing an email address."""
        text = "Please contact me at john.doe@example.com for more information."
        result = self.detector.detect_pii(text)
        
        self.assertGreater(len(result), 0)
        
        # Check if at least one email was detected
        email_detected = False
        for pii in result:
            if pii["type"] == "email" and "john.doe@example.com" in pii["value"]:
                email_detected = True
                break
        
        self.assertTrue(email_detected)
    
    def test_detect_pii_with_phone(self):
        """Test PII detection with text containing a phone number."""
        text = "Call me at (555) 123-4567 or +1-555-123-4567."
        result = self.detector.detect_pii(text)
        
        self.assertGreater(len(result), 0)
        
        # Check if at least one phone number was detected
        phone_detected = False
        for pii in result:
            if pii["type"] == "phone":
                phone_detected = True
                break
        
        self.assertTrue(phone_detected)
    
    def test_detect_pii_with_name(self):
        """Test PII detection with text containing a name."""
        text = "My name is John Smith and I work at Acme Corporation."
        result = self.detector.detect_pii(text)
        
        self.assertGreater(len(result), 0)
        
        # Check if at least one name was detected
        name_detected = False
        for pii in result:
            if pii["type"] == "name" and "John Smith" in pii["value"]:
                name_detected = True
                break
        
        self.assertTrue(name_detected)
    
    def test_detect_pii_with_address(self):
        """Test PII detection with text containing an address."""
        text = "I live at 123 Main St, Anytown, CA 12345."
        result = self.detector.detect_pii(text)
        
        self.assertGreater(len(result), 0)
        
        # Check if at least one address was detected
        address_detected = False
        for pii in result:
            if pii["type"] == "address":
                address_detected = True
                break
        
        self.assertTrue(address_detected)
    
    def test_detect_pii_with_credit_card(self):
        """Test PII detection with text containing a credit card number."""
        text = "My credit card number is 4111 1111 1111 1111."
        result = self.detector.detect_pii(text)
        
        self.assertGreater(len(result), 0)
        
        # Check if at least one credit card was detected
        cc_detected = False
        for pii in result:
            if pii["type"] == "credit_card":
                cc_detected = True
                break
        
        self.assertTrue(cc_detected)
    
    def test_detect_pii_with_dob(self):
        """Test PII detection with text containing a date of birth."""
        text = "I was born on January 15, 1980."
        result = self.detector.detect_pii(text)
        
        self.assertGreater(len(result), 0)
        
        # Check if at least one date of birth was detected
        dob_detected = False
        for pii in result:
            if pii["type"] == "dob":
                dob_detected = True
                break
        
        self.assertTrue(dob_detected)


if __name__ == "__main__":
    unittest.main() 