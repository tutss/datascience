"""
Response parsing utilities for extracting answers from LLM responses
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class ResponseParser:
    @staticmethod
    def extract_answer_from_xml(response: str) -> Optional[str]:
        """
        Extract answer from XML tags in the response
        
        Args:
            response: Raw response text from LLM
        
        Returns:
            Extracted answer ("yes" or "no") or None if not found
        """
        # Look for <answer>yes</answer> or <answer>no</answer> patterns
        xml_pattern = r'<answer>\s*(yes|no)\s*</answer>'
        match = re.search(xml_pattern, response.lower())
        
        if match:
            return match.group(1).strip().lower()
        
        return None
    
    @staticmethod
    def extract_answer_fallback(response: str) -> Optional[str]:
        """
        Fallback method to extract yes/no answers when XML parsing fails
        
        Args:
            response: Raw response text from LLM
        
        Returns:
            Extracted answer ("yes" or "no") or None if not found
        """
        response_lower = response.lower().strip()
        
        # Check for standalone yes/no at the beginning or end
        if response_lower.startswith('yes') or response_lower.endswith('yes'):
            return 'yes'
        elif response_lower.startswith('no') or response_lower.endswith('no'):
            return 'no'
        
        # Look for "yes" or "no" surrounded by word boundaries
        yes_pattern = r'\byes\b'
        no_pattern = r'\bno\b'
        
        yes_matches = re.findall(yes_pattern, response_lower)
        no_matches = re.findall(no_pattern, response_lower)
        
        # Return the answer if only one type is found
        if yes_matches and not no_matches:
            return 'yes'
        elif no_matches and not yes_matches:
            return 'no'
        
        return None
    
    @staticmethod
    def parse_response(response: str) -> Optional[str]:
        """
        Parse LLM response to extract yes/no answer
        
        Args:
            response: Raw response text from LLM
        
        Returns:
            Extracted answer ("yes" or "no") or None if parsing failed
        """
        if not response or not isinstance(response, str):
            logger.warning("Invalid response provided for parsing")
            return None
        
        # Try XML extraction first
        answer = ResponseParser.extract_answer_from_xml(response)
        if answer:
            logger.debug(f"Successfully extracted answer from XML: {answer}")
            return answer
        
        # Fall back to text parsing
        answer = ResponseParser.extract_answer_fallback(response)
        if answer:
            logger.debug(f"Successfully extracted answer with fallback method: {answer}")
            return answer
        
        logger.warning(f"Failed to parse response: {response[:100]}...")
        return None
    
    @staticmethod
    def validate_answer(answer: Optional[str]) -> bool:
        """
        Validate that the extracted answer is valid
        
        Args:
            answer: Extracted answer string
        
        Returns:
            True if answer is valid ("yes" or "no"), False otherwise
        """
        return answer in ["yes", "no"]