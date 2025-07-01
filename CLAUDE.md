# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a data science repository containing Jupyter notebooks for machine learning, data analysis, and AI experiments. It includes several distinct projects:

- **Machine Learning Experiments**: Jupyter notebooks for various ML algorithms (K-Means, Neural Networks, CatBoost, etc.)
- **Spotify Project**: Brazilian rap music analysis using Spotify API data
- **Vision**: Computer vision experiments including face embeddings and attention mechanisms
- **Query Rewriter**: Multi-agent system for text-to-SQL with Next.js frontend (Mimir UI)
- **Torch Studies**: PyTorch experiments including ConvNets, UNet, and image inpainting
- **SSP Data**: Brazilian police data analysis with web scraping
- **Whisper-CLIP**: Audio-visual AI applications

## Environment Setup

### Python Environment
The project uses Poetry for Python dependency management:

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

Main Python dependencies:
- numpy ^2.1.3
- torch ^2.5.1
- matplotlib ^3.9.3
- Python ^3.10, <3.13

### Next.js Projects
For the Mimir UI frontend (query-rewriter/mimir-ui/):

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Lint code
npm run lint
```

## Development Commands

### Python Projects
```bash
# Run Jupyter notebooks
jupyter notebook

# Run Python scripts
python <script_name>.py

# For query-rewriter crew
cd agents/query-rewriter/query_rewriter_crew
uvicorn app:app --reload --port 8000
```

### Next.js Frontend (Mimir UI)
```bash
cd agents/query-rewriter/mimir-ui
npm run dev    # Development server on localhost:3000
npm run build  # Production build
npm run start  # Production server
npm run lint   # ESLint
```

### Spotify Project
Requires environment variables:
- SPOTIPY_CLIENT_ID
- SPOTIPY_CLIENT_SECRET

```bash
cd spotify-project
python api_caller.py  # Collect data from Spotify API
```

## Architecture Overview

### Multi-Agent Query Rewriter System
- **Backend**: FastAPI application with CrewAI agents (`agents/query-rewriter/query_rewriter_crew/`)
- **Frontend**: Next.js with TypeScript and Tailwind CSS (`agents/query-rewriter/mimir-ui/`)
- **API Integration**: Axios for HTTP requests, proxy configuration in next.config.js

### Data Science Workflows
- **Notebooks**: Organized by topic (algorithms/, notebooks/, plot_notebooks/)
- **Deep Learning**: PyTorch-based experiments in torch-studies/
- **Computer Vision**: Face recognition, attention mechanisms, image datasets
- **Data Analysis**: EDA notebooks with pandas, matplotlib, seaborn

### Project Structure
- `agents/`: AI agent implementations and MCP servers
- `algorithms/`: Core ML algorithm implementations
- `notebooks/`: General data science notebooks
- `spotify-project/`: Music data analysis pipeline
- `vision/`: Computer vision experiments
- `torch-studies/`: PyTorch deep learning projects
- `ssp-data/`: Brazilian crime data analysis
- `whisper-clip/`: Multimodal AI applications

## Development Notes

### Jupyter Notebooks
Most analysis work is done in Jupyter notebooks. Common patterns:
- EDA (Exploratory Data Analysis) notebooks
- Model training and evaluation
- Data preprocessing pipelines
- Visualization and plotting

### API Integration
- Spotify API for music data collection
- FastAPI for backend services
- MCP (Model Context Protocol) servers for Zotero integration

### Data Sources
- Spotify API for music features and playlists
- Oxford-IIIT Pet Dataset for computer vision
- Brazilian SSP (Public Security) data for crime analysis
- Custom datasets for various ML experiments

### Testing and Validation
No centralized testing framework is configured. Individual projects may have their own test files (e.g., `test.py` in query_rewriter_crew).