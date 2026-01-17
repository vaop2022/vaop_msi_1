# VAOP MSI v0.1

Methodological Sustainability Index Calculator

A professional engineering tool for calculating the Methodological Sustainability Index (MSI) of codebases using static analysis and AI-powered semantic analysis.

## Architecture

This project follows a **Clean Layered Architecture** (Onion/Hexagonal inspired) to ensure core logic is independent of external tools.

See [docs/01_architecture_overview.md](docs/01_architecture_overview.md) for detailed architecture documentation.

## Quick Start

See [docs/02_setup_guide.md](docs/02_setup_guide.md) for complete setup instructions.

### Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Usage

```bash
# Basic usage (with AI analysis)
python -m src.main audit <path-to-repository>

# Output results as JSON
python -m src.main audit <path-to-repository> --output json > results.json

# Skip AI analysis (faster, uses only static analysis)
python -m src.main audit <path-to-repository> --no-ai

# Provide API key directly
python -m src.main audit <path-to-repository> --api-key YOUR_KEY
```

**Note:** For AI analysis, you need a `GEMINI_API_KEY` in your `.env` file or passed via `--api-key` flag.

## Project Structure

```
vaop_msi_1/
├── docs/                       # Documentation & Guidelines
├── src/                        # Source Code
│   ├── domain/                 # Core logic, data models (Pure Python)
│   ├── adapters/               # External tools wrappers (Infrastructure)
│   ├── services/               # Business Logic (Orchestrator)
│   └── main.py                 # Entry point (CLI)
├── tests/                      # Unit tests
└── requirements.txt
```

## License

[To be determined]

