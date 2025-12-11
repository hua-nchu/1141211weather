# Specification: GitHub Deployment with Security

## Overview

Deploy the completed CWA Weather Scraper project to GitHub with proper security measures for API key protection.

## Security Requirements

### Environment Variable Implementation

**Goal**: Protect API keys from being exposed in public repositories

**Implementation**:
1. Use `python-dotenv` library to load environment variables
2. Store API key in `.env` file (excluded from Git)
3. Provide `.env.example` template for other users
4. Maintain backward compatibility with fallback to default key

**Technical Design**:
```python
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('CWA_API_KEY', 'default_fallback_key')
```

## Git Configuration

### .gitignore Rules

Required exclusions:
- `.env` - Environment variables (contains secrets)
- `data.db` - Local SQLite database
- `__pycache__/` - Python bytecode
- `*.pyc` - Compiled Python files
- `.vscode/`, `.idea/` - IDE configurations
- `.gemini/` - Gemini Agent directory

### Repository Structure

Files to be tracked:
- All Python source files
- `requirements.txt` (including python-dotenv)
- `.env.example` (template only)
- `.gitignore`
- Documentation (README.md, prompt.md)
- OpenSpec records

## Documentation Requirements

### README.md Updates

Must include:
1. API key setup instructions
2. Environment variable configuration steps
3. Security warnings about `.env` file
4. Example using course-provided demo key

### Setup Instructions

Users must be able to:
1. Clone the repository
2. Copy `.env.example` to `.env`
3. Configure their API key
4. Run the application without code modifications

## Deployment Process

### Initial Commit

Commit message format:
```
Initial commit: CWA Weather Scraper with enhanced visualization

- API data fetching with environment variable security
- SQLite database with batch management
- Streamlit app with CWA-style design
- Enhanced Taiwan map with heatmap and animation
- Complete documentation and OpenSpec records
```

### GitHub Repository

- **URL**: https://github.com/hua-nchu/1141211weather.git
- **Branch**: main
- **Visibility**: Public (with proper .gitignore)

## Success Criteria

- [x] API key not visible in any committed files
- [x] `.env` file excluded from Git
- [x] All source code files uploaded
- [x] Documentation complete and accessible
- [x] Repository cloneable and runnable by others
- [x] Security measures documented in README

## Dependencies

New dependency added:
- `python-dotenv>=1.0.0`

## Files Modified

1. `fetch_weather.py` - Environment variable support
2. `requirements.txt` - Added python-dotenv
3. `.gitignore` - Added .env exclusion
4. `README.md` - API key setup instructions

## Files Created

1. `.env.example` - Environment variable template
2. `.env` - Local configuration (not tracked)
