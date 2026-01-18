"""
Wrapper for Google Gemini API.
Performs semantic analysis of code for algorithm-centricity and modularity assessment.
"""

import os
import warnings
from pathlib import Path
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Suppress FutureWarning BEFORE importing deprecated package
warnings.filterwarnings('ignore', category=FutureWarning)

# Try new API first, fallback to old if needed
try:
    from google import genai
    USE_NEW_API = True
except ImportError:
    import google.generativeai as genai
    USE_NEW_API = False

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
        
        if USE_NEW_API:
            # New API: google-genai
            self.client = genai.Client(api_key=self.api_key)
            self.model_name = "gemini-2.0-flash-exp"  # or "gemini-pro" if flash not available
            self.model = None
        else:
            # Old API: google-generativeai (with warning suppression)
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.client = None
            self.model_name = None
    
    def _generate_content(self, prompt: str) -> str:
        """
        Generate content using appropriate API (new or old).
        
        Args:
            prompt: Text prompt for the model
            
        Returns:
            Response text
        """
        if USE_NEW_API:
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                # Extract text from response (format may vary)
                if hasattr(response, 'text'):
                    return response.text
                elif hasattr(response, 'candidates') and response.candidates:
                    if hasattr(response.candidates[0], 'content'):
                        parts = response.candidates[0].content.parts
                        if parts:
                            return parts[0].text if hasattr(parts[0], 'text') else str(parts[0])
                return str(response)
            except Exception as e:
                # Fallback to old API if new one fails
                return self._generate_content_old(prompt)
        else:
            return self._generate_content_old(prompt)
    
    def _generate_content_old(self, prompt: str) -> str:
        """Generate content using old API."""
        response = self.model.generate_content(prompt)
        return response.text
    
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
            analysis_text = self._generate_content(prompt)
            
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
            analysis_text = self._generate_content(prompt)
            
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
            analysis_text = self._generate_content(prompt)
            
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
