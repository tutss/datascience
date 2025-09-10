import logging
import threading
import time
from typing import Optional
import wave

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    pyaudio = None

logger = logging.getLogger("prompt_magic.audio")


class AudioService:
    def __init__(self):
        if not PYAUDIO_AVAILABLE:
            logger.warning("PyAudio not available. Audio recording will not work.")
            self.available = False
            return
        
        self.available = True
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.recording = False
        self.frames = []
        self.stream: Optional[pyaudio.Stream] = None
        self.audio: Optional[pyaudio.PyAudio] = None
        self._record_thread = None

    def start_recording(self) -> None:
        if not self.available:
            raise RuntimeError("Audio service not available. PyAudio may not be installed.")
        
        if self.recording:
            logger.warning("Recording already in progress")
            return
        
        try:
            self.recording = True
            self.frames = []
            self.audio = pyaudio.PyAudio()
            
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            def record_audio():
                try:
                    while self.recording:
                        if self.stream and not self.stream.is_stopped():
                            data = self.stream.read(self.chunk, exception_on_overflow=False)
                            self.frames.append(data)
                        else:
                            break
                except Exception as e:
                    logger.error(f"Error during audio recording: {e}")
                    self.recording = False
            
            self._record_thread = threading.Thread(target=record_audio, daemon=True)
            self._record_thread.start()
            logger.info("Audio recording started")
            
        except Exception as e:
            logger.error(f"Failed to start audio recording: {e}")
            self._cleanup()
            raise RuntimeError(f"Could not start audio recording: {e}")

    def stop_recording(self) -> None:
        if not self.recording:
            logger.warning("No recording in progress")
            return
        
        logger.info("Stopping audio recording")
        self.recording = False
        
        if self._record_thread and self._record_thread.is_alive():
            self._record_thread.join(timeout=2.0)
        
        self._cleanup()

    def _cleanup(self) -> None:
        try:
            if self.stream:
                if not self.stream.is_stopped():
                    self.stream.stop_stream()
                self.stream.close()
                self.stream = None
        except Exception as e:
            logger.error(f"Error closing audio stream: {e}")
        
        try:
            if self.audio:
                self.audio.terminate()
                self.audio = None
        except Exception as e:
            logger.error(f"Error terminating PyAudio: {e}")
        
        self._record_thread = None

    def save_recording(self, filename: str) -> None:
        if not self.available:
            raise RuntimeError("Audio service not available")
        
        if not self.frames:
            raise ValueError("No audio data to save")
        
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(pyaudio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.frames))
            logger.info(f"Audio saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save audio to {filename}: {e}")
            raise

    def get_audio_duration(self) -> float:
        if not self.frames:
            return 0.0
        
        total_samples = len(self.frames) * self.chunk
        return total_samples / self.rate
    
    def is_available(self) -> bool:
        return self.available and PYAUDIO_AVAILABLE