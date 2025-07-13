# Data Science Repository

A collection of data science projects, machine learning experiments, and AI applications organized by topic and complexity.

## Repository Structure

### Projects (`projects/`)

- **Query Rewriter**: Multi-agent text-to-SQL system with Next.js frontend
- **Spotify Project**: Brazilian rap music analysis using Spotify API
- **SSP Data**: Brazilian police data analysis with web scraping
- **Health Analysis**: Nike running data analysis
- **Whisper-CLIP**: Multimodal AI applications combining audio and visual processing
- **Zotero MCP**: Model Context Protocol server for Zotero integration (https://github.com/tutss/zotero-mcp-server)

### Studies (`studies/`)
Learning materials and experimental code organized by topic:
- **Algorithms**: Core ML implementations (K-Means, Neural Networks, CatBoost)
- **Torch Studies**: PyTorch experiments (ConvNets, UNet, self-attention)
- **Notebooks**: General data science notebooks and plotting examples
- **ML from A to Z**: Course materials with various ML techniques
- **Agents**: AI agent implementations and research

### Specialized Directories
- **Vision**: Computer vision experiments (face embeddings, attention, vision transformers, Oxford-IIIT Pet dataset)
- **Utils**: Utility scripts (PDF conversion, social media tools)

## Environment Setup

Uses Poetry for Python dependency management:
```bash
poetry install  # Install dependencies
poetry shell    # Activate environment
```

## File Organization Guidelines

### Where to Save New Work

- **Complete projects**: `projects/[project-name]/`
- **Learning experiments**: `studies/[topic]/`
- **Computer vision work**: `vision/`
- **PyTorch experiments**: `studies/torch-studies/`
- **Data analysis notebooks**: `studies/notebooks/`
- **Algorithm implementations**: `studies/algorithms/`
- **Utility scripts**: `utils/`

### Naming Conventions

- Jupyter notebooks: descriptive names (e.g., `spotify-eda.ipynb`, `face-recognition-training.ipynb`)
- Projects: use kebab-case for directories
- Python files: snake_case for scripts and modules
- Data files: include date stamps when versioning (e.g., `df_2022-06-12.csv`)

See individual project READMEs for specific setup instructions.