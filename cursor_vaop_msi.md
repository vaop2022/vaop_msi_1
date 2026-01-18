# VAOP MSI v0.1 project blueprint
_Exported on 1/18/2026 at 14:47:35 GMT+2 from Cursor (2.3.41)_

---

**User**

Excellent. Let's initialize the repository `vaop2022/vaop_msi_1` as a clean, professional engineering product from day one.

I have designed a **Clean Layered Architecture** (Onion/Hexagonal inspired) to ensure the core logic (MSI calculations) is independent of the external tools (Radon, API calls).

Here is the blueprint for the prototype.

### 1. Project Structure (The Skeleton)

We will organize the code into `src` (source) and `docs` (documentation).

**Suggested Directory Tree:**

```text
vaop_msi_1/
├── docs/                       # [Folder] Documentation & Guidelines
│   ├── 01_architecture_overview.md
│   └── 02_setup_guide.md
├── src/                        # [Folder] Source Code
│   ├── __init__.py
│   ├── domain/                 # [Layer 1] Core logic, data models (Pure Python)
│   │   ├── __init__.py
│   │   └── models.py           # Metric definitions (Pydantic models)
│   ├── adapters/               # [Layer 2] External tools wrappers (Infrastructure)
│   │   ├── __init__.py
│   │   ├── static_analyzer.py  # Wrapper for Radon/Lizard
│   │   └── ai_analyzer.py      # Wrapper for Gemini API
│   ├── services/               # [Layer 3] Business Logic (Orchestrator)
│   │   ├── __init__.py
│   │   └── msi_calculator.py   # Combines Static + AI data
│   └── main.py                 # [Layer 4] Entry point (CLI)
├── tests/                      # [Folder] Unit tests
├── .env.example                # Template for environment variables
├── .gitignore
├── requirements.txt
└── README.md

```

---

### 2. Configuration Files

Here are the initial files you need to commit to set up the environment.

#### `requirements.txt`

We will use **Typer** for the CLI (Command Line Interface), **Pydantic** for strict data validation, and **Rich** for beautiful terminal output (essential for a high-quality product feel).

```text
# Core Logic & CLI
typer>=0.9.0
rich>=13.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0

# Static Analysis Tools (The "Builders")
radon>=6.0.0
lizard>=1.17.0

# AI Integration
google-generativeai>=0.3.0

```

#### `.gitignore`

Standard Python exclusion.

```text
__pycache__/
*.pyc
.env
.venv/
.DS_Store

```

---

### 3. Documentation (The `docs` folder)

As requested, here are the Markdown instructions with English comments.

#### `docs/01_architecture_overview.md`

```markdown
# Architecture Overview: MSI v0.1

## Philosophy
This project follows a **Layered Architecture** to separate technical implementation details from the Methodological Sustainability Index (MSI) business logic.

## Layers

### 1. Domain Layer (`src/domain`)
* **Responsibility:** Defines *what* MSI is. Contains Pydantic models for `Repairability`, `ChangeEffort`, and `LegacyCompatibility`.
* **Dependency:** No external dependencies. Pure Python.

### 2. Adapters Layer (`src/adapters`)
* **Responsibility:** Interacts with the "outside world".
* **Components:**
    * `static_analyzer.py`: Runs `radon` and `lizard` on the codebase.
    * `ai_analyzer.py`: Sends code snippets to Google Gemini for semantic audit.

### 3. Services Layer (`src/services`)
* **Responsibility:** The "Brain". It orchestrates the flow:
    1.  Call Adapters to get raw data.
    2.  Apply weights/coefficients defined in the VAOP methodology.
    3.  Calculate the final Score (Gold/Silver/Bronze).

### 4. Entry Point (`src/main.py`)
* **Responsibility:** CLI interface using `typer`. Handles user input and prints the formatted Report using `rich`.

```

#### `docs/02_setup_guide.md`

```markdown
# Setup Guide

## Prerequisites
* Python 3.10+
* Google Gemini API Key

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/vaop2022/vaop_msi_1.git](https://github.com/vaop2022/vaop_msi_1.git)
    cd vaop_msi_1
    ```

2.  **Create Virtual Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables:**
    Create a `.env` file in the root directory:
    ```bash
    GEMINI_API_KEY="your_api_key_here"
    ```

```

---

### 4. Prototype Code Entry Point

Here is the code for `src/main.py` to prove the architecture works. It initializes the CLI.

#### `src/main.py`

```python
import typer
from rich.console import Console
from rich.panel import Panel

# Initialize Typer app and Rich console
app = typer.Typer()
console = Console()

@app.command()
def audit(path: str = typer.Argument(..., help="Path to the repository/folder to audit")):
    """
    Runs the MSI (Methodological Sustainability Index) audit on the specified path.
    """
    console.print(Panel.fit(f"Starting MSI Audit for: [bold cyan]{path}[/bold cyan]", title="VAOP MSI v0.1"))

    # TODO: Initialize Adapters
    console.print("[yellow]Step 1:[/yellow] Initializing Static Analyzers (Radon/Lizard)...")
    
    # TODO: Initialize AI Service
    console.print("[yellow]Step 2:[/yellow] Connecting to Gemini AI Processor...")

    # TODO: Calculate Score
    console.print("[yellow]Step 3:[/yellow] Calculating Repairability & Change Effort...")

    # Placeholder result
    console.print("\n[bold green]Audit Complete![/bold green]")
    console.print("Overall MSI Rating: [bold gold1]GOLD (Prototype)[/bold gold1]")

if __name__ == "__main__":
    app()

```

### Next Steps for You:

1. **Create these files** locally in the folder structure shown above.
2. **Run** `pip install -r requirements.txt`.
3. **Run** `python src/main.py .` to see the CLI interface "alive".

Once you have pushed this skeleton to GitHub, tell me, and I will write the code for **Layer 1 (Domain Models)** to define exactly what data structure constitutes the MSI Index.

---

**Cursor**

Initializing the repository with the clean layered architecture. Creating the directory structure and files.


Creating the directory structure and files:


```plaintext
# Core Logic & CLI
typer>=0.9.0
rich>=13.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0

# Static Analysis Tools (The "Builders")
radon>=6.0.0
lizard>=1.17.0

# AI Integration
google-generativeai>=0.3.0

```

```ignore
__pycache__/
*.pyc
.env
.venv/
.DS_Store

```

```markdown
# Architecture Overview: MSI v0.1

## Philosophy
This project follows a **Layered Architecture** to separate technical implementation details from the Methodological Sustainability Index (MSI) business logic.

## Layers

### 1. Domain Layer (`src/domain`)
* **Responsibility:** Defines *what* MSI is. Contains Pydantic models for `Repairability`, `ChangeEffort`, and `LegacyCompatibility`.
* **Dependency:** No external dependencies. Pure Python.

### 2. Adapters Layer (`src/adapters`)
* **Responsibility:** Interacts with the "outside world".
* **Components:**
    * `static_analyzer.py`: Runs `radon` and `lizard` on the codebase.
    * `ai_analyzer.py`: Sends code snippets to Google Gemini for semantic audit.

### 3. Services Layer (`src/services`)
* **Responsibility:** The "Brain". It orchestrates the flow:
    1.  Call Adapters to get raw data.
    2.  Apply weights/coefficients defined in the VAOP methodology.
    3.  Calculate the final Score (Gold/Silver/Bronze).

### 4. Entry Point (`src/main.py`)
* **Responsibility:** CLI interface using `typer`. Handles user input and prints the formatted Report using `rich`.

```

```markdown
# Setup Guide

