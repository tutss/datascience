"""
OpenAI GPT API client for LLM University Bias Experiment
"""

import openai
import os
from typing import Optional
import time
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI client
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment variable OPENAI_API_KEY
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate_response(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7, model: str = "gpt-4") -> str:
        """
        Generate response from GPT
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            model: GPT model to use
        
        Returns:
            Generated response text
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating GPT response: {e}")
            raise
    
    def generate_with_retry(self, prompt: str, max_retries: int = 3, delay: float = 1.0, **kwargs) -> str:
        """
        Generate response with retry logic for rate limiting
        
        Args:
            prompt: The input prompt
            max_retries: Maximum number of retry attempts
            delay: Delay between retries in seconds
            **kwargs: Additional arguments passed to generate_response
        
        Returns:
            Generated response text
        """
        for attempt in range(max_retries + 1):
            try:
                return self.generate_response(prompt, **kwargs)
            except Exception as e:
                if attempt == max_retries:
                    logger.error(f"Failed to generate response after {max_retries} retries: {e}")
                    raise
                
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
        
        raise Exception("This should never be reached")