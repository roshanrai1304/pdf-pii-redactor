"""
PDF processing utilities for extracting and modifying PDF content.
"""

import fitz  # PyMuPDF
import logging
from typing import List, Dict, Tuple, Any, Optional

logger = logging.getLogger(__name__)


class PDFProcessor:
    """
    Handles PDF document processing, including text extraction and redaction.
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the PDF processor.
        
        Args:
            verbose: Whether to enable verbose logging
        """
        self.verbose = verbose
        if verbose:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.WARNING)
    
    def extract_text(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract text content from a PDF file, preserving page structure.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries containing page number and text content
        """
        pages = []
        
        try:
            doc = fitz.open(pdf_path)
            
            for page_num, page in enumerate(doc):
                text = page.get_text()
                if text.strip():  # Only add pages with actual text content
                    pages.append({
                        "page_num": page_num,
                        "text": text,
                        "width": page.rect.width,
                        "height": page.rect.height
                    })
            
            logger.info(f"Extracted text from {len(pages)} pages")
            return pages
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise
    
    def apply_redactions(self, pdf_path: str, output_path: str, 
                         redactions: List[Dict[str, Any]]) -> None:
        """
        Apply redactions to a PDF file and save the result.
        
        Args:
            pdf_path: Path to the original PDF file
            output_path: Path where the redacted PDF will be saved
            redactions: List of redaction instructions
        """
        try:
            doc = fitz.open(pdf_path)
            
            # Group redactions by page
            redactions_by_page = {}
            for redaction in redactions:
                page_num = redaction["page_num"]
                if page_num not in redactions_by_page:
                    redactions_by_page[page_num] = []
                redactions_by_page[page_num].append(redaction)
            
            # Apply redactions page by page
            for page_num, page_redactions in redactions_by_page.items():
                page = doc[page_num]
                
                # First, mark all redactions
                for redaction in page_redactions:
                    rect = fitz.Rect(
                        redaction["x0"], 
                        redaction["y0"], 
                        redaction["x1"], 
                        redaction["y1"]
                    )
                    # Mark text for redaction
                    page.add_redact_annot(rect, text=" ")
                
                # Then apply all redactions at once
                page.apply_redactions()
                
                if self.verbose:
                    logger.info(f"Applied {len(page_redactions)} redactions to page {page_num}")
            
            # Save the redacted document
            doc.save(output_path)
            doc.close()
            
            logger.info(f"Saved redacted PDF to {output_path}")
            
        except Exception as e:
            logger.error(f"Error applying redactions: {str(e)}")
            raise
    
    def find_text_instances(self, pdf_path: str, text_to_find: str) -> List[Dict[str, Any]]:
        """
        Find all instances of a specific text in the PDF and return their positions.
        
        Args:
            pdf_path: Path to the PDF file
            text_to_find: Text to search for
            
        Returns:
            List of dictionaries with page number and rectangle coordinates
        """
        instances = []
        
        try:
            doc = fitz.open(pdf_path)
            
            for page_num, page in enumerate(doc):
                text_instances = page.search_for(text_to_find)
                
                for rect in text_instances:
                    instances.append({
                        "page_num": page_num,
                        "x0": rect.x0,
                        "y0": rect.y0,
                        "x1": rect.x1,
                        "y1": rect.y1,
                        "text": text_to_find
                    })
            
            if self.verbose:
                logger.info(f"Found {len(instances)} instances of '{text_to_find}'")
            
            return instances
            
        except Exception as e:
            logger.error(f"Error searching for text: {str(e)}")
            raise 