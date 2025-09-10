import logging
import os
import tempfile
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

from .services.audio_service import AudioService
from .services.whisper_service import WhisperService
from .services.prompt_service import PromptService
from .utils import setup_logging, sanitize_input, validate_audio_file

logger = setup_logging()


class PromptRequest(BaseModel):
    user_request: str


class TranscriptionResponse(BaseModel):
    transcription: str


class PromptResponse(BaseModel):
    generated_prompt: str


class FullProcessResponse(BaseModel):
    transcription: str
    generated_prompt: str


class RecordingStatusResponse(BaseModel):
    recording: bool
    duration: float
    available: bool

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Prompt Magic application")
    yield
    logger.info("Shutting down Prompt Magic application")

app = FastAPI(
    title="Prompt Magic", 
    description="Speech-to-text prompt generation",
    lifespan=lifespan
)

# TODO(human)

audio_service = AudioService()
whisper_service = WhisperService()
prompt_service = PromptService()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.get("/api/recording/status")
async def get_recording_status() -> RecordingStatusResponse:
    return RecordingStatusResponse(
        recording=audio_service.recording if audio_service.is_available() else False,
        duration=audio_service.get_audio_duration() if audio_service.is_available() else 0.0,
        available=audio_service.is_available()
    )

@app.post("/api/recording/start")
async def start_recording():
    if not audio_service.is_available():
        raise HTTPException(
            status_code=503, 
            detail="Audio recording not available. PyAudio may not be installed."
        )
    
    try:
        audio_service.start_recording()
        logger.info("Recording started via API")
        return {"status": "recording_started", "message": "Recording started successfully"}
    except Exception as e:
        logger.error(f"Failed to start recording: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start recording: {str(e)}")

@app.post("/api/recording/stop")
async def stop_recording():
    if not audio_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="Audio recording not available"
        )
    
    if not audio_service.recording:
        raise HTTPException(
            status_code=400,
            detail="No recording in progress"
        )
    
    try:
        audio_service.stop_recording()
        duration = audio_service.get_audio_duration()
        logger.info(f"Recording stopped via API, duration: {duration}s")
        return {
            "status": "recording_stopped", 
            "message": "Recording stopped successfully",
            "duration": duration
        }
    except Exception as e:
        logger.error(f"Failed to stop recording: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to stop recording: {str(e)}")

@app.post("/api/recording/process")
async def process_recording() -> FullProcessResponse:
    if not audio_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="Audio recording not available"
        )
    
    if audio_service.recording:
        raise HTTPException(
            status_code=400,
            detail="Recording still in progress. Stop recording first."
        )
    
    if not audio_service.frames:
        raise HTTPException(
            status_code=400,
            detail="No recorded audio to process"
        )
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_service.save_recording(temp_file.name)
            temp_file_path = temp_file.name
        
        transcription = await whisper_service.transcribe(temp_file_path)
        generated_prompt = await prompt_service.generate_prompt(transcription)
        
        os.unlink(temp_file_path)
        
        return FullProcessResponse(
            transcription=transcription,
            generated_prompt=generated_prompt
        )
    
    except Exception as e:
        logger.error(f"Failed to process recording: {e}")
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.post("/api/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)) -> Dict[str, Any]:
    if not audio_file.filename.endswith(('.wav', '.mp3', '.m4a', '.webm')):
        raise HTTPException(status_code=400, detail="Unsupported audio format")
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(audio_file.filename).suffix) as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        transcription = await whisper_service.transcribe(temp_file_path)
        
        os.unlink(temp_file_path)
        
        return {"transcription": transcription}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@app.post("/api/generate-prompt")
async def generate_prompt(data: Dict[str, str]) -> Dict[str, Any]:
    user_request = data.get("user_request", "").strip()
    
    if not user_request:
        raise HTTPException(status_code=400, detail="User request cannot be empty")
    
    try:
        generated_prompt = await prompt_service.generate_prompt(user_request)
        return {"generated_prompt": generated_prompt}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prompt generation failed: {str(e)}")

@app.post("/api/process-full")
async def process_full_pipeline(audio_file: UploadFile = File(...)) -> Dict[str, Any]:
    if not audio_file.filename.endswith(('.wav', '.mp3', '.m4a', '.webm')):
        raise HTTPException(status_code=400, detail="Unsupported audio format")
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(audio_file.filename).suffix) as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        transcription = await whisper_service.transcribe(temp_file_path)
        generated_prompt = await prompt_service.generate_prompt(transcription)
        
        os.unlink(temp_file_path)
        
        return {
            "transcription": transcription,
            "generated_prompt": generated_prompt
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)