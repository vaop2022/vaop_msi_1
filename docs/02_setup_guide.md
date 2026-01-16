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

