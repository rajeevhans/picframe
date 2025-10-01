# Testing Guide for PicFrame

This document provides comprehensive guidelines for testing PicFrame contributions, including unit tests, integration tests, and manual testing procedures.

## Table of Contents

- [Testing Philosophy](#testing-philosophy)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Writing Tests](#writing-tests)
- [Test Coverage](#test-coverage)
- [Manual Testing](#manual-testing)
- [Platform-Specific Testing](#platform-specific-testing)
- [Performance Testing](#performance-testing)
- [Security Testing](#security-testing)

## Testing Philosophy

PicFrame follows a comprehensive testing approach that includes:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions and external interfaces
- **Manual Tests**: Verify functionality on actual hardware
- **Performance Tests**: Ensure acceptable performance characteristics
- **Security Tests**: Validate security measures and input handling

## Test Structure

```
test/
├── unit/                   # Unit tests for individual components
│   ├── test_controller.py
│   ├── test_model.py
│   ├── test_image_cache.py
│   └── test_interfaces/
│       ├── test_mqtt.py
│       ├── test_http.py
│       └── test_peripherals.py
├── integration/            # Integration tests
│   ├── test_mqtt_integration.py
│   ├── test_http_integration.py
│   └── test_display_pipeline.py
├── fixtures/               # Test data and fixtures
│   ├── images/
│   ├── configs/
│   └── mock_data/
├── performance/            # Performance tests
│   ├── test_image_processing.py
│   └── test_cache_performance.py
├── conftest.py            # Pytest configuration and fixtures
└── requirements-test.txt   # Test-specific dependencies
```

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install -r requirements-dev.txt
```

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/picframe --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Skip slow tests

# Run specific test files
pytest test/unit/test_controller.py
pytest test/integration/test_mqtt_integration.py

# Run with verbose output
pytest -v

# Run tests in parallel (if pytest-xdist installed)
pytest -n auto
```

### Continuous Integration

```bash
# Full CI test suite
pytest --cov=src/picframe --cov-report=xml --cov-report=term-missing
```

## Writing Tests

### Unit Test Example

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from picframe.image_cache import ImageCache
from picframe.exceptions import ImageLoadError

class TestImageCache:
    """Test suite for ImageCache class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.cache = ImageCache(max_size=10, cache_dir="/tmp/test_cache")
    
    def teardown_method(self):
        """Clean up after each test method."""
        self.cache.clear()
    
    def test_cache_initialization(self):
        """Test that cache initializes with correct parameters."""
        assert self.cache.max_size == 10
        assert self.cache.cache_dir == "/tmp/test_cache"
        assert len(self.cache) == 0
    
    @patch('picframe.image_cache.Image.open')
    def test_load_image_success(self, mock_open):
        """Test successful image loading and caching."""
        # Arrange
        mock_image = Mock()
        mock_image.size = (1920, 1080)
        mock_open.return_value = mock_image
        
        # Act
        result = self.cache.load_image("test.jpg")
        
        # Assert
        assert result == mock_image
        mock_open.assert_called_once_with("test.jpg")
        assert "test.jpg" in self.cache
    
    @patch('picframe.image_cache.Image.open')
    def test_load_image_file_not_found(self, mock_open):
        """Test handling of missing image files."""
        # Arrange
        mock_open.side_effect = FileNotFoundError("File not found")
        
        # Act & Assert
        with pytest.raises(ImageLoadError, match="File not found"):
            self.cache.load_image("missing.jpg")
    
    @pytest.mark.parametrize("file_path,expected_key", [
        ("/path/to/image.jpg", "image.jpg"),
        ("../images/photo.png", "photo.png"),
        ("image with spaces.jpeg", "image with spaces.jpeg"),
    ])
    def test_cache_key_generation(self, file_path, expected_key):
        """Test cache key generation from file paths."""
        key = self.cache._generate_cache_key(file_path)
        assert key == expected_key
```

### Integration Test Example

```python
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from picframe.interface_mqtt import MQTTInterface
from picframe.controller import Controller

class TestMQTTIntegration:
    """Integration tests for MQTT interface."""
    
    @pytest.fixture
    def mqtt_config(self):
        """MQTT configuration fixture."""
        return {
            'broker': 'localhost',
            'port': 1883,
            'username': 'test_user',
            'password': 'test_pass',
            'topic_prefix': 'picframe/test'
        }
    
    @pytest.fixture
    def controller_mock(self):
        """Mock controller for testing."""
        controller = Mock(spec=Controller)
        controller.next_image = Mock()
        controller.previous_image = Mock()
        controller.pause_slideshow = Mock()
        return controller
    
    @pytest.mark.asyncio
    async def test_mqtt_command_processing(self, mqtt_config, controller_mock):
        """Test MQTT command processing integration."""
        # Arrange
        mqtt_interface = MQTTInterface(mqtt_config, controller_mock)
        
        with patch('paho.mqtt.client.Client') as mock_client:
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance
            
            # Act
            await mqtt_interface.start()
            
            # Simulate receiving a command
            message = Mock()
            message.topic = 'picframe/test/command'
            message.payload = b'next'
            
            mqtt_interface._on_message(mock_client_instance, None, message)
            
            # Assert
            controller_mock.next_image.assert_called_once()
```

### Test Fixtures

```python
# conftest.py
import pytest
import tempfile
import shutil
from pathlib import Path
from PIL import Image

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)

@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    image = Image.new('RGB', (100, 100), color='red')
    return image

@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        'display': {
            'width': 1920,
            'height': 1080,
            'fps': 30
        },
        'slideshow': {
            'duration': 10,
            'fade_time': 1.0
        },
        'mqtt': {
            'broker': 'localhost',
            'port': 1883
        }
    }

@pytest.fixture(scope="session")
def test_images_dir():
    """Directory containing test images."""
    return Path(__file__).parent / "fixtures" / "images"
```

## Test Coverage

### Coverage Requirements

- **Minimum Coverage**: 80% overall
- **Critical Components**: 90%+ coverage
- **New Features**: 95%+ coverage
- **Bug Fixes**: Must include tests that reproduce the bug

### Coverage Analysis

```bash
# Generate coverage report
pytest --cov=src/picframe --cov-report=html --cov-report=term-missing

# View HTML report
open htmlcov/index.html

# Check coverage for specific modules
pytest --cov=src/picframe.controller --cov-report=term-missing
```

### Coverage Configuration

Coverage settings in `pyproject.toml`:
```toml
[tool.coverage.run]
source = ["src/picframe"]
omit = [
    "*/tests/*",
    "*/test_*",
    "src/picframe/_version.py",
    "*/venv/*",
    "*/.venv/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:"
]
```

## Manual Testing

### Development Environment Testing

1. **Basic Functionality**
   ```bash
   # Test application startup
   python -m picframe.start -v
   
   # Test with sample configuration
   python -m picframe.start test/fixtures/configs/test_config.yaml
   ```

2. **Interface Testing**
   - MQTT: Use MQTT client to send commands
   - HTTP: Test web interface endpoints
   - Peripherals: Test button/touch inputs

3. **Image Processing**
   - Test various image formats (JPEG, PNG, HEIC)
   - Test different image sizes and aspect ratios
   - Verify EXIF data processing

### Raspberry Pi Testing

1. **Hardware Setup**
   - Test on actual Raspberry Pi hardware
   - Verify display output on connected screen
   - Test peripheral inputs (buttons, touch)

2. **Performance Testing**
   - Monitor CPU and memory usage
   - Test with large image collections
   - Verify smooth slideshow transitions

3. **Integration Testing**
   - Test Home Assistant integration
   - Verify MQTT broker connectivity
   - Test network connectivity handling

## Platform-Specific Testing

### Raspberry Pi OS
```bash
# Test on Raspberry Pi OS
python -m pytest test/ -m "not slow" --tb=short

# Test with hardware-specific features
python -m pytest test/integration/test_display_hardware.py
```

### Development Platforms
```bash
# Test on macOS/Linux/Windows
python -m pytest test/unit/ -v

# Test cross-platform compatibility
python -m pytest test/integration/test_cross_platform.py
```

## Performance Testing

### Image Processing Performance
```python
import time
import pytest
from picframe.image_cache import ImageCache

def test_image_loading_performance():
    """Test image loading performance."""
    cache = ImageCache(max_size=100)
    
    start_time = time.time()
    for i in range(10):
        cache.load_image(f"test/fixtures/images/sample_{i}.jpg")
    end_time = time.time()
    
    # Should load 10 images in less than 5 seconds
    assert (end_time - start_time) < 5.0

@pytest.mark.slow
def test_large_collection_performance():
    """Test performance with large image collections."""
    # Test with 1000+ images
    pass
```

### Memory Usage Testing
```python
import psutil
import pytest

def test_memory_usage():
    """Test memory usage stays within acceptable limits."""
    process = psutil.Process()
    initial_memory = process.memory_info().rss
    
    # Perform memory-intensive operations
    cache = ImageCache(max_size=50)
    for i in range(100):
        cache.load_image(f"test/fixtures/images/large_image_{i}.jpg")
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Memory increase should be less than 500MB
    assert memory_increase < 500 * 1024 * 1024
```

## Security Testing

### Input Validation Testing
```python
def test_file_path_validation():
    """Test file path validation prevents directory traversal."""
    cache = ImageCache()
    
    # Test directory traversal attempts
    malicious_paths = [
        "../../../etc/passwd",
        "..\\..\\windows\\system32\\config\\sam",
        "/etc/shadow",
        "C:\\Windows\\System32\\config\\SAM"
    ]
    
    for path in malicious_paths:
        with pytest.raises(ValueError, match="Invalid file path"):
            cache.load_image(path)
```

### Authentication Testing
```python
def test_http_authentication():
    """Test HTTP interface authentication."""
    from picframe.interface_http import HTTPInterface
    
    # Test with invalid credentials
    response = client.get('/api/status', auth=('wrong', 'credentials'))
    assert response.status_code == 401
    
    # Test with valid credentials
    response = client.get('/api/status', auth=('admin', 'correct_password'))
    assert response.status_code == 200
```

## Test Data Management

### Test Image Creation
```python
# Create test images programmatically
from PIL import Image, ImageDraw

def create_test_image(width, height, color='red', text=None):
    """Create a test image with specified properties."""
    image = Image.new('RGB', (width, height), color=color)
    
    if text:
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), text, fill='white')
    
    return image

# Save test images
test_image = create_test_image(1920, 1080, 'blue', 'Test Image')
test_image.save('test/fixtures/images/test_1920x1080.jpg')
```

### Configuration Templates
```yaml
# test/fixtures/configs/minimal_config.yaml
display:
  width: 800
  height: 600
  
slideshow:
  duration: 5
  
image_dir: "test/fixtures/images"
```

## Continuous Integration

### GitHub Actions Example
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8, 3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
        pip install -e .
    
    - name: Run tests
      run: |
        pytest --cov=src/picframe --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Troubleshooting Tests

### Common Issues

1. **Import Errors**
   - Ensure PicFrame is installed in development mode: `pip install -e .`
   - Check PYTHONPATH includes src directory

2. **Missing Dependencies**
   - Install test dependencies: `pip install -r requirements-dev.txt`
   - Check for platform-specific dependencies

3. **Test Data Issues**
   - Ensure test fixtures are present
   - Check file permissions on test data

4. **Hardware-Specific Failures**
   - Use appropriate test markers to skip hardware tests
   - Mock hardware interfaces for unit tests

### Debug Mode
```bash
# Run tests with debug output
pytest -v -s --tb=long

# Run specific test with debugging
pytest -v -s test/unit/test_controller.py::TestController::test_specific_method

# Use pdb for interactive debugging
pytest --pdb test/unit/test_controller.py
```

This testing guide ensures comprehensive coverage of PicFrame functionality while maintaining code quality and reliability across different platforms and use cases.