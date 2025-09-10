# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Rules

You MUST strictly adhere to the following rules:

- Do not add licenses on READMEs for this repository
- For title and headers, only keep the first word uppercase
- Do not use emojis
- Avoid too many headers when writing markdown files. Keep it concise
- Use simple and straightforward language
- Do not add comments on generated code, when needed, only docstrings
- Use descriptive variable names

# Overview

This is a data science repository containing Jupyter notebooks for machine learning, data analysis, and AI experiments. The repository is organized into two main sections:

### Projects (`projects/`)
Complete, production-ready applications and analysis:
- **Query Rewriter**: Multi-agent text-to-SQL system with Next.js frontend (Mimir UI)
- **Spotify Project**: Brazilian rap music analysis using Spotify API data
- **SSP Data**: Brazilian police data analysis with web scraping
- **Health Analysis**: Nike running data analysis
- **Whisper-CLIP**: Audio-visual AI applications
- **Zotero MCP**: Model Context Protocol server for Zotero integration

### Studies (`studies/`)
Learning materials and experimental code:
- **Algorithms**: Core ML implementations (K-Means, Neural Networks, CatBoost)
- **Torch Studies**: PyTorch experiments (ConvNets, UNet, self-attention)
- **Notebooks**: General data science notebooks and plotting examples
- **ML from A to Z**: Course materials with various ML techniques
- **Agents**: AI agent implementations and research

### Specialized Directories
- **Vision**: Computer vision experiments (face embeddings, attention, vision transformers)
- **Utils**: Utility scripts (PDF conversion, social media tools)

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

### Key Directory Structure
- `projects/`: Complete applications and production analysis
- `studies/`: Learning experiments and educational code
- `vision/`: Computer vision experiments and datasets
- `utils/`: General utility scripts

### File Organization Guidelines
When creating new work:
- **Complete projects**: Place in `projects/[project-name]/`
- **Learning experiments**: Place in `studies/[topic]/`
- **Computer vision work**: Place in `vision/`
- **PyTorch experiments**: Place in `studies/torch-studies/`
- **Utility scripts**: Place in `utils/`

Use descriptive names for notebooks (e.g., `spotify-eda.ipynb`) and kebab-case for project directories.

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

### Development Workflow
Most work is exploratory and done in Jupyter notebooks:
- Start with EDA (Exploratory Data Analysis) notebooks
- Iterate on model training and evaluation
- Extract reusable code into Python modules
- For production code, move to dedicated project directories

### Testing and Validation
No centralized testing framework is configured. Individual projects may have their own test files (e.g., `test.py` in query_rewriter_crew). For data science work, validation is typically done through:
- Cross-validation in notebooks
- Manual inspection of results
- Comparative analysis between models
- Create a plan and revise it with me before executing tasks