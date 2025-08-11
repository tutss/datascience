"""
Claude API client for LLM University Bias Experiment
"""

import anthropic
import os
from typing import Optional
import time
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class ClaudeClient:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Claude client
        
        Args:
            api_key: Anthropic API key. If None, will try to get from environment variable ANTHROPIC_API_KEY
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
        # Rate limiting: 50 calls per minute
        self.call_count = 0
        self.rate_limit = 50
        self.rate_limit_window_start = time.time()
    
    def _check_rate_limit(self):
        """
        Check and enforce rate limiting (50 calls per minute)
        """
        current_time = time.time()
        
        # Reset counter if more than 60 seconds have passed
        if current_time - self.rate_limit_window_start >= 60:
            self.call_count = 0
            self.rate_limit_window_start = current_time
            logger.debug("Rate limit window reset")
        
        # If we've hit the rate limit, sleep for 65 seconds
        if self.call_count >= self.rate_limit:
            sleep_time = 65
            logger.info(f"Rate limit reached ({self.rate_limit} calls). Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
            
            # Reset counter after sleep
            self.call_count = 0
            self.rate_limit_window_start = time.time()
            logger.info("Rate limit reset after sleep")

    def generate_response(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7, model: str = "claude-sonnet-4-20250514") -> str:
        """
        Generate response from Claude
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            model: Claude model to use
        
        Returns:
            Generated response text
        """
        # Check rate limit before making the call
        self._check_rate_limit()
        
        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Increment call count after successful call
            self.call_count += 1
            logger.debug(f"Claude API call successful. Count: {self.call_count}/{self.rate_limit}")
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Error generating Claude response: {e}")
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