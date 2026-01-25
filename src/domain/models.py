"""
Pydantic models for MSI metrics.
Defines the core data structures for Repairability, ChangeEffort, and LegacyCompatibility.
"""

from __future__ import annotations

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


class GitAnalysisData(BaseModel):
    """Raw data from Git history analysis."""
    
    average_churn_rate: float = Field(..., description="Average commits per file per year")
    file_churn_map: Dict[str, float] = Field(default_factory=dict, description="File path -> churn rate mapping")
    high_churn_files: List[str] = Field(default_factory=list, description="Files with churn above threshold")
    complexity_churn_ratio: float = Field(..., description="Correlation between complexity and churn")
    analysis_period_days: int = Field(..., description="Time window analyzed in days")
    total_files_tracked: int = Field(default=0, description="Total number of files with commit history")
    total_commits_analyzed: int = Field(default=0, description="Total commits analyzed in the time window")


class MSIResult(BaseModel):
    """Complete MSI audit result."""
    
    # Input metadata
    target_path: str = Field(..., description="Path or URL of the analyzed repository")
    analysis_timestamp: str = Field(..., description="ISO timestamp of the analysis")
    
    # Raw data
    static_analysis: StaticAnalysisData = Field(..., description="Raw static analysis data")
    ai_analysis: Optional[AIAnalysisData] = Field(None, description="Raw AI analysis data")
    git_analysis: Optional["GitAnalysisData"] = Field(None, description="Raw Git history analysis data")
    
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
