import whisper
import torch
from typing import Optional


class WhisperService:
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.model: Optional[whisper.Whisper] = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def _load_model(self) -> whisper.Whisper:
        if self.model is None:
            self.model = whisper.load_model(self.model_size, device=self.device)
        return self.model
    
    async def transcribe(self, audio_path: str) -> str:
        model = self._load_model()
        
        result = model.transcribe(
            audio_path,
            language="en",
            task="transcribe",
            fp16=False if self.device == "cpu" else True
        )
        
        return result["text"].strip()
    
    def transcribe_sync(self, audio_path: str) -> str:
        model = self._load_model()
        
        result = model.transcribe(
            audio_path,
            language="en", 
            task="transcribe",
            fp16=False if self.device == "cpu" else True
        )
        
        return result["text"].strip()
    
    def get_model_info(self) -> dict:
        return {
            "model_size": self.model_size,
            "device": self.device,
            "loaded": self.model is not None
        }