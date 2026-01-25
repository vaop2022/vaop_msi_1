# Phase 2 Technical Specification: Pilot & Calibration
**Duration:** Days 46-75 (30 days)  
**Status:** Planning

---

## 1. Executive Summary

Phase 2 focuses on **completing hard metrics** that were placeholders in Phase 1, implementing **real-world testing** on benchmark repositories, and **calibrating** the MSI scoring algorithm based on empirical data.

### Key Objectives:
1. ✅ Implement Git history analysis (churn rate calculation)
2. ✅ Implement API stability checks (SemVer analysis)
3. ✅ Implement migration test coverage detection
4. ✅ Create benchmark testing framework
5. ✅ Calibrate scoring weights based on real-world data
6. ✅ Validate correlation between MSI scores and actual maintenance complexity

---

## 2. Architecture Design

### 2.1. New Adapters (Infrastructure Layer)

Following the Clean Architecture principle, we will add three new adapters in `src/adapters/`:

#### 2.1.1. `git_analyzer.py` - Git History Analysis Adapter
**Purpose:** Extract churn metrics from Git repository history.

**Responsibilities:**
- Analyze commit history for file change frequency
- Calculate churn rate per file (commits per file over time period)
- Identify high-churn files (files changed frequently)
- Calculate complexity-churn correlation
- Detect "hot spots" (complex files that change often)

**Dependencies:**
- `GitPython` (already in requirements.txt)
- Git repository must be initialized (`.git` directory present)

**Key Methods:**
```python
class GitAnalyzer:
    def __init__(self, repo_path: str)
    def analyze_churn(self, time_window_days: int = 365) -> Dict[str, Any]
    def get_file_churn_rate(self, file_path: str) -> float
    def get_high_churn_files(self, threshold: float = 5.0) -> List[str]
    def calculate_complexity_churn_ratio(self, static_data: Dict) -> float
```

**Output Structure:**
```python
{
    "average_churn_rate": float,  # Average commits per file
    "file_churn_map": Dict[str, float],  # File path -> churn rate
    "high_churn_files": List[str],  # Files with churn > threshold
    "complexity_churn_ratio": float,  # Correlation metric
    "analysis_period_days": int
}
```

**Architectural Notes:**
- This adapter is **optional** - if no `.git` directory exists, it returns neutral values
- Follows adapter pattern: isolates GitPython dependency from domain logic
- Returns raw data, normalization happens in service layer

---

#### 2.1.2. `api_stability_analyzer.py` - API Stability & SemVer Adapter
**Purpose:** Analyze API stability and versioning compliance.

**Responsibilities:**
- Detect version files (`version.py`, `__version__.py`, `setup.py`, `pyproject.toml`)
- Parse SemVer strings (major.minor.patch)
- Analyze version history for breaking changes
- Check for API deprecation markers
- Detect public API surface (functions/classes with public visibility)

**Dependencies:**
- `ast` (standard library) - for parsing Python AST
- `toml` (for `pyproject.toml` parsing) - add to requirements.txt
- Git history (via GitAnalyzer) for version change tracking

**Key Methods:**
```python
class APIStabilityAnalyzer:
    def __init__(self, repo_path: str, git_analyzer: Optional[GitAnalyzer] = None)
    def analyze_api_stability(self) -> Dict[str, Any]
    def detect_version_files(self) -> List[Path]
    def parse_semver(self, version_string: str) -> Optional[SemVer]
    def analyze_breaking_changes(self) -> Dict[str, Any]
    def detect_public_api_surface(self) -> Dict[str, Any]
```

**Output Structure:**
```python
{
    "api_stability_score": float,  # 0-100
    "version_info": {
        "current_version": str,
        "version_history": List[Dict],
        "breaking_changes_count": int,
        "semver_compliant": bool
    },
    "public_api_surface": {
        "public_functions": int,
        "public_classes": int,
        "deprecated_count": int
    }
}
```

**Architectural Notes:**
- Works independently of Git (can analyze current state)
- Enhanced with Git history if available (more accurate)
- Uses AST parsing to detect public APIs (naming conventions)

---

#### 2.1.3. `test_coverage_analyzer.py` - Migration Test Coverage Adapter
**Purpose:** Detect migration tests and backward compatibility test coverage.

**Responsibilities:**
- Scan for test files (pytest, unittest patterns)
- Identify migration-related tests (keywords: "migration", "backward", "compatibility", "legacy")
- Analyze test coverage for API changes
- Detect version-specific test suites
- Calculate migration test coverage percentage

**Dependencies:**
- `ast` (standard library) - for parsing test files
- File system scanning

