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
