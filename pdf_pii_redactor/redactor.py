"""
Main redaction module that coordinates the PII detection and PDF redaction process.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from tqdm import tqdm

from pdf_pii_redactor.pdf_processor import PDFProcessor
from pdf_pii_redactor.pii_detector import PIIDetector
from pdf_pii_redactor.language_detector import LanguageDetector

logger = logging.getLogger(__name__)


class PDFRedactor:
    """
    Coordinates the process of detecting and redacting PII from PDF documents.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None, model: str = "gpt-4o", verbose: bool = False):
        """
        Initialize the PDF redactor.
        
        Args:
            openai_api_key: OpenAI API key
            model: OpenAI model to use
            verbose: Whether to enable verbose logging
        """
        self.verbose = verbose
        
        if verbose:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.WARNING)
        
        # Initialize components
        self.pdf_processor = PDFProcessor(verbose=verbose)
        self.pii_detector = PIIDetector(api_key=openai_api_key, model=model, verbose=verbose)
        self.language_detector = LanguageDetector(verbose=verbose)
    
    def redact_pdf(self, input_path: str, output_path: str) -> Dict[str, Any]:
        """
        Process a PDF file to detect and redact PII.
        
        Args:
            input_path: Path to the input PDF file
            output_path: Path where the redacted PDF will be saved
            
        Returns:
            Dictionary with statistics about the redaction process
        """
        logger.info(f"Starting redaction process for {input_path}")
        
        # Extract text from PDF
        pages = self.pdf_processor.extract_text(input_path)
        
        if not pages:
            logger.warning("No text content found in the PDF")
            return {"redacted_items": 0, "pages_processed": 0}
        
        # Detect document language
        language = self.language_detector.detect_document_language(pages)
        logger.info(f"Detected document language: {language}")
        
        # Process each page to find PII
        all_redactions = []
        
        for page in tqdm(pages, desc="Processing pages", disable=not self.verbose):
            page_num = page["page_num"]
            text = page["text"]
            
            # Detect PII in the page text
            pii_instances = self.pii_detector.detect_pii(text, language)
            
            # For each PII instance, find its position in the PDF
            for pii in pii_instances:
                pii_text = pii["value"]
                
                # Find all instances of this text in the PDF
                text_instances = self.pdf_processor.find_text_instances(input_path, pii_text)
                
                # Add to redactions list
                for instance in text_instances:
                    if instance["page_num"] == page_num:  # Only consider instances on the current page
                        redaction = {
                            "page_num": page_num,
                            "x0": instance["x0"],
                            "y0": instance["y0"],
                            "x1": instance["x1"],
                            "y1": instance["y1"],
                            "text": pii_text,
                            "type": pii["type"]
                        }
                        all_redactions.append(redaction)
        
        # Apply redactions to the PDF
        if all_redactions:
            logger.info(f"Applying {len(all_redactions)} redactions")
            self.pdf_processor.apply_redactions(input_path, output_path, all_redactions)
        else:
            logger.info("No PII found to redact")
            # Create a copy of the original PDF if no redactions
            with open(input_path, "rb") as src, open(output_path, "wb") as dst:
                dst.write(src.read())
        
        # Return statistics
        stats = {
            "redacted_items": len(all_redactions),
            "pages_processed": len(pages),
            "language": language,
            "pii_types_found": list(set(r["type"] for r in all_redactions)) if all_redactions else []
        }
        
        return stats 