**Key Methods:**
```python
class TestCoverageAnalyzer:
    def __init__(self, repo_path: str)
    def analyze_migration_coverage(self) -> Dict[str, Any]
    def find_test_files(self) -> List[Path]
    def detect_migration_tests(self, test_files: List[Path]) -> List[Path]
    def calculate_coverage_percentage(self) -> float
```

**Output Structure:**
```python
{
    "migration_test_coverage": float,  # 0-100 percentage
    "total_test_files": int,
    "migration_test_files": List[str],
    "backward_compatibility_tests": int,
    "version_specific_tests": int
}
```

**Architectural Notes:**
- Heuristic-based (searches for keywords in test names/comments)
- Can be enhanced with actual test coverage tools (coverage.py) in future
- Returns percentage, not absolute numbers (normalized)

---

### 2.2. Domain Model Updates

#### 2.2.1. New Data Models

Add to `src/domain/models.py`:

```python
class GitAnalysisData(BaseModel):
    """Raw data from Git history analysis."""
    average_churn_rate: float
    file_churn_map: Dict[str, float]
    high_churn_files: List[str]
    complexity_churn_ratio: float
    analysis_period_days: int

class APIStabilityData(BaseModel):
    """Raw data from API stability analysis."""
    api_stability_score: float
    version_info: Dict[str, Any]
    public_api_surface: Dict[str, Any]

class TestCoverageData(BaseModel):
    """Raw data from test coverage analysis."""
    migration_test_coverage: float
    total_test_files: int
    migration_test_files: List[str]
```

#### 2.2.2. Update Existing Models

Update `MSIResult` to include new raw data:
```python
class MSIResult(BaseModel):
    # ... existing fields ...
    git_analysis: Optional[GitAnalysisData] = None
    api_stability_data: Optional[APIStabilityData] = None
    test_coverage_data: Optional[TestCoverageData] = None
```

---

### 2.3. Service Layer Updates

#### 2.3.1. Update `MSICalculator` Service

**Changes to `_calculate_change_effort()`:**
- Replace placeholder churn_rate with actual Git data
- Use `GitAnalyzer` to get real churn metrics
- Calculate complexity-churn correlation
- Identify high-churn files

**Changes to `_calculate_legacy_compatibility()`:**
- Replace placeholder api_stability with `APIStabilityAnalyzer` results
- Replace placeholder migration_coverage with `TestCoverageAnalyzer` results
- Use real SemVer data for scoring

**New Method:**
```python
def _integrate_git_data(self, static_data: StaticAnalysisData, git_data: Optional[GitAnalysisData]) -> Dict[str, Any]
```

---

### 2.4. Benchmark Testing Framework

**New Module:** `src/services/benchmark_runner.py`

**Purpose:** Automated testing on benchmark repositories to validate and calibrate MSI scores.

**Responsibilities:**
- Run MSI analysis on predefined benchmark repositories
- Compare results against expected scores
- Generate calibration reports
- Validate correlation between MSI and real maintenance complexity

**Benchmark Repositories:**
1. **High MSI Expected (Gold):**
   - `scikit-learn/scikit-learn` - Well-architected ML library
   - `pytorch/pytorch` - Large but modular codebase
   
2. **Medium MSI Expected (Silver):**
   - `facebook/react` - Good architecture, but framework-dependent
   - `django/django` - Mature but legacy patterns
   
3. **Low MSI Expected (Basic):**
   - Legacy PHP monoliths (if available)
   - Tightly-coupled projects

**Key Methods:**
```python
class BenchmarkRunner:
    def __init__(self, msi_calculator: MSICalculator)
    def run_benchmark_suite(self) -> Dict[str, Any]
    def analyze_repository(self, repo_url: str, expected_rating: MSIRating) -> Dict[str, Any]
    def generate_calibration_report(self) -> Dict[str, Any]
    def validate_correlation(self) -> float  # Returns correlation coefficient
```

---

### 2.5. Calibration System

**New Module:** `src/services/calibration.py`

**Purpose:** Adjust scoring weights based on empirical data from benchmarks.

**Responsibilities:**
- Analyze benchmark results
- Identify misaligned scores (e.g., Gold project scoring as Basic)
- Suggest weight adjustments
- Apply calibrated weights to MSI calculation

**Calibration Process:**
1. Run benchmarks on known-good and known-bad projects
2. Identify discrepancies between expected and actual scores
3. Adjust weights in `MSICalculator` to align with expectations
4. Validate on holdout set of repositories

**Key Methods:**
```python
class CalibrationService:
    def __init__(self, benchmark_results: List[Dict])
    def analyze_discrepancies(self) -> Dict[str, Any]
    def suggest_weight_adjustments(self) -> Dict[str, float]
    def apply_calibration(self, new_weights: Dict[str, float])
```

---

## 3. Implementation Plan