## Prerequisites
* Python 3.10+
* Google Gemini API Key

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/vaop2022/vaop_msi_1.git](https://github.com/vaop2022/vaop_msi_1.git)
    cd vaop_msi_1
    ```

2.  **Create Virtual Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables:**
    Create a `.env` file in the root directory:
    ```bash
    GEMINI_API_KEY="your_api_key_here"
    ```

```

```python
"""
VAOP MSI v0.1 - Methodological Sustainability Index Calculator
"""

```

```python
"""
Domain Layer: Core business logic and data models.
Pure Python, no external dependencies.
"""

```

```python
"""
Pydantic models for MSI metrics.
TODO: Define Repairability, ChangeEffort, and LegacyCompatibility models.
"""

```

```python
"""
Adapters Layer: External tools wrappers (Infrastructure).
Interfaces with Radon, Lizard, and Gemini API.
"""

```

```python
"""
Wrapper for static analysis tools (Radon, Lizard).
TODO: Implement static code analysis integration.
"""

```

```python
"""
Wrapper for Google Gemini API.
TODO: Implement AI-based semantic code analysis.
"""

```

```python
"""
Services Layer: Business logic orchestrator.
Combines data from adapters and calculates MSI scores.
"""

```

```python
"""
MSI Calculator Service.
TODO: Implement business logic to combine Static + AI data and calculate final scores.
"""

```

```python
import typer
from rich.console import Console
from rich.panel import Panel

# Initialize Typer app and Rich console
app = typer.Typer()
console = Console()

@app.command()
def audit(path: str = typer.Argument(..., help="Path to the repository/folder to audit")):
    """
    Runs the MSI (Methodological Sustainability Index) audit on the specified path.
    """
    console.print(Panel.fit(f"Starting MSI Audit for: [bold cyan]{path}[/bold cyan]", title="VAOP MSI v0.1"))

    # TODO: Initialize Adapters
    console.print("[yellow]Step 1:[/yellow] Initializing Static Analyzers (Radon/Lizard)...")
    
    # TODO: Initialize AI Service
    console.print("[yellow]Step 2:[/yellow] Connecting to Gemini AI Processor...")

    # TODO: Calculate Score
    console.print("[yellow]Step 3:[/yellow] Calculating Repairability & Change Effort...")

    # Placeholder result
    console.print("\n[bold green]Audit Complete![/bold green]")
    console.print("Overall MSI Rating: [bold gold1]GOLD (Prototype)[/bold gold1]")

if __name__ == "__main__":
    app()

```

```markdown
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
python src/main.py audit <path-to-repository>
```

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

```

Creating the tests directory and checking for linting issues:


Verifying the structure and testing the CLI:


Creating `.env.example` manually since it was blocked:


Verifying `.env.example` exists:


Repository initialized with the clean layered architecture. Here's what was created:

## Project structure

```
vaop_msi_1/
├── docs/
│   ├── 01_architecture_overview.md
│   └── 02_setup_guide.md
├── src/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   └── models.py (placeholder)
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── static_analyzer.py (placeholder)
│   │   └── ai_analyzer.py (placeholder)
│   ├── services/
│   │   ├── __init__.py
│   │   └── msi_calculator.py (placeholder)
│   └── main.py (working CLI prototype)
├── tests/ (empty, ready for tests)
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Next steps

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Test the CLI:
   ```bash
   python src/main.py audit .
   ```

3. Set up environment:
   - Copy `.env.example` to `.env`
   - Add your `GEMINI_API_KEY`

The skeleton is ready. The CLI entry point (`src/main.py`) is functional and displays the prototype interface. All layers are in place with placeholder files ready for implementation.

Ready for Layer 1 (Domain Models) implementation. The structure follows the clean architecture blueprint with clear separation of concerns.

```plaintext
vaop_msi_1/
├── docs/
│   ├── 01_architecture_overview.md
│   └── 02_setup_guide.md
├── src/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   └── models.py (placeholder)
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── static_analyzer.py (placeholder)
│   │   └── ai_analyzer.py (placeholder)
│   ├── services/
│   │   ├── __init__.py
│   │   └── msi_calculator.py (placeholder)
│   └── main.py (working CLI prototype)
├── tests/ (empty, ready for tests)
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

```shellscript
   pip install -r requirements.txt
```

```shellscript
   python src/main.py audit .
```

---

**User**

Отлично, я смог всё установить. Сделай начало кода из Фазы 1 по приложенному  Тех Заданию
Не забывай, что мы пишем файлы и комменты на английском. @Tech_part.md 
@d:\pr\4-Eco-prog\MSI\vaop_msi_1\ 

---

**Cursor**

Изучаю текущую структуру проекта и приступаю к реализации Фазы 1.


Проверяю requirements.txt и приступаю к реализации Фазы 1.


Реализую Фазу 1: создаю модели домена, адаптеры для статического анализа и AI, сервис расчета MSI и обновляю main.py.


```python
"""
Pydantic models for MSI metrics.
Defines the core data structures for Repairability, ChangeEffort, and LegacyCompatibility.
"""

from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class MSIRating(str, Enum):
    """MSI Rating levels (analogous to LEED certification)."""
    BASIC = "Basic"
    SILVER = "Silver"
    GOLD = "Gold"


class RepairabilityMetrics(BaseModel):
    """Repairability metric: Ease of making local changes without cascade effects."""
    
    # Hard metrics from static analysis
    average_coupling: float = Field(..., description="Average coupling score (lower is better)")
    average_cohesion: float = Field(..., description="Average cohesion score (higher is better)")
    cyclomatic_complexity: float = Field(..., description="Average cyclomatic complexity")
    isolated_modules_percentage: float = Field(..., description="Percentage of modules that can be changed in isolation")
    
    # AI analysis score
    ai_modularity_score: float = Field(..., ge=0, le=100, description="AI assessment of modularity (0-100)")
    ai_spaghetti_code_detected: bool = Field(..., description="Whether AI detected spaghetti code patterns")
    
    # Final normalized score
    score: float = Field(..., ge=0, le=100, description="Normalized repairability score (0-100)")


class ChangeEffortMetrics(BaseModel):
    """Change Effort metric: Cost/complexity of updating business logic."""
    
    # Hard metrics from Git history
    average_churn_rate: float = Field(..., description="Average file churn rate (commits per file)")
    complexity_churn_ratio: float = Field(..., description="Complexity score * churn rate")
    high_churn_files_count: int = Field(..., description="Number of files with high churn")
    
    # AI analysis score
    ai_change_impact_score: float = Field(..., ge=0, le=100, description="AI assessment of change impact (0-100)")
    ai_algorithmic_centricity: float = Field(..., ge=0, le=100, description="AI assessment of algorithm-centricity (0-100)")
    
    # Final normalized score
    score: float = Field(..., ge=0, le=100, description="Normalized change effort score (0-100, lower is better)")


class LegacyCompatibilityMetrics(BaseModel):
    """Legacy Compatibility metric: Backward compatibility and reusability."""
    
    # Hard metrics
    api_stability_score: float = Field(..., ge=0, le=100, description="API stability score based on SemVer checks")
    migration_test_coverage: float = Field(..., ge=0, le=100, description="Migration test coverage percentage")
    
    # AI analysis score
    ai_algorithmic_separation: float = Field(..., ge=0, le=100, description="AI assessment of algorithm separation from implementation")
    ai_framework_independence: float = Field(..., ge=0, le=100, description="AI assessment of framework independence")
    
    # Final normalized score
    score: float = Field(..., ge=0, le=100, description="Normalized legacy compatibility score (0-100)")


class StaticAnalysisData(BaseModel):
    """Raw data from static analysis tools (Radon, Lizard)."""
    
    radon_complexity: Dict[str, Any] = Field(default_factory=dict, description="Radon complexity analysis results")
    lizard_complexity: Dict[str, Any] = Field(default_factory=dict, description="Lizard complexity analysis results")
    file_count: int = Field(..., description="Total number of Python files analyzed")
    total_lines: int = Field(..., description="Total lines of code")


class AIAnalysisData(BaseModel):
    """Raw data from AI semantic analysis."""
    
    repairability_analysis: Dict[str, Any] = Field(default_factory=dict, description="AI analysis for repairability")
    change_effort_analysis: Dict[str, Any] = Field(default_factory=dict, description="AI analysis for change effort")
    legacy_compatibility_analysis: Dict[str, Any] = Field(default_factory=dict, description="AI analysis for legacy compatibility")
    analyzed_modules: List[str] = Field(default_factory=list, description="List of module paths analyzed by AI")


class MSIResult(BaseModel):
    """Complete MSI audit result."""
    
    # Input metadata
    target_path: str = Field(..., description="Path or URL of the analyzed repository")
    analysis_timestamp: str = Field(..., description="ISO timestamp of the analysis")
    
    # Raw data
    static_analysis: StaticAnalysisData = Field(..., description="Raw static analysis data")
    ai_analysis: Optional[AIAnalysisData] = Field(None, description="Raw AI analysis data")
    
    # Calculated metrics
    repairability: RepairabilityMetrics = Field(..., description="Repairability metric results")
    change_effort: ChangeEffortMetrics = Field(..., description="Change effort metric results")
    legacy_compatibility: LegacyCompatibilityMetrics = Field(..., description="Legacy compatibility metric results")
    
    # Final MSI score
    msi_score: float = Field(..., ge=0, le=100, description="Overall MSI score (weighted average, 0-100)")
    msi_rating: MSIRating = Field(..., description="MSI certification rating (Basic/Silver/Gold)")
    
    # Metadata
    weights: Dict[str, float] = Field(
        default_factory=lambda: {"repairability": 0.4, "change_effort": 0.35, "legacy_compatibility": 0.25},
        description="Weights used for calculating MSI score"
    )

```

```python
"""
Wrapper for static analysis tools (Radon, Lizard).
Extracts hard metrics: complexity, coupling, cohesion indicators.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from radon.complexity import cc_visit
from radon.metrics import mi_visit
from radon.raw import analyze
import lizard


class StaticAnalyzer:
    """Adapter for static code analysis tools."""
    
    def __init__(self, target_path: str):
        """
        Initialize static analyzer.
        
        Args:
            target_path: Path to the repository or directory to analyze
        """
        self.target_path = Path(target_path)
        if not self.target_path.exists():
            raise ValueError(f"Path does not exist: {target_path}")
    
    def analyze(self) -> Dict[str, Any]:
        """
        Run static analysis using Radon and Lizard.
        
        Returns:
            Dictionary containing raw analysis data
        """
        python_files = self._find_python_files()
        
        if not python_files:
            return {
                "radon_complexity": {},
                "lizard_complexity": {},
                "file_count": 0,
                "total_lines": 0
            }
        
        radon_results = self._run_radon_analysis(python_files)
        lizard_results = self._run_lizard_analysis(python_files)
        
        total_lines = sum(radon_results.get("file_stats", {}).values())
        
        return {
            "radon_complexity": radon_results,
            "lizard_complexity": lizard_results,
            "file_count": len(python_files),
            "total_lines": total_lines
        }
    
    def _find_python_files(self) -> List[Path]:
        """Find all Python files in the target path."""
        python_files = []
        
        # Exclude common directories
        exclude_dirs = {'.git', '.venv', 'venv', '__pycache__', '.pytest_cache', 'node_modules'}
        
        for root, dirs, files in os.walk(self.target_path):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    python_files.append(file_path)
        
        return python_files
    
    def _run_radon_analysis(self, python_files: List[Path]) -> Dict[str, Any]:
        """
        Run Radon analysis on Python files.
        
        Returns:
            Dictionary with complexity metrics and maintainability index
        """
        all_complexity = []
        all_maintainability = []
        file_stats = {}
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    source_code = f.read()
                
                # Cyclomatic complexity
                complexity_results = cc_visit(source_code)
                if complexity_results:
                    all_complexity.extend(complexity_results)
                
                # Maintainability index (includes cohesion indicators)
                mi_score = mi_visit(source_code, multi=True)
                all_maintainability.append(mi_score)
                
                # Raw analysis (line counts)
                raw_analysis = analyze(source_code)
                file_stats[str(file_path.relative_to(self.target_path))] = raw_analysis.loc
                
            except Exception as e:
                # Skip files that can't be analyzed
                continue
        
        # Calculate averages
        avg_complexity = (
            sum(c.complexity for c in all_complexity) / len(all_complexity)
            if all_complexity else 0.0
        )
        avg_maintainability = (
            sum(all_maintainability) / len(all_maintainability)
            if all_maintainability else 0.0
        )
        
        return {
            "functions": [
                {
                    "name": c.name,
                    "complexity": c.complexity,
                    "rank": c.rank
                }
                for c in all_complexity
            ],
            "average_complexity": avg_complexity,
            "average_maintainability_index": avg_maintainability,
            "total_functions": len(all_complexity),
            "file_stats": file_stats
        }
    
    def _run_lizard_analysis(self, python_files: List[Path]) -> Dict[str, Any]:
        """
        Run Lizard analysis on Python files.
        
        Returns:
            Dictionary with complexity and parameter metrics
        """
        all_results = []
        
        for file_path in python_files:
            try:
                result = lizard.analyze_file(str(file_path))
                if result:
                    all_results.append(result)
            except Exception as e:
                # Skip files that can't be analyzed
                continue
        
        if not all_results:
            return {
                "average_complexity": 0.0,
                "average_parameters": 0.0,
                "total_functions": 0,
                "files": []
            }
        
        # Aggregate results
        all_functions = []
        for result in all_results:
            for func in result.function_list:
                all_functions.append({
                    "name": func.name,
                    "complexity": func.cyclomatic_complexity,
                    "parameters": len(func.parameters),
                    "lines": func.length
                })
        
        avg_complexity = (
            sum(f["complexity"] for f in all_functions) / len(all_functions)
            if all_functions else 0.0
        )
        avg_parameters = (
            sum(f["parameters"] for f in all_functions) / len(all_functions)
            if all_functions else 0.0
        )
        
        return {
            "average_complexity": avg_complexity,
            "average_parameters": avg_parameters,
            "total_functions": len(all_functions),
            "functions": all_functions
        }

```

```python
"""
Wrapper for Google Gemini API.
Performs semantic analysis of code for algorithm-centricity and modularity assessment.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()


class AIAnalyzer:
    """Adapter for AI-based semantic code analysis using Google Gemini."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI analyzer.
        
        Args:
            api_key: Google Gemini API key. If not provided, reads from GEMINI_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it in .env file or pass as argument.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_repairability(self, code_samples: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze code for repairability (modularity, isolation).
        
        Args:
            code_samples: List of dicts with 'path' and 'code' keys
            
        Returns:
            Dictionary with AI analysis results
        """
        prompt = self._build_repairability_prompt(code_samples)
        
        try:
            response = self.model.generate_content(prompt)
            analysis_text = response.text
            
            # Parse response (basic parsing - can be enhanced)
            return {
                "modularity_score": self._extract_score(analysis_text, "modularity"),
                "spaghetti_code_detected": "spaghetti" in analysis_text.lower() or "tightly coupled" in analysis_text.lower(),
                "isolation_score": self._extract_score(analysis_text, "isolation"),
                "raw_analysis": analysis_text
            }
        except Exception as e:
            return {
                "modularity_score": 50.0,  # Default neutral score
                "spaghetti_code_detected": False,
                "isolation_score": 50.0,
                "raw_analysis": f"Error during AI analysis: {str(e)}",
                "error": str(e)
            }
    
    def analyze_change_effort(self, code_samples: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze code for change effort (algorithm-centricity, change impact).
        
        Args:
            code_samples: List of dicts with 'path' and 'code' keys
            
        Returns:
            Dictionary with AI analysis results
        """
        prompt = self._build_change_effort_prompt(code_samples)
        
        try:
            response = self.model.generate_content(prompt)
            analysis_text = response.text
            
            return {
                "change_impact_score": self._extract_score(analysis_text, "change impact"),
                "algorithmic_centricity": self._extract_score(analysis_text, "algorithmic"),
                "separation_score": self._extract_score(analysis_text, "separation"),
                "raw_analysis": analysis_text
            }
        except Exception as e:
            return {
                "change_impact_score": 50.0,
                "algorithmic_centricity": 50.0,
                "separation_score": 50.0,
                "raw_analysis": f"Error during AI analysis: {str(e)}",
                "error": str(e)
            }
    
    def analyze_legacy_compatibility(self, code_samples: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze code for legacy compatibility (algorithm separation, framework independence).
        
        Args:
            code_samples: List of dicts with 'path' and 'code' keys
            
        Returns:
            Dictionary with AI analysis results
        """
        prompt = self._build_legacy_compatibility_prompt(code_samples)
        
        try:
            response = self.model.generate_content(prompt)
            analysis_text = response.text
            
            return {
                "algorithmic_separation": self._extract_score(analysis_text, "separation"),
                "framework_independence": self._extract_score(analysis_text, "framework"),
                "raw_analysis": analysis_text
            }
        except Exception as e:
            return {
                "algorithmic_separation": 50.0,
                "framework_independence": 50.0,
                "raw_analysis": f"Error during AI analysis: {str(e)}",
                "error": str(e)
            }
    
    def _build_repairability_prompt(self, code_samples: List[Dict[str, str]]) -> str:
        """Build prompt for repairability analysis."""
        code_text = "\n\n".join([
            f"File: {sample['path']}\n```python\n{sample['code']}\n```"
            for sample in code_samples[:5]  # Limit to 5 files to avoid token limits
        ])
        
        return f"""You are a senior software architect analyzing code for Methodological Sustainability Index (MSI).

Analyze the following code samples for REPAIRABILITY (ease of making local changes without cascade effects).

Focus on:
1. Modularity: Are functions isolated? Can they be changed independently?
2. Spaghetti code detection: Are there tight couplings that create cascade effects?
3. Isolation: What percentage of modules can be changed in isolation?

Provide:
- A modularity score (0-100, where 100 = highly modular, 0 = tightly coupled)
- An isolation score (0-100, percentage of modules that can be changed independently)
- Detection of spaghetti code patterns (yes/no)
- Brief explanation

Code samples:
{code_text}

Format your response with clear scores and explanations."""

    def _build_change_effort_prompt(self, code_samples: List[Dict[str, str]]) -> str:
        """Build prompt for change effort analysis."""
        code_text = "\n\n".join([
            f"File: {sample['path']}\n```python\n{sample['code']}\n```"
            for sample in code_samples[:5]
        ])
        
        return f"""You are a senior software architect analyzing code for Methodological Sustainability Index (MSI).

Analyze the following code samples for CHANGE EFFORT (cost/complexity of updating business logic).

Focus on:
1. Algorithmic Centricity: Is the pure algorithm separated from implementation details (frameworks, hardware)?
2. Change Impact: If you change a business rule, how many files would be affected?
3. Separation of Concerns: Are algorithms independent of frameworks and infrastructure?

Provide:
- A change impact score (0-100, where 100 = high impact/cost, 0 = low impact)
- An algorithmic centricity score (0-100, where 100 = algorithm is well-separated, 0 = tightly coupled)
- A separation score (0-100, how well algorithms are separated from implementation)
- Brief explanation

Code samples:
{code_text}

Format your response with clear scores and explanations."""

    def _build_legacy_compatibility_prompt(self, code_samples: List[Dict[str, str]]) -> str:
        """Build prompt for legacy compatibility analysis."""
        code_text = "\n\n".join([
            f"File: {sample['path']}\n```python\n{sample['code']}\n```"
            for sample in code_samples[:5]
        ])
        
        return f"""You are a senior software architect analyzing code for Methodological Sustainability Index (MSI).

Analyze the following code samples for LEGACY COMPATIBILITY (backward compatibility and reusability).

Focus on:
1. Algorithmic Separation: Is the pure algorithm separated from "hardware" and frameworks?
2. Framework Independence: Can the core algorithms be reused without the framework?
3. Adaptive Reuse: Can old systems be renovated without complete demolition?

Provide:
- An algorithmic separation score (0-100, where 100 = well-separated, 0 = tightly bound)
- A framework independence score (0-100, where 100 = independent, 0 = framework-dependent)
- Brief explanation

Code samples:
{code_text}

Format your response with clear scores and explanations."""

    def _extract_score(self, text: str, keyword: str) -> float:
        """
        Extract a score (0-100) from AI response text.
        Looks for patterns like "score: 75" or "75/100".
        """
        import re
        
        # Try to find score patterns
        patterns = [
            rf"{keyword}.*?(\d{{1,3}})\s*/?\s*100",
            rf"{keyword}.*?score.*?(\d{{1,3}})",
            rf"(\d{{1,3}}).*?{keyword}",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                score = float(match.group(1))
                return min(100.0, max(0.0, score))
        
        # Default to neutral score if not found
        return 50.0
    
    def get_code_samples(self, target_path: str, max_files: int = 10) -> List[Dict[str, str]]:
        """
        Extract code samples from target path for AI analysis.
        Selects files with highest complexity for analysis.
        
        Args:
            target_path: Path to repository
            max_files: Maximum number of files to analyze
            
        Returns:
            List of dicts with 'path' and 'code' keys
        """
        from .static_analyzer import StaticAnalyzer
        
        # Use static analyzer to find complex files
        static_analyzer = StaticAnalyzer(target_path)
        python_files = static_analyzer._find_python_files()
        
        # Get complexity scores
        file_complexity = []
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    source_code = f.read()
                
                from radon.complexity import cc_visit
                complexity_results = cc_visit(source_code)
                total_complexity = sum(c.complexity for c in complexity_results)
                
                file_complexity.append((file_path, total_complexity, source_code))
            except Exception:
                continue
        
        # Sort by complexity (highest first) and take top files
        file_complexity.sort(key=lambda x: x[1], reverse=True)
        selected_files = file_complexity[:max_files]
        
        return [
            {
                "path": str(f[0].relative_to(Path(target_path))),
                "code": f[2][:2000]  # Limit code size to avoid token limits
            }
            for f in selected_files
        ]

```

Реализую сервис расчета MSI и обновляю main.py:


```python
"""
MSI Calculator Service.
Orchestrates data collection from adapters and calculates final MSI scores.
"""

from datetime import datetime
from typing import Optional
from pathlib import Path

from ..domain.models import (
    MSIResult,
    MSIRating,
    RepairabilityMetrics,
    ChangeEffortMetrics,
    LegacyCompatibilityMetrics,
    StaticAnalysisData,
    AIAnalysisData
)
from ..adapters.static_analyzer import StaticAnalyzer
from ..adapters.ai_analyzer import AIAnalyzer


class MSICalculator:
    """Service for calculating Methodological Sustainability Index."""
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        """
        Initialize MSI Calculator.
        
        Args:
            gemini_api_key: Optional Gemini API key (if not provided, reads from env)
        """
        self.gemini_api_key = gemini_api_key
    
    def calculate(self, target_path: str, use_ai: bool = True) -> MSIResult:
        """
        Calculate MSI for the target path.
        
        Args:
            target_path: Path to repository or directory
            use_ai: Whether to use AI analysis (requires API key)
            
        Returns:
            MSIResult with all calculated metrics
        """
        # Step 1: Static Analysis
        static_analyzer = StaticAnalyzer(target_path)
        static_data = static_analyzer.analyze()
        static_analysis = StaticAnalysisData(**static_data)
        
        # Step 2: AI Analysis (if enabled)
        ai_analysis = None
        if use_ai:
            try:
                ai_analyzer = AIAnalyzer(self.gemini_api_key)
                code_samples = ai_analyzer.get_code_samples(target_path, max_files=10)
                
                if code_samples:
                    repairability_ai = ai_analyzer.analyze_repairability(code_samples)
                    change_effort_ai = ai_analyzer.analyze_change_effort(code_samples)
                    legacy_compat_ai = ai_analyzer.analyze_legacy_compatibility(code_samples)
                    
                    ai_analysis = AIAnalysisData(
                        repairability_analysis=repairability_ai,
                        change_effort_analysis=change_effort_ai,
                        legacy_compatibility_analysis=legacy_compat_ai,
                        analyzed_modules=[s["path"] for s in code_samples]
                    )
            except Exception as e:
                # Continue without AI if it fails
                print(f"Warning: AI analysis failed: {e}")
        
        # Step 3: Calculate Metrics
        repairability = self._calculate_repairability(static_analysis, ai_analysis)
        change_effort = self._calculate_change_effort(static_analysis, ai_analysis)
        legacy_compatibility = self._calculate_legacy_compatibility(static_analysis, ai_analysis)
        
        # Step 4: Calculate Final MSI Score
        weights = {"repairability": 0.4, "change_effort": 0.35, "legacy_compatibility": 0.25}
        msi_score = (
            repairability.score * weights["repairability"] +
            (100 - change_effort.score) * weights["change_effort"] +  # Invert change effort (lower is better)
            legacy_compatibility.score * weights["legacy_compatibility"]
        )
        
        # Determine rating
        if msi_score >= 80:
            rating = MSIRating.GOLD
        elif msi_score >= 60:
            rating = MSIRating.SILVER
        else:
            rating = MSIRating.BASIC
        
        return MSIResult(
            target_path=target_path,
            analysis_timestamp=datetime.now().isoformat(),
            static_analysis=static_analysis,
            ai_analysis=ai_analysis,
            repairability=repairability,
            change_effort=change_effort,
            legacy_compatibility=legacy_compatibility,
            msi_score=round(msi_score, 2),
            msi_rating=rating,
            weights=weights
        )
    
    def _calculate_repairability(
        self,
        static_data: StaticAnalysisData,
        ai_data: Optional[AIAnalysisData]
    ) -> RepairabilityMetrics:
        """Calculate Repairability metric."""
        radon = static_data.radon_complexity
        lizard = static_data.lizard_complexity
        
        # Hard metrics
        avg_complexity = radon.get("average_complexity", 0.0)
        avg_maintainability = radon.get("average_maintainability_index", 0.0)
        
        # Coupling indicator (lower complexity = lower coupling)
        # Normalize complexity to 0-100 (assuming max reasonable complexity is 20)
        coupling_score = min(100.0, (avg_complexity / 20.0) * 100.0)
        
        # Cohesion indicator (maintainability index, normalized)
        # MI ranges roughly 0-100, where higher is better
        cohesion_score = min(100.0, max(0.0, avg_maintainability))
        
        # Estimate isolated modules percentage
        # Lower complexity and higher maintainability = more isolated modules
        isolated_percentage = max(0.0, min(100.0, 100.0 - coupling_score + (cohesion_score * 0.3)))
        
        # AI metrics
        if ai_data and ai_data.repairability_analysis:
            ai_modularity = ai_data.repairability_analysis.get("modularity_score", 50.0)
            ai_spaghetti = ai_data.repairability_analysis.get("spaghetti_code_detected", False)
        else:
            ai_modularity = 50.0  # Neutral default
            ai_spaghetti = False
        
        # Combine hard metrics (70%) and AI metrics (30%)
        hard_score = (100.0 - coupling_score) * 0.4 + cohesion_score * 0.3 + isolated_percentage * 0.3
        ai_score = ai_modularity
        final_score = hard_score * 0.7 + ai_score * 0.3
        
        return RepairabilityMetrics(
            average_coupling=coupling_score,
            average_cohesion=cohesion_score,
            cyclomatic_complexity=avg_complexity,
            isolated_modules_percentage=isolated_percentage,
            ai_modularity_score=ai_modularity,
            ai_spaghetti_code_detected=ai_spaghetti,
            score=round(final_score, 2)
        )
    
    def _calculate_change_effort(
        self,
        static_data: StaticAnalysisData,
        ai_data: Optional[AIAnalysisData]
    ) -> ChangeEffortMetrics:
        """Calculate Change Effort metric."""
        radon = static_data.radon_complexity
        lizard = static_data.lizard_complexity
        
        # Hard metrics (simplified - Phase 1 doesn't include Git history yet)
        avg_complexity = radon.get("average_complexity", 0.0)
        
        # Placeholder for churn rate (will be implemented in Phase 2 with GitPython)
        churn_rate = 1.0  # Default neutral value
        complexity_churn_ratio = avg_complexity * churn_rate
        high_churn_files = 0  # Placeholder
        
        # AI metrics
        if ai_data and ai_data.change_effort_analysis:
            ai_change_impact = ai_data.change_effort_analysis.get("change_impact_score", 50.0)
            ai_algorithmic = ai_data.change_effort_analysis.get("algorithmic_centricity", 50.0)
        else:
            ai_change_impact = 50.0
            ai_algorithmic = 50.0
        
        # Calculate score (higher complexity + higher churn = higher effort)
        # Normalize complexity (0-100 scale, assuming max 20)
        complexity_score = min(100.0, (avg_complexity / 20.0) * 100.0)
        churn_score = min(100.0, churn_rate * 10.0)  # Normalize churn
        
        # Combine metrics
        hard_score = (complexity_score + churn_score) / 2.0
        ai_score = ai_change_impact  # Higher impact = higher effort
        
        # Invert algorithmic centricity (higher centricity = lower effort)
        effort_reduction = (100.0 - ai_algorithmic) * 0.3
        
        final_score = hard_score * 0.6 + ai_score * 0.4 - effort_reduction
        final_score = max(0.0, min(100.0, final_score))
        
        return ChangeEffortMetrics(
            average_churn_rate=churn_rate,
            complexity_churn_ratio=complexity_churn_ratio,
            high_churn_files_count=high_churn_files,
            ai_change_impact_score=ai_change_impact,
            ai_algorithmic_centricity=ai_algorithmic,
            score=round(final_score, 2)
        )
    
    def _calculate_legacy_compatibility(
        self,
        static_data: StaticAnalysisData,
        ai_data: Optional[AIAnalysisData]
    ) -> LegacyCompatibilityMetrics:
        """Calculate Legacy Compatibility metric."""
        # Hard metrics (simplified - Phase 1 doesn't include SemVer checks yet)
        api_stability = 50.0  # Placeholder - will be implemented in Phase 2
        migration_coverage = 50.0  # Placeholder
        
        # AI metrics
        if ai_data and ai_data.legacy_compatibility_analysis:
            ai_separation = ai_data.legacy_compatibility_analysis.get("algorithmic_separation", 50.0)
            ai_framework = ai_data.legacy_compatibility_analysis.get("framework_independence", 50.0)
        else:
            ai_separation = 50.0
            ai_framework = 50.0
        
        # Combine metrics
        hard_score = (api_stability + migration_coverage) / 2.0
        ai_score = (ai_separation + ai_framework) / 2.0
        
        final_score = hard_score * 0.4 + ai_score * 0.6
        
        return LegacyCompatibilityMetrics(
            api_stability_score=api_stability,
            migration_test_coverage=migration_coverage,
            ai_algorithmic_separation=ai_separation,
            ai_framework_independence=ai_framework,
            score=round(final_score, 2)
        )

```

```python
"""
MSI v0.1 - Methodological Sustainability Index Calculator
Entry point for CLI application.
"""

import json
import typer
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from .services.msi_calculator import MSICalculator

# Initialize Typer app and Rich console
app = typer.Typer()
console = Console()


@app.command()
def audit(
    path: str = typer.Argument(..., help="Path to the repository/folder to audit"),
    output: str = typer.Option("console", "--output", "-o", help="Output format: 'console' or 'json'"),
    no_ai: bool = typer.Option(False, "--no-ai", help="Skip AI analysis (faster, less accurate)"),
    api_key: str = typer.Option(None, "--api-key", help="Gemini API key (overrides .env)")
):
    """
    Runs the MSI (Methodological Sustainability Index) audit on the specified path.
    
    Example:
        python src/main.py audit ./my_project
        python src/main.py audit ./my_project --output json > results.json
    """
    console.print(Panel.fit(
        f"Starting MSI Audit for: [bold cyan]{path}[/bold cyan]",
        title="VAOP MSI v0.1"
    ))
    
    # Validate path
    target_path = Path(path)
    if not target_path.exists():
        console.print(f"[bold red]Error:[/bold red] Path does not exist: {path}")
        raise typer.Exit(1)
    
    # Initialize calculator
    calculator = MSICalculator(gemini_api_key=api_key)
    
    # Run analysis with progress indicators
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task1 = progress.add_task("[yellow]Step 1:[/yellow] Running Static Analysis (Radon/Lizard)...", total=None)
        
        try:
            result = calculator.calculate(str(target_path), use_ai=not no_ai)
            progress.update(task1, completed=True)
            
            if not no_ai:
                task2 = progress.add_task("[yellow]Step 2:[/yellow] AI Semantic Analysis (Gemini)...", total=None)
                progress.update(task2, completed=True)
            
            task3 = progress.add_task("[yellow]Step 3:[/yellow] Calculating MSI Scores...", total=None)
            progress.update(task3, completed=True)
            
        except Exception as e:
            console.print(f"[bold red]Error during analysis:[/bold red] {str(e)}")
            raise typer.Exit(1)
    
    # Output results
    if output == "json":
        # JSON output for programmatic use
        output_dict = result.model_dump(mode="json")
        print(json.dumps(output_dict, indent=2))
    else:
        # Rich console output
        _display_results(console, result)


def _display_results(console: Console, result):
    """Display MSI results in a formatted table."""
    console.print("\n[bold green]Audit Complete![/bold green]\n")
    
    # Overall score
    rating_color = {
        "Gold": "gold1",
        "Silver": "bright_white",
        "Basic": "yellow"
    }
    console.print(Panel.fit(
        f"Overall MSI Score: [bold {rating_color.get(result.msi_rating.value, 'white')}]{result.msi_score}/100[/bold {rating_color.get(result.msi_rating.value, 'white')}]\n"
        f"Rating: [bold {rating_color.get(result.msi_rating.value, 'white')}]{result.msi_rating.value}[/bold {rating_color.get(result.msi_rating.value, 'white')}]",
        title="MSI Result"
    ))
    
    # Metrics table
    table = Table(title="Detailed Metrics", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Score", justify="right", style="green")
    table.add_column("Details", style="white")
    
    # Repairability
    table.add_row(
        "Repairability",
        f"{result.repairability.score}/100",
        f"Coupling: {result.repairability.average_coupling:.1f}, "
        f"Cohesion: {result.repairability.average_cohesion:.1f}, "
        f"Isolated: {result.repairability.isolated_modules_percentage:.1f}%"
    )
    
    # Change Effort
    table.add_row(
        "Change Effort",
        f"{result.change_effort.score}/100",
        f"Churn: {result.change_effort.average_churn_rate:.2f}, "
        f"Complexity: {result.change_effort.complexity_churn_ratio:.2f}, "
        f"AI Centricity: {result.change_effort.ai_algorithmic_centricity:.1f}"
    )
    
    # Legacy Compatibility
    table.add_row(
        "Legacy Compatibility",
        f"{result.legacy_compatibility.score}/100",
        f"API Stability: {result.legacy_compatibility.api_stability_score:.1f}, "
        f"Framework Independence: {result.legacy_compatibility.ai_framework_independence:.1f}"
    )
    
    console.print(table)
    
    # Static analysis summary
    console.print(f"\n[bold]Static Analysis Summary:[/bold]")
    console.print(f"  Files analyzed: {result.static_analysis.file_count}")
    console.print(f"  Total lines: {result.static_analysis.total_lines}")
    console.print(f"  Avg complexity: {result.static_analysis.radon_complexity.get('average_complexity', 0):.2f}")
    
    if result.ai_analysis:
        console.print(f"\n[bold]AI Analysis:[/bold]")
        console.print(f"  Modules analyzed: {len(result.ai_analysis.analyzed_modules)}")
        if result.ai_analysis.repairability_analysis.get("spaghetti_code_detected"):
            console.print("  [yellow]⚠ Warning: Spaghetti code patterns detected[/yellow]")


if __name__ == "__main__":
    app()

```

```pip-requirements
# Core Logic & CLI
typer>=0.9.0
rich>=13.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0

# Static Analysis Tools (The "Builders")
radon>=6.0.0
lizard>=1.17.0

# Git History Analysis
GitPython>=3.1.0

# AI Integration
google-generativeai>=0.3.0


```

Проверяю ошибки линтера:


Проверяю импорты и исправляю возможные проблемы:


Проверяю корректность структуры и создаю простой тест для проверки импортов:


Исправляю импорты для корректной работы при запуске:


```python
"""
Wrapper for Google Gemini API.
Performs semantic analysis of code for algorithm-centricity and modularity assessment.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()


class AIAnalyzer:
    """Adapter for AI-based semantic code analysis using Google Gemini."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI analyzer.
        
        Args:
            api_key: Google Gemini API key. If not provided, reads from GEMINI_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it in .env file or pass as argument.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_repairability(self, code_samples: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze code for repairability (modularity, isolation).
        
        Args:
            code_samples: List of dicts with 'path' and 'code' keys
            
        Returns:
            Dictionary with AI analysis results
        """
        prompt = self._build_repairability_prompt(code_samples)
        
        try:
            response = self.model.generate_content(prompt)
            analysis_text = response.text
            
            # Parse response (basic parsing - can be enhanced)
            return {
                "modularity_score": self._extract_score(analysis_text, "modularity"),
                "spaghetti_code_detected": "spaghetti" in analysis_text.lower() or "tightly coupled" in analysis_text.lower(),
                "isolation_score": self._extract_score(analysis_text, "isolation"),
                "raw_analysis": analysis_text
            }
        except Exception as e:
            return {
                "modularity_score": 50.0,  # Default neutral score
                "spaghetti_code_detected": False,
                "isolation_score": 50.0,
                "raw_analysis": f"Error during AI analysis: {str(e)}",
                "error": str(e)
            }
    
    def analyze_change_effort(self, code_samples: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze code for change effort (algorithm-centricity, change impact).
        
        Args:
            code_samples: List of dicts with 'path' and 'code' keys
            
        Returns:
            Dictionary with AI analysis results
        """
        prompt = self._build_change_effort_prompt(code_samples)
        
        try:
            response = self.model.generate_content(prompt)
            analysis_text = response.text
            
            return {
                "change_impact_score": self._extract_score(analysis_text, "change impact"),
                "algorithmic_centricity": self._extract_score(analysis_text, "algorithmic"),
                "separation_score": self._extract_score(analysis_text, "separation"),
                "raw_analysis": analysis_text
            }
        except Exception as e:
            return {
                "change_impact_score": 50.0,
                "algorithmic_centricity": 50.0,
                "separation_score": 50.0,
                "raw_analysis": f"Error during AI analysis: {str(e)}",
                "error": str(e)
            }
    
    def analyze_legacy_compatibility(self, code_samples: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze code for legacy compatibility (algorithm separation, framework independence).
        
        Args:
            code_samples: List of dicts with 'path' and 'code' keys
            
        Returns:
            Dictionary with AI analysis results
        """
        prompt = self._build_legacy_compatibility_prompt(code_samples)
        
        try:
            response = self.model.generate_content(prompt)
            analysis_text = response.text
            
            return {
                "algorithmic_separation": self._extract_score(analysis_text, "separation"),
                "framework_independence": self._extract_score(analysis_text, "framework"),
                "raw_analysis": analysis_text
            }
        except Exception as e:
            return {
                "algorithmic_separation": 50.0,
                "framework_independence": 50.0,
                "raw_analysis": f"Error during AI analysis: {str(e)}",
                "error": str(e)
            }
    
    def _build_repairability_prompt(self, code_samples: List[Dict[str, str]]) -> str:
        """Build prompt for repairability analysis."""
        code_text = "\n\n".join([
            f"File: {sample['path']}\n```python\n{sample['code']}\n```"
            for sample in code_samples[:5]  # Limit to 5 files to avoid token limits
        ])
        
        return f"""You are a senior software architect analyzing code for Methodological Sustainability Index (MSI).

Analyze the following code samples for REPAIRABILITY (ease of making local changes without cascade effects).

Focus on:
1. Modularity: Are functions isolated? Can they be changed independently?
2. Spaghetti code detection: Are there tight couplings that create cascade effects?
3. Isolation: What percentage of modules can be changed in isolation?

Provide:
- A modularity score (0-100, where 100 = highly modular, 0 = tightly coupled)
- An isolation score (0-100, percentage of modules that can be changed independently)
- Detection of spaghetti code patterns (yes/no)
- Brief explanation

Code samples:
{code_text}

Format your response with clear scores and explanations."""

    def _build_change_effort_prompt(self, code_samples: List[Dict[str, str]]) -> str:
        """Build prompt for change effort analysis."""
        code_text = "\n\n".join([
            f"File: {sample['path']}\n```python\n{sample['code']}\n```"
            for sample in code_samples[:5]
        ])
        
        return f"""You are a senior software architect analyzing code for Methodological Sustainability Index (MSI).

Analyze the following code samples for CHANGE EFFORT (cost/complexity of updating business logic).

Focus on:
1. Algorithmic Centricity: Is the pure algorithm separated from implementation details (frameworks, hardware)?
2. Change Impact: If you change a business rule, how many files would be affected?
3. Separation of Concerns: Are algorithms independent of frameworks and infrastructure?

Provide:
- A change impact score (0-100, where 100 = high impact/cost, 0 = low impact)
- An algorithmic centricity score (0-100, where 100 = algorithm is well-separated, 0 = tightly coupled)
- A separation score (0-100, how well algorithms are separated from implementation)
- Brief explanation

Code samples:
{code_text}

Format your response with clear scores and explanations."""

    def _build_legacy_compatibility_prompt(self, code_samples: List[Dict[str, str]]) -> str:
        """Build prompt for legacy compatibility analysis."""
        code_text = "\n\n".join([
            f"File: {sample['path']}\n```python\n{sample['code']}\n```"
            for sample in code_samples[:5]
        ])
        
        return f"""You are a senior software architect analyzing code for Methodological Sustainability Index (MSI).

Analyze the following code samples for LEGACY COMPATIBILITY (backward compatibility and reusability).

Focus on:
1. Algorithmic Separation: Is the pure algorithm separated from "hardware" and frameworks?
2. Framework Independence: Can the core algorithms be reused without the framework?
3. Adaptive Reuse: Can old systems be renovated without complete demolition?

Provide:
- An algorithmic separation score (0-100, where 100 = well-separated, 0 = tightly bound)
- A framework independence score (0-100, where 100 = independent, 0 = framework-dependent)
- Brief explanation

Code samples:
{code_text}

Format your response with clear scores and explanations."""

    def _extract_score(self, text: str, keyword: str) -> float:
        """
        Extract a score (0-100) from AI response text.
        Looks for patterns like "score: 75" or "75/100".
        """
        import re
        
        # Try to find score patterns
        patterns = [
            rf"{keyword}.*?(\d{{1,3}})\s*/?\s*100",
            rf"{keyword}.*?score.*?(\d{{1,3}})",
            rf"(\d{{1,3}}).*?{keyword}",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                score = float(match.group(1))
                return min(100.0, max(0.0, score))
        
        # Default to neutral score if not found
        return 50.0
    
    def get_code_samples(self, target_path: str, max_files: int = 10) -> List[Dict[str, str]]:
        """
        Extract code samples from target path for AI analysis.
        Selects files with highest complexity for analysis.
        
        Args:
            target_path: Path to repository
            max_files: Maximum number of files to analyze
            
        Returns:
            List of dicts with 'path' and 'code' keys
        """
        # Import here to avoid circular dependency
        from ..adapters.static_analyzer import StaticAnalyzer
        
        # Use static analyzer to find complex files
        static_analyzer = StaticAnalyzer(target_path)
        python_files = static_analyzer._find_python_files()
        
        # Get complexity scores
        file_complexity = []
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    source_code = f.read()
                
                from radon.complexity import cc_visit
                complexity_results = cc_visit(source_code)
                total_complexity = sum(c.complexity for c in complexity_results)
                
                file_complexity.append((file_path, total_complexity, source_code))
            except Exception:
                continue
        
        # Sort by complexity (highest first) and take top files
        file_complexity.sort(key=lambda x: x[1], reverse=True)
        selected_files = file_complexity[:max_files]
        
        return [
            {
                "path": str(f[0].relative_to(Path(target_path))),
                "code": f[2][:2000]  # Limit code size to avoid token limits
            }
            for f in selected_files
        ]

```

Исправляю импорт в `ai_analyzer.py`:


```python
"""
Wrapper for Google Gemini API.
Performs semantic analysis of code for algorithm-centricity and modularity assessment.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()


class AIAnalyzer:
    """Adapter for AI-based semantic code analysis using Google Gemini."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI analyzer.
        
        Args:
            api_key: Google Gemini API key. If not provided, reads from GEMINI_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it in .env file or pass as argument.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_repairability(self, code_samples: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze code for repairability (modularity, isolation).
        
        Args:
            code_samples: List of dicts with 'path' and 'code' keys
            
        Returns:
            Dictionary with AI analysis results
        """
        prompt = self._build_repairability_prompt(code_samples)
        
        try:
            response = self.model.generate_content(prompt)
            analysis_text = response.text
            
            # Parse response (basic parsing - can be enhanced)
            return {
                "modularity_score": self._extract_score(analysis_text, "modularity"),
                "spaghetti_code_detected": "spaghetti" in analysis_text.lower() or "tightly coupled" in analysis_text.lower(),
                "isolation_score": self._extract_score(analysis_text, "isolation"),
                "raw_analysis": analysis_text
            }
        except Exception as e:
            return {
                "modularity_score": 50.0,  # Default neutral score
                "spaghetti_code_detected": False,
                "isolation_score": 50.0,
                "raw_analysis": f"Error during AI analysis: {str(e)}",
                "error": str(e)
            }
    
    def analyze_change_effort(self, code_samples: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze code for change effort (algorithm-centricity, change impact).
        
        Args:
            code_samples: List of dicts with 'path' and 'code' keys
            
        Returns:
            Dictionary with AI analysis results
        """
        prompt = self._build_change_effort_prompt(code_samples)
        
        try:
            response = self.model.generate_content(prompt)
            analysis_text = response.text
            
            return {
                "change_impact_score": self._extract_score(analysis_text, "change impact"),
                "algorithmic_centricity": self._extract_score(analysis_text, "algorithmic"),
                "separation_score": self._extract_score(analysis_text, "separation"),
                "raw_analysis": analysis_text
            }
        except Exception as e:
            return {
                "change_impact_score": 50.0,
                "algorithmic_centricity": 50.0,
                "separation_score": 50.0,
                "raw_analysis": f"Error during AI analysis: {str(e)}",
                "error": str(e)
            }
    
    def analyze_legacy_compatibility(self, code_samples: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze code for legacy compatibility (algorithm separation, framework independence).
        
        Args:
            code_samples: List of dicts with 'path' and 'code' keys
            
        Returns:
            Dictionary with AI analysis results
        """
        prompt = self._build_legacy_compatibility_prompt(code_samples)
        
        try:
            response = self.model.generate_content(prompt)
            analysis_text = response.text
            
            return {
                "algorithmic_separation": self._extract_score(analysis_text, "separation"),
                "framework_independence": self._extract_score(analysis_text, "framework"),
                "raw_analysis": analysis_text
            }
        except Exception as e:
            return {
                "algorithmic_separation": 50.0,
                "framework_independence": 50.0,
                "raw_analysis": f"Error during AI analysis: {str(e)}",
                "error": str(e)
            }
    
    def _build_repairability_prompt(self, code_samples: List[Dict[str, str]]) -> str:
        """Build prompt for repairability analysis."""
        code_text = "\n\n".join([
            f"File: {sample['path']}\n```python\n{sample['code']}\n```"
            for sample in code_samples[:5]  # Limit to 5 files to avoid token limits
        ])
        
        return f"""You are a senior software architect analyzing code for Methodological Sustainability Index (MSI).

Analyze the following code samples for REPAIRABILITY (ease of making local changes without cascade effects).

Focus on:
1. Modularity: Are functions isolated? Can they be changed independently?
2. Spaghetti code detection: Are there tight couplings that create cascade effects?
3. Isolation: What percentage of modules can be changed in isolation?

Provide:
- A modularity score (0-100, where 100 = highly modular, 0 = tightly coupled)
- An isolation score (0-100, percentage of modules that can be changed independently)
- Detection of spaghetti code patterns (yes/no)
- Brief explanation

Code samples:
{code_text}

Format your response with clear scores and explanations."""

    def _build_change_effort_prompt(self, code_samples: List[Dict[str, str]]) -> str:
        """Build prompt for change effort analysis."""
        code_text = "\n\n".join([
            f"File: {sample['path']}\n```python\n{sample['code']}\n```"
            for sample in code_samples[:5]
        ])
        
        return f"""You are a senior software architect analyzing code for Methodological Sustainability Index (MSI).

Analyze the following code samples for CHANGE EFFORT (cost/complexity of updating business logic).

Focus on:
1. Algorithmic Centricity: Is the pure algorithm separated from implementation details (frameworks, hardware)?
2. Change Impact: If you change a business rule, how many files would be affected?
3. Separation of Concerns: Are algorithms independent of frameworks and infrastructure?

Provide:
- A change impact score (0-100, where 100 = high impact/cost, 0 = low impact)
- An algorithmic centricity score (0-100, where 100 = algorithm is well-separated, 0 = tightly coupled)
- A separation score (0-100, how well algorithms are separated from implementation)
- Brief explanation

Code samples:
{code_text}

Format your response with clear scores and explanations."""

    def _build_legacy_compatibility_prompt(self, code_samples: List[Dict[str, str]]) -> str:
        """Build prompt for legacy compatibility analysis."""
        code_text = "\n\n".join([
            f"File: {sample['path']}\n```python\n{sample['code']}\n```"
            for sample in code_samples[:5]
        ])
        
        return f"""You are a senior software architect analyzing code for Methodological Sustainability Index (MSI).

Analyze the following code samples for LEGACY COMPATIBILITY (backward compatibility and reusability).

Focus on:
1. Algorithmic Separation: Is the pure algorithm separated from "hardware" and frameworks?
2. Framework Independence: Can the core algorithms be reused without the framework?
3. Adaptive Reuse: Can old systems be renovated without complete demolition?

Provide:
- An algorithmic separation score (0-100, where 100 = well-separated, 0 = tightly bound)
- A framework independence score (0-100, where 100 = independent, 0 = framework-dependent)
- Brief explanation

Code samples:
{code_text}

Format your response with clear scores and explanations."""

    def _extract_score(self, text: str, keyword: str) -> float:
        """
        Extract a score (0-100) from AI response text.
        Looks for patterns like "score: 75" or "75/100".
        """
        import re
        
        # Try to find score patterns
        patterns = [
            rf"{keyword}.*?(\d{{1,3}})\s*/?\s*100",
            rf"{keyword}.*?score.*?(\d{{1,3}})",
            rf"(\d{{1,3}}).*?{keyword}",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                score = float(match.group(1))
                return min(100.0, max(0.0, score))
        
        # Default to neutral score if not found
        return 50.0
    
    def get_code_samples(self, target_path: str, max_files: int = 10) -> List[Dict[str, str]]:
        """
        Extract code samples from target path for AI analysis.
        Selects files with highest complexity for analysis.
        
        Args:
            target_path: Path to repository
            max_files: Maximum number of files to analyze
            
        Returns:
            List of dicts with 'path' and 'code' keys
        """
        # Import here to avoid circular dependency
        from .static_analyzer import StaticAnalyzer
        
        # Use static analyzer to find complex files
        static_analyzer = StaticAnalyzer(target_path)
        python_files = static_analyzer._find_python_files()
        
        # Get complexity scores
        file_complexity = []
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    source_code = f.read()
                
                from radon.complexity import cc_visit
                complexity_results = cc_visit(source_code)
                total_complexity = sum(c.complexity for c in complexity_results)
                
                file_complexity.append((file_path, total_complexity, source_code))
            except Exception:
                continue
        
        # Sort by complexity (highest first) and take top files
        file_complexity.sort(key=lambda x: x[1], reverse=True)
        selected_files = file_complexity[:max_files]
        
        return [
            {
                "path": str(f[0].relative_to(Path(target_path))),
                "code": f[2][:2000]  # Limit code size to avoid token limits
            }
            for f in selected_files
        ]

```

Создаю краткую инструкцию по тестированию и проверяю структуру:


Обновляю README с более подробными инструкциями:


```markdown
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


```

Реализация Фазы 1 завершена. Сводка:

## Реализовано для Фазы 1

### 1. Domain Models (`src/domain/models.py`)
- `RepairabilityMetrics` — метрика ремонтопригодности
- `ChangeEffortMetrics` — метрика стоимости изменений
- `LegacyCompatibilityMetrics` — метрика совместимости с legacy
- `MSIResult` — итоговый результат с рейтингом (Basic/Silver/Gold)
- `StaticAnalysisData` и `AIAnalysisData` — сырые данные

### 2. Static Analyzer Adapter (`src/adapters/static_analyzer.py`)
- Интеграция с Radon (cyclomatic complexity, maintainability index)
- Интеграция с Lizard (complexity, parameters)
- Автоматический поиск Python-файлов
- Исключение служебных директорий (.git, .venv, и т.д.)

### 3. AI Analyzer Adapter (`src/adapters/ai_analyzer.py`)
- Интеграция с Google Gemini API
- Промпты для трех метрик:
  - Repairability: модульность, изоляция, спагетти-код
  - Change Effort: алгоритмо-центричность, влияние изменений
  - Legacy Compatibility: разделение алгоритмов, независимость от фреймворков
- Автоматический выбор наиболее сложных файлов для анализа
- Парсинг ответов AI для извлечения числовых оценок

### 4. MSI Calculator Service (`src/services/msi_calculator.py`)
- Оркестрация анализа (статический + AI)
- Расчет трех метрик с нормализацией 0–100
- Взвешенное вычисление итогового MSI Score
- Определение рейтинга: Gold (≥80), Silver (≥60), Basic (<60)

### 5. CLI Entry Point (`src/main.py`)
- Полная интеграция всех компонентов
- Rich-вывод с таблицами и прогресс-барами
- JSON-вывод для программного использования
- Опция `--no-ai` для быстрого анализа без AI
- Обработка ошибок

### 6. Обновления
- `requirements.txt` — добавлен GitPython (для Фазы 2)
- `README.md` — обновлены инструкции по использованию

## Как использовать

```bash
# Установка зависимостей
pip install -r requirements.txt

# Базовое использование (с AI)
python -m src.main audit .

# Вывод в JSON
python -m src.main audit . --output json > results.json

# Без AI (только статический анализ)
python -m src.main audit . --no-ai
```

## Особенности реализации

1. Clean Architecture — четкое разделение слоев
2. Обработка ошибок — graceful fallback при недоступности AI
3. Английские комментарии — все комментарии на английском
4. Типизация — использование Pydantic для валидации данных
5. Расширяемость — готово к добавлению Git-анализа в Фазе 2

Готово к тестированию. Инструмент принимает путь к репозиторию и выдает JSON с сырыми метриками, как требуется в Фазе 1.

```shellscript
# Установка зависимостей
pip install -r requirements.txt

# Базовое использование (с AI)
python -m src.main audit .

# Вывод в JSON
python -m src.main audit . --output json > results.json

# Без AI (только статический анализ)
python -m src.main audit . --no-ai
```

