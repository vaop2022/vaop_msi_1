"""
Wrapper for Git history analysis using GitPython.
Extracts churn metrics: file change frequency, hot spots, complexity-churn correlation.
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from collections import defaultdict

try:
    import git
    from git import Repo, InvalidGitRepositoryError
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False


class GitAnalyzer:
    """Adapter for Git repository history analysis."""
    
    def __init__(self, repo_path: str, time_window_days: int = 365, high_churn_threshold: float = 5.0):
        """
        Initialize Git analyzer.
        
        Args:
            repo_path: Path to the repository or directory
            time_window_days: Number of days to analyze (default: 365)
            high_churn_threshold: Commits per year threshold for "high churn" files (default: 5.0)
        """
        self.repo_path = Path(repo_path)
        self.time_window_days = time_window_days
        self.high_churn_threshold = high_churn_threshold
        self.repo = None
        self._initialize_repo()
    
    def _initialize_repo(self) -> None:
        """Initialize Git repository object."""
        if not GIT_AVAILABLE:
            return
        
        # Check if path is a git repository
        git_dir = self.repo_path / '.git'
        if not git_dir.exists():
            # Try parent directories
            current = self.repo_path
            while current != current.parent:
                git_dir = current / '.git'
                if git_dir.exists():
                    self.repo_path = current
                    break
                current = current.parent
            else:
                # No git repository found
                return
        
        try:
            self.repo = Repo(str(self.repo_path))
        except (InvalidGitRepositoryError, Exception):
            # Repository is invalid or corrupted
            self.repo = None
    
    def is_available(self) -> bool:
        """Check if Git repository is available for analysis."""
        return self.repo is not None and GIT_AVAILABLE
    
    def analyze_churn(self) -> Dict[str, Any]:
        """
        Analyze commit history for file churn metrics.
        
        Returns:
            Dictionary containing churn analysis data
        """
        if not self.is_available():
            return self._get_neutral_values()
        
        try:
            # Calculate time window
            cutoff_date = datetime.now() - timedelta(days=self.time_window_days)
            
            # Track commits per file
            file_commits = defaultdict(int)
            file_last_change = {}
            
            # Iterate through commits in the time window
            for commit in self.repo.iter_commits():
                commit_date = datetime.fromtimestamp(commit.committed_date)
                
                # Stop if we've gone beyond the time window
                if commit_date < cutoff_date:
                    break
                
                # Count commits per file
                for file_path in commit.stats.files.keys():
                    # Normalize file paths (handle both forward and backward slashes)
                    normalized_path = file_path.replace('\\', '/')
                    file_commits[normalized_path] += 1
                    file_last_change[normalized_path] = max(
                        file_last_change.get(normalized_path, commit_date),
                        commit_date
                    )
            
            if not file_commits:
                return self._get_neutral_values()
            
            # Calculate churn rates (commits per year)
            file_churn_map = {}
            for file_path, commit_count in file_commits.items():
                # Normalize to commits per year
                days_since_first = (datetime.now() - file_last_change[file_path]).days
                if days_since_first > 0:
                    churn_rate = (commit_count / days_since_first) * 365.0
                else:
                    churn_rate = commit_count * 365.0  # If changed today, extrapolate
                file_churn_map[file_path] = churn_rate
            
            # Calculate average churn rate
            average_churn_rate = sum(file_churn_map.values()) / len(file_churn_map)
            
            # Identify high-churn files
            high_churn_files = [
                file_path for file_path, churn_rate in file_churn_map.items()
                if churn_rate >= self.high_churn_threshold
            ]
            
            return {
                "average_churn_rate": average_churn_rate,
                "file_churn_map": dict(file_churn_map),
                "high_churn_files": high_churn_files,
                "complexity_churn_ratio": 0.0,  # Will be calculated with static data
                "analysis_period_days": self.time_window_days,
                "total_files_tracked": len(file_churn_map),
                "total_commits_analyzed": sum(file_commits.values())
            }
            
        except Exception as e:
            # If analysis fails, return neutral values
            return self._get_neutral_values()
    
    def get_file_churn_rate(self, file_path: str) -> float:
        """
        Get churn rate for a specific file.
        
        Args:
            file_path: Relative path to the file
            
        Returns:
            Churn rate (commits per year), or 0.0 if not found
        """
        churn_data = self.analyze_churn()
        file_churn_map = churn_data.get("file_churn_map", {})
        
        # Try exact match first
        if file_path in file_churn_map:
            return file_churn_map[file_path]
        
        # Try normalized path
        normalized_path = file_path.replace('\\', '/')
        if normalized_path in file_churn_map:
            return file_churn_map[normalized_path]
        
        # Try reverse normalized
        reverse_normalized = file_path.replace('/', '\\')
        if reverse_normalized in file_churn_map:
            return file_churn_map[reverse_normalized]
        
        return 0.0
    
    def get_high_churn_files(self, threshold: Optional[float] = None) -> List[str]:
        """
        Get list of high-churn files.
        
        Args:
            threshold: Optional threshold override (uses instance default if None)
            
        Returns:
            List of file paths with high churn
        """
        if threshold is not None:
            # Temporarily override threshold
            old_threshold = self.high_churn_threshold
            self.high_churn_threshold = threshold
            churn_data = self.analyze_churn()
            self.high_churn_threshold = old_threshold
        else:
            churn_data = self.analyze_churn()
        
        return churn_data.get("high_churn_files", [])
    
    def calculate_complexity_churn_ratio(
        self,
        static_data: Dict[str, Any],
        file_churn_map: Optional[Dict[str, float]] = None
    ) -> float:
        """
        Calculate correlation between code complexity and churn rate.
        High complexity + high churn = problematic "hot spots".
        
        Args:
            static_data: Static analysis data from Radon/Lizard
            file_churn_map: Optional pre-calculated churn map
            
        Returns:
            Complexity-churn correlation ratio (higher = more problematic)
        """
        if not self.is_available():
            return 0.0
        
        if file_churn_map is None:
            churn_data = self.analyze_churn()
            file_churn_map = churn_data.get("file_churn_map", {})
        
        if not file_churn_map:
            return 0.0
        
        # Get complexity data from static analysis
        radon_complexity = static_data.get("radon_complexity", {})
        file_stats = radon_complexity.get("file_stats", {})
        
        if not file_stats:
            return 0.0
        
        # Match files between complexity and churn data
        complexity_churn_pairs = []
        
        for file_path, complexity in file_stats.items():
            # Try to find matching churn rate
            normalized_path = file_path.replace('\\', '/')
            churn_rate = file_churn_map.get(normalized_path, 0.0)
            
            if churn_rate > 0:
                # Use lines of code as complexity proxy if available
                # Otherwise use average complexity
                complexity_score = complexity if isinstance(complexity, (int, float)) else 1.0
                complexity_churn_pairs.append((complexity_score, churn_rate))
        
        if not complexity_churn_pairs:
            return 0.0
        
        # Calculate weighted average: sum(complexity * churn) / sum(complexity)
        total_weighted_churn = sum(comp * churn for comp, churn in complexity_churn_pairs)
        total_complexity = sum(comp for comp, _ in complexity_churn_pairs)
        
        if total_complexity == 0:
            return 0.0
        
        # Return average churn weighted by complexity
        return total_weighted_churn / total_complexity
    
    def _get_neutral_values(self) -> Dict[str, Any]:
        """Return neutral/default values when Git is not available."""
        return {
            "average_churn_rate": 1.0,  # Neutral value (1 commit per year)
            "file_churn_map": {},
            "high_churn_files": [],
            "complexity_churn_ratio": 0.0,
            "analysis_period_days": self.time_window_days,
            "total_files_tracked": 0,
            "total_commits_analyzed": 0
        }