### Week 1 (Days 46-52): Git Analysis Implementation
- [ ] Create `GitAnalyzer` adapter
- [ ] Implement churn rate calculation
- [ ] Integrate with `MSICalculator`
- [ ] Update `ChangeEffortMetrics` calculation
- [ ] Unit tests for Git analyzer

### Week 2 (Days 53-59): API Stability & Test Coverage
- [ ] Create `APIStabilityAnalyzer` adapter
- [ ] Create `TestCoverageAnalyzer` adapter
- [ ] Implement SemVer parsing
- [ ] Integrate with `LegacyCompatibilityMetrics`
- [ ] Unit tests for both analyzers

### Week 3 (Days 60-66): Benchmark Framework
- [ ] Create `BenchmarkRunner` service
- [ ] Set up benchmark repository list
- [ ] Implement automated testing
- [ ] Generate benchmark reports
- [ ] Validate initial correlations

### Week 4 (Days 67-75): Calibration & Validation
- [ ] Create `CalibrationService`
- [ ] Run full benchmark suite
- [ ] Analyze discrepancies
- [ ] Adjust scoring weights
- [ ] Final validation on holdout set
- [ ] Document calibration results

---

## 4. Technical Decisions

### 4.1. Git Analysis Time Window
**Decision:** Default to 365 days (1 year) of history
**Rationale:** Balances recent changes with long-term patterns
**Configurable:** Via parameter in `GitAnalyzer.__init__()`

### 4.2. Churn Rate Threshold
**Decision:** Files with >5 commits/year are "high churn"
**Rationale:** Based on industry standards (CodeScene, etc.)
**Configurable:** Via parameter

### 4.3. SemVer Detection Strategy
**Decision:** Multi-file detection (version.py, setup.py, pyproject.toml)
**Rationale:** Different projects use different conventions
**Fallback:** If no version found, assume unstable (score = 0)

### 4.4. Migration Test Detection
**Decision:** Heuristic-based (keyword search in test names/comments)
**Rationale:** More reliable than trying to parse test logic
**Future Enhancement:** Integrate with coverage.py for actual coverage

### 4.5. Benchmark Repository Selection
**Decision:** Focus on Python repositories initially
**Rationale:** Our static analyzers (Radon, Lizard) are Python-specific
**Future:** Extend to other languages in Phase 3

---

## 5. Dependencies & Requirements

### New Python Packages:
```python
# Add to requirements.txt
toml>=0.10.2  # For pyproject.toml parsing
```

### System Requirements:
- Git must be installed (for GitPython)
- Internet access for cloning benchmark repositories (optional, can use local clones)

---

## 6. Testing Strategy

### 6.1. Unit Tests
- Test each adapter independently
- Mock Git repository for `GitAnalyzer` tests
- Test edge cases (no Git repo, no version files, no tests)

### 6.2. Integration Tests
- Test full MSI calculation with all adapters
- Test benchmark runner end-to-end
- Validate calibration process

### 6.3. Validation Tests
- Run on known-good repositories (should score Gold)
- Run on known-bad repositories (should score Basic)
- Verify correlation coefficient > 0.7

---

## 7. Success Criteria

### Phase 2 is complete when:
1. ✅ All three new adapters are implemented and tested
2. ✅ `ChangeEffortMetrics` uses real Git churn data (no placeholders)
3. ✅ `LegacyCompatibilityMetrics` uses real API stability and test coverage data
4. ✅ Benchmark framework runs successfully on 5+ repositories
5. ✅ Calibration system produces weights that align with expected scores
6. ✅ Correlation between MSI scores and actual maintenance complexity > 0.7
7. ✅ All unit tests pass
8. ✅ Documentation updated

---

## 8. Risk Mitigation

### Risk 1: Git repository not available
**Mitigation:** Adapters return neutral/default values, analysis continues

### Risk 2: Benchmark repositories unavailable
**Mitigation:** Use local clones, provide instructions for manual setup

### Risk 3: Calibration doesn't converge
**Mitigation:** Manual weight adjustment based on domain expertise, document rationale

### Risk 4: Performance issues with large repositories
**Mitigation:** Add caching, limit analysis depth, add progress indicators

---

## 9. Documentation Updates

### Files to Update:
- `docs/01_architecture_overview.md` - Add new adapters
- `docs/02_setup_guide.md` - Add Git requirements
- `README.md` - Update with Phase 2 features
- Create `docs/04_benchmark_results.md` - Benchmark findings
- Create `docs/05_calibration_report.md` - Calibration methodology

---

## 10. Next Steps (Phase 3 Preview)

After Phase 2 completion, Phase 3 will focus on:
- Web interface (Streamlit)
- Report generation (Markdown/PDF)
- GitHub API integration for remote repository analysis
- Multi-language support
- Whitepaper documentation

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-25  
**Author:** AI Architect (Cursor)
