"""
Utility functions for the PDF PII Redactor.
"""

import os
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


def validate_pdf(file_path: str) -> bool:
    """
    Validate that a file is a PDF.
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        True if the file is a valid PDF, False otherwise
    """
    if not os.path.exists(file_path):
        logger.error(f"File does not exist: {file_path}")
        return False
    
    if not os.path.isfile(file_path):
        logger.error(f"Path is not a file: {file_path}")
        return False
    
    if not file_path.lower().endswith('.pdf'):
        logger.error(f"File is not a PDF: {file_path}")
        return False
    
    # Check if file is readable
    try:
        with open(file_path, 'rb') as f:
            header = f.read(5)
            if header != b'%PDF-':
                logger.error(f"File does not have a valid PDF header: {file_path}")
                return False
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        return False
    
    return True


def group_by_type(pii_instances: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group PII instances by type.
    
    Args:
        pii_instances: List of PII instances
        
    Returns:
        Dictionary with PII types as keys and lists of instances as values
    """
    result = {}
    
    for pii in pii_instances:
        pii_type = pii.get("type")
        if pii_type:
            if pii_type not in result:
                result[pii_type] = []
            result[pii_type].append(pii)
    
    return result 