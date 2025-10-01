# Development Environment Setup Guide

This guide provides comprehensive instructions for setting up a development environment for PicFrame across different platforms, including debugging and testing procedures.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Platform-Specific Setup](#platform-specific-setup)
- [Development Dependencies](#development-dependencies)
- [IDE Configuration](#ide-configuration)
- [Debugging Setup](#debugging-setup)
- [Testing Environment](#testing-environment)
- [Hardware Testing Setup](#hardware-testing-setup)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

**Minimum Requirements:**
- Python 3.7 or higher
- Git 2.20+
- 4GB RAM (8GB recommended)
- 2GB free disk space

**Recommended Requirements:**
- Python 3.9+ for best compatibility
- Git 2.30+
- 8GB+ RAM
- SSD storage for faster development

### Required System Libraries

The following system libraries are required for PicFrame development:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y \
    python3-dev \
    python3-pip \
    python3-venv \
    git \
    build-essential \
    libgl1-mesa-dev \
    libgles2-mesa-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libffi-dev \
    libssl-dev \
    libyaml-dev \
    libopencv-dev \
    python3-opencv
```

**macOS:**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.9 git jpeg libpng freetype opencv
```

**Windows:**
```powershell
# Install Python from python.org or Microsoft Store
# Install Git from git-scm.com
# Install Visual Studio Build Tools for C++ compilation
```

## Platform-Specific Setup

### Linux Development Setup

#### 1. Clone Repository
```bash
git clone https://github.com/helgeerbe/picframe.git
cd picframe
```

#### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Development Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install PicFrame in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

#### 4. Verify Installation
```bash
python -m picframe.start -v
```

### macOS Development Setup

#### 1. Install Xcode Command Line Tools
```bash
xcode-select --install
```

#### 2. Clone and Setup
```bash
git clone https://github.com/helgeerbe/picframe.git
cd picframe

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -e .
pip install -r requirements-dev.txt
```

#### 3. Handle macOS-Specific Issues
```bash
# If you encounter OpenGL issues
export SYSTEM_VERSION_COMPAT=1

# For M1/M2 Macs, you might need specific versions
pip install --upgrade pillow
```

### Windows Development Setup

#### 1. Install Python and Git
- Download Python 3.9+ from [python.org](https://python.org)
- Download Git from [git-scm.com](https://git-scm.com)
- Install Visual Studio Build Tools

#### 2. Setup Development Environment
```cmd
# Clone repository
git clone https://github.com/helgeerbe/picframe.git
cd picframe

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
python -m pip install --upgrade pip
pip install -e .
pip install -r requirements-dev.txt
```

#### 3. Windows-Specific Configuration
```cmd
# Set environment variables for OpenGL
set MESA_GL_VERSION_OVERRIDE=3.3
set MESA_GLSL_VERSION_OVERRIDE=330
```

### Raspberry Pi Development Setup

#### 1. Prepare Raspberry Pi OS
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y \
    python3-dev \
    python3-pip \
    python3-venv \
    git \
    build-essential \
    libgl1-mesa-dev \
    libgles2-mesa-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    python3-opencv
```

#### 2. Clone and Setup
```bash
git clone https://github.com/helgeerbe/picframe.git
cd picframe

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install with Raspberry Pi optimizations
pip install --upgrade pip
pip install -e .
pip install -r requirements-dev.txt
```

#### 3. Enable GPU Memory Split
```bash
# Edit config
sudo nano /boot/config.txt

# Add or modify:
gpu_mem=128

# Reboot
sudo reboot
```

## Development Dependencies

### Core Development Tools

Create `requirements-dev.txt` with essential development dependencies:

```text
# Code formatting and linting
black>=23.0.0
isort>=5.12.0
flake8>=6.0.0
pylint>=2.17.0
bandit>=1.7.5

# Type checking
mypy>=1.0.0
types-PyYAML
types-requests

# Testing
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
pytest-asyncio>=0.21.0
pytest-xdist>=3.0.0

# Documentation
sphinx>=6.0.0
sphinx-rtd-theme>=1.2.0

# Development utilities
pre-commit>=3.0.0
tox>=4.0.0
ipython>=8.0.0
ipdb>=0.13.0

# Build and release
build>=0.10.0
twine>=4.0.0
```

### Install Development Dependencies
```bash
pip install -r requirements-dev.txt
```

### Setup Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run hooks on all files (optional)
pre-commit run --all-files
```

## IDE Configuration

### Visual Studio Code

#### 1. Install Recommended Extensions
Create `.vscode/extensions.json`:
```json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.flake8",
        "ms-python.pylint",
        "ms-python.mypy-type-checker",
        "ms-python.debugpy",
        "redhat.vscode-yaml",
        "ms-vscode.test-adapter-converter",
        "littlefoxteam.vscode-python-test-adapter"
    ]
}
```

#### 2. Configure Workspace Settings
Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.mypyEnabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "test"
    ],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".pytest_cache": true,
        ".coverage": true,
        "htmlcov": true
    },
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

#### 3. Configure Launch Configuration
Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "PicFrame Debug",
            "type": "python",
            "request": "launch",
            "module": "picframe.start",
            "args": ["test/fixtures/configs/debug_config.yaml"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src"
            }
        },
        {
            "name": "PicFrame Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["test/", "-v"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "PicFrame Version Check",
            "type": "python",
            "request": "launch",
            "module": "picframe.start",
            "args": ["-v"],
            "console": "integratedTerminal"
        }
    ]
}
```

### PyCharm

#### 1. Project Setup
- Open PicFrame directory as project
- Configure Python interpreter to use virtual environment
- Mark `src` directory as Sources Root
- Mark `test` directory as Test Sources Root

#### 2. Configure Code Style
- Go to Settings → Editor → Code Style → Python
- Set line length to 88 (Black default)
- Enable "Use tabs and indents" → Spaces only

#### 3. Configure Tools
- Settings → Tools → External Tools
- Add Black formatter
- Add Flake8 linter
- Configure pytest as test runner

## Debugging Setup

### Python Debugger (pdb)

#### 1. Basic Debugging
```python
import pdb

def problematic_function():
    # Set breakpoint
    pdb.set_trace()
    # Your code here
    pass
```

#### 2. Enhanced Debugging with ipdb
```bash
pip install ipdb
```

```python
import ipdb

def debug_image_processing():
    ipdb.set_trace()
    # Debug image processing logic
    pass
```

### Remote Debugging (Raspberry Pi)

#### 1. Install debugpy on Raspberry Pi
```bash
pip install debugpy
```

#### 2. Start Debug Server
```python
import debugpy

# Start debug server
debugpy.listen(("0.0.0.0", 5678))
print("Waiting for debugger to attach...")
debugpy.wait_for_client()

# Your PicFrame code here
```

#### 3. Connect from Development Machine
In VS Code, create launch configuration:
```json
{
    "name": "Remote Debug Raspberry Pi",
    "type": "python",
    "request": "attach",
    "connect": {
        "host": "192.168.1.100",  // Raspberry Pi IP
        "port": 5678
    },
    "pathMappings": [
        {
            "localRoot": "${workspaceFolder}",
            "remoteRoot": "/home/pi/picframe"
        }
    ]
}
```

### Logging Configuration for Development

Create `debug_logging.yaml`:
```yaml
version: 1
formatters:
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
  simple:
    format: '%(levelname)s - %(message)s'

handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: detailed
    stream: ext://sys.stdout
  
  file:
    class: logging.FileHandler
    level: DEBUG
    formatter: detailed
    filename: debug.log
    mode: w

loggers:
  picframe:
    level: DEBUG
    handlers: [console, file]
    propagate: false

root:
  level: INFO
  handlers: [console]
```

Use in development:
```python
import logging.config
import yaml

with open('debug_logging.yaml') as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger('picframe')
logger.debug("Debug message")
```

## Testing Environment

### Unit Testing Setup

#### 1. Test Directory Structure
```
test/
├── unit/
│   ├── test_controller.py
│   ├── test_model.py
│   ├── test_image_cache.py
│   └── test_interfaces/
├── integration/
│   ├── test_mqtt_integration.py
│   └── test_http_integration.py
├── fixtures/
│   ├── images/
│   ├── configs/
│   └── mock_data/
└── conftest.py
```

#### 2. Pytest Configuration
Create `pytest.ini`:
```ini
[tool:pytest]
testpaths = test
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --strict-config
    --verbose
    --tb=short
    --cov=src/picframe
    --cov-report=term-missing
    --cov-report=html
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    hardware: marks tests requiring hardware
```

#### 3. Test Fixtures
Create `test/conftest.py`:
```python
import pytest
import tempfile
import shutil
from pathlib import Path
from PIL import Image

@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)

@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        'display': {'width': 1920, 'height': 1080},
        'slideshow': {'duration': 10, 'fade_time': 1.0},
        'image_dir': 'test/fixtures/images'
    }

@pytest.fixture
def mock_image():
    """Create mock image for testing."""
    return Image.new('RGB', (100, 100), color='red')
```

### Running Tests

#### 1. Basic Test Execution
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/picframe

# Run specific test categories
pytest -m "not slow"
pytest -m integration
pytest -m hardware

# Run specific test files
pytest test/unit/test_controller.py
pytest test/integration/test_mqtt_integration.py -v
```

#### 2. Parallel Testing
```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel
pytest -n auto
pytest -n 4  # Use 4 processes
```

#### 3. Test Coverage Analysis
```bash
# Generate HTML coverage report
pytest --cov=src/picframe --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Hardware Testing Setup

### Raspberry Pi Testing Environment

#### 1. Test Configuration
Create `test/fixtures/configs/rpi_test_config.yaml`:
```yaml
display:
  width: 1920
  height: 1080
  fullscreen: false  # For testing
  
slideshow:
  duration: 5  # Shorter for testing
  fade_time: 0.5
  
image_dir: "/home/pi/test_images"

mqtt:
  broker: "localhost"
  port: 1883
  
http:
  port: 8080
  host: "0.0.0.0"
```

#### 2. Mock Hardware Interfaces
```python
# test/mocks/hardware_mocks.py
class MockGPIO:
    """Mock GPIO interface for testing."""
    
    def __init__(self):
        self.pins = {}
    
    def setup(self, pin, mode):
        self.pins[pin] = {'mode': mode, 'value': 0}
    
    def input(self, pin):
        return self.pins.get(pin, {}).get('value', 0)

class MockDisplay:
    """Mock display interface for testing."""
    
    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height
        self.is_open = False
    
    def create(self):
        self.is_open = True
    
    def destroy(self):
        self.is_open = False
```

#### 3. Hardware Test Markers
```python
# test/conftest.py
import pytest

def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers", "hardware: mark test as requiring hardware"
    )
    config.addinivalue_line(
        "markers", "rpi: mark test as Raspberry Pi specific"
    )

