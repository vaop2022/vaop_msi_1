"""
MSI v0.1 - Methodological Sustainability Index Calculator
Entry point for CLI application.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
import typer
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from services.msi_calculator import MSICalculator

# Initialize Typer app and Rich console
app = typer.Typer()
console = Console()


def _is_github_url(path: str) -> bool:
    """Check if path is a GitHub URL."""
    github_pattern = r'^https?://(www\.)?github\.com/[\w\-]+/[\w\-]+/?$'
    return bool(re.match(github_pattern, path))


def _clone_github_repo(url: str, temp_dir: Path) -> Path:
    """
    Clone GitHub repository to temporary directory.
    
    Args:
        url: GitHub repository URL
        temp_dir: Temporary directory for cloning
        
    Returns:
        Path to cloned repository
    """
    try:
        # Extract repo name from URL
        repo_name = url.rstrip('/').split('/')[-1]
        clone_path = temp_dir / repo_name
        
        console.print(f"[yellow]Cloning repository:[/yellow] {url}")
        
        # Clone repository
        result = subprocess.run(
            ['git', 'clone', url, str(clone_path)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Failed to clone repository: {result.stderr}")
        
        console.print(f"[green]✓[/green] Repository cloned to: {clone_path}")
        return clone_path
        
    except subprocess.TimeoutExpired:
        raise RuntimeError("Repository cloning timed out after 5 minutes")
    except FileNotFoundError:
        raise RuntimeError("Git not found. Please install Git to clone repositories.")


@app.command()
def audit(
    path: str = typer.Argument(..., help="Path to the repository/folder to audit, or GitHub URL (e.g., https://github.com/user/repo)"),
    output: str = typer.Option("console", "--output", "-o", help="Output format: 'console' or 'json'"),
    no_ai: bool = typer.Option(False, "--no-ai", help="Skip AI analysis (faster, less accurate)"),
    api_key: str = typer.Option(None, "--api-key", help="Gemini API key (overrides .env)"),
    keep_clone: bool = typer.Option(False, "--keep-clone", help="Keep cloned repository after analysis (only for GitHub URLs)")
):
    """
    Runs the MSI (Methodological Sustainability Index) audit on the specified path or GitHub URL.
    
    Examples:
        python src/main.py audit ./my_project
        python src.main audit https://github.com/vaop2022/va-calc-6-new
        python src/main.py audit ./my_project --output json > results.json
    """
    console.print(Panel.fit(
        f"Starting MSI Audit for: [bold cyan]{path}[/bold cyan]",
        title="VAOP MSI v0.1"
    ))
    
    temp_dir = None
    target_path = None
    
    # Check if path is a GitHub URL
    if _is_github_url(path):
        # Clone repository to temporary directory
        temp_dir = Path(tempfile.mkdtemp(prefix="msi_audit_"))
        try:
            target_path = _clone_github_repo(path, temp_dir)
        except Exception as e:
            console.print(f"[bold red]Error cloning repository:[/bold red] {str(e)}")
            if temp_dir and temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
            raise typer.Exit(1)
    else:
        # Use path as-is
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
            # Cleanup temporary directory if it was created
            if temp_dir and temp_dir.exists() and not keep_clone:
                shutil.rmtree(temp_dir, ignore_errors=True)
            raise typer.Exit(1)
    
    # Output results
    if output == "json":
        # JSON output for programmatic use
        output_dict = result.model_dump(mode="json")
        print(json.dumps(output_dict, indent=2))
    else:
        # Rich console output
        _display_results(console, result)
    
    # Cleanup temporary directory if it was created
    if temp_dir and temp_dir.exists() and not keep_clone:
        console.print(f"\n[dim]Cleaning up temporary directory...[/dim]")
        shutil.rmtree(temp_dir, ignore_errors=True)
    elif temp_dir and keep_clone:
        console.print(f"\n[yellow]Repository kept at:[/yellow] {target_path}")


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
