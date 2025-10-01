# Contributing to PicFrame

Thank you for your interest in contributing to PicFrame! This document provides guidelines and standards for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)
- [Documentation Standards](#documentation-standards)
- [Backward Compatibility](#backward-compatibility)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment (see [Development Environment Setup](#development-environment-setup))
4. Create a feature branch for your changes
5. Make your changes following our coding standards
6. Test your changes thoroughly
7. Submit a pull request

## Development Environment Setup

### Prerequisites

- Python 3.7 or higher
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/helgeerbe/picframe.git
   cd picframe
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt  # If available
   ```

4. **Install additional development tools:**
   ```bash
   pip install black flake8 pylint pytest pytest-cov mypy
   ```

5. **Verify installation:**
   ```bash
   python -m picframe.start -v
   ```

### Development Tools

- **Code Formatting:** Black (primary), autopep8 (alternative)
- **Linting:** Flake8, Pylint
- **Type Checking:** MyPy
- **Testing:** Pytest
- **Documentation:** Sphinx (for API docs)

## Coding Standards

### Python Style Guide

PicFrame follows PEP 8 with the following specific guidelines:

#### Line Length
- **Maximum line length:** 120 characters (as configured in tox.ini)
- **Preferred line length:** 88 characters (Black default)

#### Imports
```python
# Standard library imports first
import os
import sys
import logging

# Third-party imports second
import yaml
import numpy as np
from PIL import Image

# Local application imports last
from picframe import model
from picframe.interface_mqtt import MQTTInterface
```

#### Naming Conventions

**Variables and Functions:**
```python
# Use snake_case for variables and functions
image_cache = {}
def get_image_metadata(file_path):
    pass
```

**Classes:**
```python
# Use PascalCase for classes
class ImageProcessor:
    pass

class MQTTInterface:
    pass
```

**Constants:**
```python
# Use UPPER_SNAKE_CASE for constants
DEFAULT_CONFIG_PATH = "~/picframe_data/config/configuration.yaml"
MAX_CACHE_SIZE = 1000
```

**Private Methods and Variables:**
```python
class ImageCache:
    def __init__(self):
        self._cache = {}  # Private instance variable
        
    def _validate_image(self, image_path):  # Private method
        pass
```

#### Documentation Standards

**Module Docstrings:**
```python
"""
Module Name

Brief description of the module's purpose and functionality.

This module provides [detailed description of what the module does].
Key features include:
- Feature 1
- Feature 2
- Feature 3

Dependencies:
    - dependency1: Description
    - dependency2: Description

Author: PicFrame Development Team
License: See LICENSE file in the project root
"""
```

**Class Docstrings:**
```python
class ImageProcessor:
    """
    Handles image processing operations for the PicFrame application.
    
    This class provides methods for loading, transforming, and caching images
    for display in the digital picture frame. It supports various image formats
    and applies transformations like resizing, rotation, and effects.
    
    Attributes:
        cache_size (int): Maximum number of images to keep in cache
        supported_formats (list): List of supported image file extensions
        
    Example:
        processor = ImageProcessor(cache_size=100)
        image = processor.load_image("/path/to/image.jpg")
        processed = processor.apply_effects(image, effects=["blur", "sepia"])
    """
```

**Method Docstrings:**
```python
def load_image(self, file_path, target_size=None):
    """
    Load and optionally resize an image from the specified file path.
    
    This method loads an image file, validates its format, and optionally
    resizes it to the target dimensions while maintaining aspect ratio.
    
    Args:
        file_path (str): Path to the image file to load
        target_size (tuple, optional): Target (width, height) for resizing.
            If None, image is loaded at original size.
            
    Returns:
        PIL.Image: Loaded and processed image object
        
    Raises:
        FileNotFoundError: If the image file doesn't exist
        ValueError: If the image format is not supported
        IOError: If the image file is corrupted or unreadable
        
    Example:
        image = processor.load_image("/photos/vacation.jpg", (1920, 1080))
    """
```

#### Error Handling

**Exception Handling:**
```python
# Use specific exception types
try:
    image = Image.open(file_path)
except FileNotFoundError:
    logger.error(f"Image file not found: {file_path}")
    raise
except IOError as e:
    logger.error(f"Failed to load image {file_path}: {e}")
    raise ValueError(f"Invalid image file: {file_path}")

# Use context managers for resource management
with open(config_file, 'r') as f:
    config = yaml.safe_load(f)
```

**Logging:**
```python
import logging

# Use module-level logger
logger = logging.getLogger(__name__)

# Log levels usage:
logger.debug("Detailed debugging information")
logger.info("General information about program execution")
logger.warning("Something unexpected happened, but program continues")
logger.error("A serious problem occurred")
logger.critical("A very serious error occurred, program may abort")
```

#### Type Hints

Use type hints for all public methods and complex internal methods:

```python
from typing import List, Dict, Optional, Union, Tuple
from pathlib import Path

def process_images(
    image_paths: List[Path], 
    config: Dict[str, Union[str, int]], 
    output_dir: Optional[Path] = None
) -> Tuple[int, List[str]]:
    """Process multiple images according to configuration."""
    pass
```

#### Configuration and Constants

```python
# Group related constants
class DisplayConfig:
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080
    DEFAULT_FPS = 30
    SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

# Use dataclasses for configuration objects
from dataclasses import dataclass

@dataclass
class ImageConfig:
    width: int = 1920
    height: int = 1080
    quality: int = 85
    format: str = 'JPEG'
```

### Code Formatting Configuration

Create or update `.flake8` configuration:
```ini
[flake8]
max-line-length = 120
extend-ignore = E203, W503
exclude = 
    .git,
    __pycache__,
    build,
    dist,
    *.egg-info,
    venv,
    .venv
```

Create `pyproject.toml` section for Black:
```toml
[tool.black]
line-length = 88
target-version = ['py37', 'py38', 'py39', 'py310', 'py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

### Best Practices

#### Code Organization
- Keep functions small and focused (max 50 lines when possible)
- Use meaningful variable and function names
- Avoid deep nesting (max 4 levels)
- Group related functionality into classes or modules
- Separate business logic from presentation logic

#### Performance Considerations
- Use generators for large datasets
- Cache expensive operations appropriately
- Avoid premature optimization
- Profile code before optimizing
- Use appropriate data structures

#### Security Guidelines
- Validate all user inputs
- Use secure defaults for configuration
- Avoid hardcoded credentials
- Sanitize file paths to prevent directory traversal
- Use secure communication protocols (HTTPS, TLS)

## Testing Requirements

### Test Structure
```
test/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for component interactions
├── fixtures/       # Test data and fixtures
└── conftest.py     # Pytest configuration
```

### Writing Tests
```python
import pytest
from unittest.mock import Mock, patch
from picframe.image_cache import ImageCache

class TestImageCache:
    """Test suite for ImageCache class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.cache = ImageCache(max_size=10)
    
    def test_cache_initialization(self):
        """Test that cache initializes with correct parameters."""
        assert self.cache.max_size == 10
        assert len(self.cache) == 0
    
    @patch('picframe.image_cache.Image.open')
    def test_load_image_success(self, mock_open):
        """Test successful image loading."""
        mock_image = Mock()
        mock_open.return_value = mock_image
        
        result = self.cache.load_image("test.jpg")
        
        assert result == mock_image
        mock_open.assert_called_once_with("test.jpg")
```

### Test Coverage
- Aim for 80%+ code coverage
- Focus on critical paths and error conditions
- Test both success and failure scenarios
- Include edge cases and boundary conditions

## Documentation Standards

### Code Comments
```python
# Use comments to explain WHY, not WHAT
def calculate_aspect_ratio(width, height):
    # Avoid division by zero which could crash the display
    if height == 0:
        return 1.0
    return width / height

# Complex algorithms need explanation
def apply_ken_burns_effect(image, zoom_factor, pan_x, pan_y):
    """Apply Ken Burns pan and zoom effect to image."""
    # Ken Burns effect simulates camera movement by gradually
    # zooming and panning across the image over time
    # Formula: new_pos = original_pos * zoom + pan_offset
    pass
```

### README Updates
When adding new features, update relevant documentation:
- README.md for user-facing changes
- API documentation for new interfaces
- Configuration documentation for new options

## Pull Request Process

### Before Submitting
1. **Run all tests:** `pytest`
2. **Check code formatting:** `black --check .`
3. **Run linting:** `flake8 .`
4. **Check type hints:** `mypy src/`
5. **Update documentation** if needed
6. **Test on target platform** (Raspberry Pi if possible)

### Pull Request Template
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Tested on Raspberry Pi (if applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Code is commented appropriately
- [ ] Documentation updated
- [ ] No new warnings introduced
```

### Review Criteria
- Code quality and adherence to standards
- Test coverage and quality
- Documentation completeness
- Backward compatibility
- Performance impact
- Security considerations

## Backward Compatibility

### Guidelines
- **Configuration:** New configuration options should have sensible defaults
- **API:** Existing public APIs should remain functional
- **Dependencies:** Avoid breaking dependency changes
- **File Formats:** Maintain support for existing file formats

### Deprecation Process
1. **Mark as deprecated** with clear migration path
2. **Add deprecation warnings** in code
3. **Update documentation** with migration guide
4. **Remove after 2 major versions** minimum

### Version Compatibility
- Support Python 3.7+ as specified in pyproject.toml
- Test against multiple Python versions
- Document any version-specific features

## Getting Help

- **Issues:** Use GitHub Issues for bug reports and feature requests
- **Discussions:** Use GitHub Discussions for questions and ideas
- **Documentation:** Check existing documentation first
- **Code Review:** Request reviews from maintainers

Thank you for contributing to PicFrame!