@pytest.fixture
def skip_if_no_hardware():
    """Skip test if hardware is not available."""
    try:
        import RPi.GPIO
        return False
    except ImportError:
        pytest.skip("Hardware not available")
```

### Integration Testing

#### 1. MQTT Testing
```bash
# Install mosquitto for testing
sudo apt install mosquitto mosquitto-clients

# Start test broker
mosquitto -p 1883 -v

# Test MQTT in another terminal
mosquitto_pub -h localhost -t "picframe/test/command" -m "next"
```

#### 2. HTTP Testing
```python
# test/integration/test_http_integration.py
import pytest
import requests
from picframe.interface_http import HTTPInterface

@pytest.fixture
def http_server():
    """Start HTTP server for testing."""
    server = HTTPInterface({'port': 8080, 'host': 'localhost'})
    server.start()
    yield server
    server.stop()

def test_http_status_endpoint(http_server):
    """Test HTTP status endpoint."""
    response = requests.get('http://localhost:8080/api/status')
    assert response.status_code == 200
    assert 'current_image' in response.json()
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Import Errors
```bash
# Problem: ModuleNotFoundError: No module named 'picframe'
# Solution: Install in development mode
pip install -e .

# Problem: Import errors in tests
# Solution: Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"
```

#### 2. OpenGL Issues
```bash
# Linux: Install Mesa drivers
sudo apt install libgl1-mesa-dev libgles2-mesa-dev

# macOS: Set compatibility mode
export SYSTEM_VERSION_COMPAT=1

# Windows: Install proper graphics drivers
# Use software rendering if needed:
set MESA_GL_VERSION_OVERRIDE=3.3
```

