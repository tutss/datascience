import logging
import sys
from pathlib import Path


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("prompt_magic.log")
        ]
    )
    
    logger = logging.getLogger("prompt_magic")
    logger.info(f"Logging configured at {log_level} level")
    
    return logger


def sanitize_input(text: str, max_length: int = 1000) -> str:
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    sanitized = text.strip()[:max_length]
    
    dangerous_patterns = ["<script", "javascript:", "data:"]
    for pattern in dangerous_patterns:
        if pattern in sanitized.lower():
            raise ValueError("Potentially dangerous input detected")
    
    return sanitized


def validate_audio_file(filename: str, max_size_mb: int = 50) -> bool:
    if not filename:
        return False
    
    allowed_extensions = {'.wav', '.mp3', '.m4a', '.webm', '.flac', '.ogg'}
    file_path = Path(filename)
    
    if file_path.suffix.lower() not in allowed_extensions:
        return False
    
    if file_path.exists():
        size_mb = file_path.stat().st_size / (1024 * 1024)
        if size_mb > max_size_mb:
            return False
    
    return True