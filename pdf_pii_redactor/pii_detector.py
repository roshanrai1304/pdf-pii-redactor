"""
PII detection using OpenAI API.
"""

import json
import logging
from typing import List, Dict, Any, Optional
import openai

logger = logging.getLogger(__name__)

class PIIDetector:
    """
    Detects personally identifiable information (PII) in text using OpenAI API.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o", verbose: bool = False):
        """
        Initialize the PII detector.
        
        Args:
            api_key: OpenAI API key
            model: OpenAI model to use
            verbose: Whether to enable verbose logging
        """
        self.model = model
        self.verbose = verbose
        
        if api_key:
            openai.api_key = api_key
        
        # Define PII types to detect
        self.pii_types = [
            "names",
            "email addresses",
            "phone numbers",
            "addresses",
            "credit card numbers",
            "dates of birth"
        ]
    
    def detect_pii(self, text: str, language: str = "en") -> List[Dict[str, Any]]:
        """
        Detect PII in the given text.
        
        Args:
            text: Text to analyze
            language: ISO 639-1 language code
            
        Returns:
            List of dictionaries containing PII type and value
        """
        if not text or len(text.strip()) < 5:
            return []
        
        try:
            # Construct the prompt for PII detection
            prompt = self._create_pii_detection_prompt(text, language)
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                temperature=0.0,  # Use deterministic output
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            content = response.choices[0].message.content
            pii_data = json.loads(content)
            
            if self.verbose:
                logger.info(f"Detected {len(pii_data.get('pii', []))} PII instances")
            
            return pii_data.get("pii", [])
            
        except Exception as e:
            logger.error(f"Error detecting PII: {str(e)}")
            return []
    
    def _create_pii_detection_prompt(self, text: str, language: str) -> Dict[str, str]:
        """
        Create a prompt for PII detection.
        
        Args:
            text: Text to analyze
            language: ISO 639-1 language code
            
        Returns:
            Dictionary with system and user prompts
        """
        system_prompt = f"""You are a privacy protection assistant specialized in identifying personally identifiable information (PII) in documents.
Your task is to identify the following types of PII in the provided text:
- Names (full names, first names, last names)
- Email addresses
- Phone numbers (in any format)
- Physical addresses (street addresses, postal codes, etc.)
- Credit card numbers
- Dates of birth (in any format)

Important: For dates of birth, identify dates that are:
- Explicitly mentioned as birth dates, birthdays, or DOB
- Mentioned in contexts like "I was born on...", "born in...", "date of birth is..."
- Any date clearly referring to when someone was born

Do NOT flag regular dates like meeting dates, document dates, or other temporal references that aren't related to someone's birth.

The text is in {language} language.

Respond with a JSON object containing an array of PII instances found in the text. Each instance should include:
1. "type": The type of PII (name, email, phone, address, credit_card, dob)
2. "value": The exact text that contains the PII
3. "start_index": The character index where this PII starts in the text
4. "end_index": The character index where this PII ends in the text

Format your response as:
{{"pii": [
  {{"type": "name", "value": "John Doe", "start_index": 10, "end_index": 18}},
  ...
]}}

Be thorough and precise. Include all instances of PII you can find. For dates of birth, include any dates that are clearly indicated as someone's birth date or when someone mentions being born on a specific date."""

        user_prompt = f"Please identify all PII in the following text:\n\n{text}"
        
        return {
            "system": system_prompt,
            "user": user_prompt
        } 