#### 3. Permission Issues (Raspberry Pi)
```bash
# Add user to required groups
sudo usermod -a -G gpio,spi,i2c,video pi

# Set permissions for GPIO
sudo chmod 666 /dev/gpiomem
```

#### 4. Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .
pip install -r requirements-dev.txt
```

#### 5. Test Failures
```bash
# Clear pytest cache
pytest --cache-clear

# Run tests with more verbose output
pytest -vvv --tb=long

# Run specific failing test
pytest test/unit/test_controller.py::TestController::test_specific_method -vvv
```

### Performance Issues

#### 1. Slow Tests
```bash
# Profile test execution
pytest --durations=10

# Skip slow tests during development
pytest -m "not slow"

# Use parallel execution
pytest -n auto
```

#### 2. Memory Issues
```bash
# Monitor memory usage during tests
pytest --memray

# Use memory profiling
pip install memory-profiler
python -m memory_profiler test_script.py
```

### Development Workflow

#### 1. Daily Development Routine
```bash
# Start development session
cd picframe
source venv/bin/activate

# Pull latest changes
git pull origin main

# Run quick tests
pytest test/unit/ -x

# Start development
# ... make changes ...

# Run affected tests
pytest test/unit/test_modified_module.py

# Format code
black src/ test/
isort src/ test/

# Run linting
flake8 src/ test/

# Run full test suite before committing
pytest

# Commit changes
git add .
git commit -m "Description of changes"
```

#### 2. Pre-commit Checklist
```bash
# Format code
black .
isort .

# Run linting
flake8 .
pylint src/picframe/

# Type checking
mypy src/

# Run tests
pytest --cov=src/picframe

# Check security
bandit -r src/

# Update documentation if needed
# Commit changes
```

This development setup guide provides everything needed to start contributing to PicFrame effectively across different platforms and development scenarios.