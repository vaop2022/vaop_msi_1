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
    * `git_analyzer.py`: Analyzes Git repository history for churn metrics (Phase 2).

### 3. Services Layer (`src/services`)
* **Responsibility:** The "Brain". It orchestrates the flow:
    1.  Call Adapters to get raw data.
    2.  Apply weights/coefficients defined in the VAOP methodology.
    3.  Calculate the final Score (Gold/Silver/Bronze).

### 4. Entry Point (`src/main.py`)
* **Responsibility:** CLI interface using `typer`. Handles user input and prints the formatted Report using `rich`.

