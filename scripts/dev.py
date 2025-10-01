#!/usr/bin/env python3
"""
PicFrame Development Helper Script

This script provides convenient commands for common development tasks.
Usage: python scripts/dev.py <command> [options]
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent

def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result."""
    if cwd is None:
        cwd = PROJECT_ROOT
    
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(
        cmd, 
        cwd=cwd, 
        shell=isinstance(cmd, str),
        check=check,
        capture_output=False
    )
    return result.returncode == 0

def setup_dev_environment():
    """Set up the development environment."""
    print("Setting up PicFrame development environment...")
    
    # Check if virtual environment exists
    venv_path = PROJECT_ROOT / "venv"
    if not venv_path.exists():
        print("Creating virtual environment...")
        run_command([sys.executable, "-m", "venv", "venv"])
    
    # Determine activation script
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate.bat"
        pip_path = venv_path / "Scripts" / "pip"
    else:  # Unix-like
        activate_script = venv_path / "bin" / "activate"
        pip_path = venv_path / "bin" / "pip"
    
    # Install PicFrame in development mode
    print("Installing PicFrame in development mode...")
    run_command([str(pip_path), "install", "-e", "."])
    
    # Install development dependencies
    print("Installing development dependencies...")
    run_command([str(pip_path), "install", "-r", "requirements-dev.txt"])
    
    # Install pre-commit hooks
    print("Installing pre-commit hooks...")
    pre_commit_path = venv_path / ("Scripts" if os.name == 'nt' else "bin") / "pre-commit"
    run_command([str(pre_commit_path), "install"])
    
    print("Development environment setup complete!")
    print(f"Activate with: source {activate_script}")

def run_tests(test_type="all", coverage=False, verbose=False):
    """Run tests with various options."""
    cmd = ["python", "-m", "pytest"]
    
    if test_type == "unit":
        cmd.append("test/unit/")
    elif test_type == "integration":
        cmd.append("test/integration/")
    elif test_type == "fast":
        cmd.extend(["-m", "not slow"])
    
    if coverage:
        cmd.extend(["--cov=src/picframe", "--cov-report=html", "--cov-report=term-missing"])
    
    if verbose:
        cmd.append("-v")
    
    return run_command(cmd)

def format_code():
    """Format code with Black and isort."""
    print("Formatting code with Black...")
    run_command(["python", "-m", "black", "src/", "test/"])
    
    print("Sorting imports with isort...")
    run_command(["python", "-m", "isort", "src/", "test/"])
    
    print("Code formatting complete!")

def run_linting():
    """Run linting checks."""
    print("Running flake8...")
    success = run_command(["python", "-m", "flake8", "src/", "test/"], check=False)
    
    print("Running pylint...")
    success &= run_command(["python", "-m", "pylint", "src/picframe/"], check=False)
    
    return success

def run_type_checking():
    """Run type checking with mypy."""
    print("Running mypy type checking...")
    return run_command(["python", "-m", "mypy", "src/"], check=False)

def run_security_check():
    """Run security checks with bandit."""
    print("Running bandit security checks...")
    return run_command(["python", "-m", "bandit", "-r", "src/"], check=False)

def clean_project():
    """Clean build artifacts and cache files."""
    print("Cleaning project...")
    
    # Directories to remove
    dirs_to_remove = [
        "build", "dist", ".pytest_cache", "htmlcov", ".mypy_cache",
        "src/picframe.egg-info"
    ]
    
    for dir_name in dirs_to_remove:
        dir_path = PROJECT_ROOT / dir_name
        if dir_path.exists():
            print(f"Removing {dir_path}")
            import shutil
            shutil.rmtree(dir_path)
    
    # Files to remove
    files_to_remove = [".coverage"]
    for file_name in files_to_remove:
        file_path = PROJECT_ROOT / file_name
        if file_path.exists():
            print(f"Removing {file_path}")
            file_path.unlink()
    
    # Remove __pycache__ directories
    for pycache in PROJECT_ROOT.rglob("__pycache__"):
        print(f"Removing {pycache}")
        import shutil
        shutil.rmtree(pycache)
    
    # Remove .pyc files
    for pyc_file in PROJECT_ROOT.rglob("*.pyc"):
        print(f"Removing {pyc_file}")
        pyc_file.unlink()
    
    print("Project cleaned!")

def run_picframe_debug():
    """Run PicFrame in debug mode."""
    config_path = PROJECT_ROOT / "test" / "fixtures" / "configs" / "debug_config.yaml"
    print(f"Running PicFrame with debug configuration: {config_path}")
    return run_command(["python", "-m", "picframe.start", str(config_path)])

def check_version():
    """Check PicFrame version and dependencies."""
    print("Checking PicFrame version and dependencies...")
    return run_command(["python", "-m", "picframe.start", "-v"])

def main():
    """Main entry point for the development script."""
    parser = argparse.ArgumentParser(description="PicFrame Development Helper")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Setup command
    subparsers.add_parser("setup", help="Set up development environment")
    
    # Test commands
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument("--type", choices=["all", "unit", "integration", "fast"], 
                           default="all", help="Type of tests to run")
    test_parser.add_argument("--coverage", action="store_true", help="Run with coverage")
    test_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    # Code quality commands
    subparsers.add_parser("format", help="Format code with Black and isort")
    subparsers.add_parser("lint", help="Run linting checks")
    subparsers.add_parser("typecheck", help="Run type checking")
    subparsers.add_parser("security", help="Run security checks")
    
    # Utility commands
    subparsers.add_parser("clean", help="Clean build artifacts and cache")
    subparsers.add_parser("debug", help="Run PicFrame in debug mode")
    subparsers.add_parser("version", help="Check version and dependencies")
    
    # All-in-one commands
    subparsers.add_parser("check", help="Run all code quality checks")
    subparsers.add_parser("ci", help="Run CI-like checks (format, lint, typecheck, test)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Change to project directory
    os.chdir(PROJECT_ROOT)
    
    success = True
    
    if args.command == "setup":
        setup_dev_environment()
    elif args.command == "test":
        success = run_tests(args.type, args.coverage, args.verbose)
    elif args.command == "format":
        format_code()
    elif args.command == "lint":
        success = run_linting()
    elif args.command == "typecheck":
        success = run_type_checking()
    elif args.command == "security":
        success = run_security_check()
    elif args.command == "clean":
        clean_project()
    elif args.command == "debug":
        success = run_picframe_debug()
    elif args.command == "version":
        success = check_version()
    elif args.command == "check":
        format_code()
        success = run_linting() and run_type_checking() and run_security_check()
    elif args.command == "ci":
        format_code()
        success = (run_linting() and 
                  run_type_checking() and 
                  run_security_check() and 
                  run_tests("all", coverage=True))
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())