"""
Wrapper for static analysis tools (Radon, Lizard).
Extracts hard metrics: complexity, coupling, cohesion indicators.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from radon.complexity import cc_visit, cc_rank
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
                    "rank": cc_rank(c.complexity)
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
