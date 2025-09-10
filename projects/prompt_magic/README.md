# Prompt magic

A speech-to-text application that transforms spoken requirements into well-structured prompts ready for use with AI models.

## Overview

Prompt magic follows a three-step process:
1. **Speech to text**: Uses OpenAI's Whisper model to convert audio recordings into text
2. **Prompt generation**: Uses Claude API to transform user requirements into structured prompts
3. **Copy & paste**: Provides optimized prompts with clear roles, goals, and step-by-step instructions

## Features

- Audio recording with microphone input
- Real-time speech-to-text transcription
- AI-powered prompt optimization
- Web interface for easy interaction
- API endpoints for programmatic access

## Requirements

- Python 3.10+
- Poetry for dependency management
- Anthropic API key for Claude access
- Optional: PyAudio for audio recording (can work without for file uploads)

## Installation

### 1. Clone and setup environment

```bash
cd /path/to/datascience/projects/prompt-magic
poetry install
```

### 2. Install audio dependencies (Optional)

For microphone recording support:
```bash
# macOS
brew install portaudio
poetry install --extras audio

# Ubuntu/Debian  
sudo apt-get install portaudio19-dev python3-pyaudio
poetry install --extras audio

# Windows
# Download PyAudio wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
poetry install --extras audio
```

### 3. Environment configuration

Create `.env` file:
```bash
cp .env.example .env
```

Add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_claude_api_key_here
```

## Usage

### Start the server

```bash
poetry shell
cd prompt_magic
python -m uvicorn main:app --reload --port 8000
```

### Web Interface

Visit http://localhost:8000 to access the web interface.

### API endpoints

#### Live recording workflow
```bash
# Check recording status
GET /api/recording/status

# Start recording
POST /api/recording/start

# Stop recording  
POST /api/recording/stop

# Process recorded audio
POST /api/recording/process
```

#### File upload processing
```bash
# Upload audio file for complete speech-to-prompt processing
POST /api/process-full
curl -X POST -F "audio_file=@recording.wav" http://localhost:8000/api/process-full
```

#### Individual services
```bash
# Transcribe audio to text
POST /api/transcribe
curl -X POST -F "audio_file=@recording.wav" http://localhost:8000/api/transcribe

# Generate prompt from text
POST /api/generate-prompt
curl -X POST -H "Content-Type: application/json" \
  -d '{"user_request": "I need a prompt to help me write better code reviews"}' \
  http://localhost:8000/api/generate-prompt
```

## Supported audio formats

- WAV (recommended)
- MP3
- M4A
- WebM
- FLAC
- OGG

## Architecture

```
prompt_magic/
├── main.py              # FastAPI application
├── services/            # Core business logic
│   ├── audio_service.py # Audio recording/processing
│   ├── whisper_service.py # Speech-to-text
│   └── prompt_service.py # Prompt generation
├── utils.py             # Utility functions
└── static/              # Web frontend files
```

## Development

### Code formatting
```bash
poetry run black .
poetry run flake8 .
```

### Debug mode
Set environment variable for detailed logging:
```bash
export LOG_LEVEL=DEBUG
```

## Troubleshooting

### PyAudio installation issues
If PyAudio installation fails, the application will still work with file uploads:
```bash
poetry install  # Skip --extras audio
```

### Audio device problems
Check available audio devices:
```python
import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))
```

### API key issues
Ensure your Anthropic API key is valid:
```bash
curl -H "Authorization: Bearer $ANTHROPIC_API_KEY" \
     -H "Content-Type: application/json" \
     https://api.anthropic.com/v1/messages
```

## Configuration

### Environment variables
- `ANTHROPIC_API_KEY`: Required for prompt generation
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `MAX_UPLOAD_SIZE`: Maximum audio file size in MB (default: 50)

### Whisper model configuration
Default model: `base` (fast, moderate accuracy)
Available models: `tiny`, `base`, `small`, `medium`, `large`

Larger models provide better accuracy but require more memory and processing time.

## License

This project follows the repository's standard license terms.