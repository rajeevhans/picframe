# Backward Compatibility Guide

This document outlines PicFrame's approach to maintaining backward compatibility and provides guidelines for contributors to ensure changes don't break existing functionality.

## Table of Contents

- [Compatibility Policy](#compatibility-policy)
- [Versioning Strategy](#versioning-strategy)
- [Configuration Compatibility](#configuration-compatibility)
- [API Compatibility](#api-compatibility)
- [Deprecation Process](#deprecation-process)
- [Migration Guides](#migration-guides)
- [Testing Compatibility](#testing-compatibility)

## Compatibility Policy

PicFrame follows semantic versioning (SemVer) and maintains backward compatibility according to these principles:

### Major Version Changes (X.0.0)
- **Breaking changes allowed**
- Configuration format changes
- API signature changes
- Removal of deprecated features
- Minimum Python version updates

### Minor Version Changes (X.Y.0)
- **Backward compatible**
- New features and functionality
- New configuration options (with defaults)
- New API endpoints or methods
- Performance improvements

### Patch Version Changes (X.Y.Z)
- **Backward compatible**
- Bug fixes
- Security fixes
- Documentation updates
- Minor performance improvements

## Versioning Strategy

### Current Support Matrix

| PicFrame Version | Python Support | Status | End of Support |
|------------------|----------------|--------|----------------|
| 2.x.x           | 3.7+          | Active | TBD            |
| 1.x.x           | 3.6+          | Maintenance | 2024-12-31   |

### Deprecation Timeline

Features are deprecated for at least **2 major versions** before removal:

1. **Version N**: Feature marked as deprecated, warnings added
2. **Version N+1**: Deprecation warnings continue
3. **Version N+2**: Feature removed

## Configuration Compatibility

### Configuration File Format

#### Backward Compatible Changes ✅
```yaml
# Adding new optional sections
display:
  width: 1920
  height: 1080
  # New optional setting with default
  brightness: 100  # Default: 100

# Adding new optional parameters
slideshow:
  duration: 10
  fade_time: 1.0
  # New optional parameter
  shuffle: false  # Default: false
```

#### Breaking Changes ❌
```yaml
# Renaming existing sections
display:  # Was: screen
  width: 1920
  height: 1080

# Changing parameter types
slideshow:
  duration: "10s"  # Was: 10 (integer seconds)
```

### Configuration Migration

When breaking changes are necessary, provide migration utilities:

```python
# config_migrator.py
def migrate_config_v1_to_v2(old_config):
    """Migrate configuration from v1 to v2 format."""
    new_config = {}
    
    # Rename sections
    if 'screen' in old_config:
        new_config['display'] = old_config['screen']
    
    # Convert parameter types
    if 'slideshow' in old_config:
        slideshow = old_config['slideshow'].copy()
        if isinstance(slideshow.get('duration'), str):
            # Convert "10s" to 10
            duration_str = slideshow['duration']
            slideshow['duration'] = int(duration_str.rstrip('s'))
        new_config['slideshow'] = slideshow
    
    return new_config
```

### Configuration Validation

```python
def validate_config_compatibility(config, version):
    """Validate configuration compatibility with PicFrame version."""
    warnings = []
    errors = []
    
    # Check for deprecated settings
    if 'old_setting' in config:
        warnings.append(
            "Configuration option 'old_setting' is deprecated. "
            "Use 'new_setting' instead."
        )
    
    # Check for removed settings
    if version >= (2, 0, 0) and 'removed_setting' in config:
        errors.append(
            "Configuration option 'removed_setting' was removed in v2.0.0. "
            "See migration guide for alternatives."
        )
    
    return warnings, errors
```

## API Compatibility

### Public API Guidelines

#### Method Signatures
```python
# ✅ Backward compatible: Adding optional parameters
def load_image(self, path, resize=None, cache=True):
    # New optional parameter 'cache' with default
    pass

# ❌ Breaking change: Changing required parameters
def load_image(self, path, target_size):  # Was: load_image(self, path)
    pass

# ✅ Backward compatible: Adding keyword-only parameters
def load_image(self, path, resize=None, *, cache=True):
    pass
```

#### Return Values
```python
# ✅ Backward compatible: Adding fields to returned dictionaries
def get_status(self):
    return {
        'current_image': 'photo.jpg',
        'slideshow_active': True,
        # New field with clear naming
        'cache_size': 50
    }

# ❌ Breaking change: Changing return type
def get_status(self):
    # Was: dict, now: StatusObject
    return StatusObject(current_image='photo.jpg')
```

### Interface Compatibility

#### MQTT Interface
```python
# Maintain topic structure compatibility
class MQTTInterface:
    def __init__(self, config):
        # Support both old and new topic formats
        self.topic_prefix = config.get('topic_prefix', 'picframe')
        
        # Deprecated topic support
        if 'old_topic_format' in config:
            warnings.warn(
                "old_topic_format is deprecated. Use topic_prefix instead.",
                DeprecationWarning
            )
            self.topic_prefix = self._convert_old_topic_format(
                config['old_topic_format']
            )
```

#### HTTP Interface
```python
# Maintain endpoint compatibility
@app.route('/api/v1/status')  # Keep v1 endpoints
@app.route('/api/status')     # Default to latest
def get_status():
    return jsonify(get_current_status())

# Deprecated endpoints with warnings
@app.route('/status')  # Deprecated endpoint
def get_status_deprecated():
    warnings.warn(
        "Endpoint /status is deprecated. Use /api/status instead.",
        DeprecationWarning
    )
    return redirect('/api/status')
```

## Deprecation Process

### Step 1: Mark as Deprecated
```python
import warnings

def old_function():
    """Deprecated function."""
    warnings.warn(
        "old_function is deprecated and will be removed in v3.0.0. "
        "Use new_function instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return new_function()
```

### Step 2: Update Documentation
```python
def old_function():
    """
    Deprecated function.
    
    .. deprecated:: 2.1.0
        Use :func:`new_function` instead.
        
    This function will be removed in version 3.0.0.
    """
```

### Step 3: Add Migration Path
```python
# Provide clear migration examples
def old_function(*args, **kwargs):
    """
    Deprecated: Use new_function instead.
    
    Migration example:
        # Old way
        result = old_function(param1, param2)
        
        # New way
        result = new_function(param1=param1, param2=param2)
    """
```

### Step 4: Remove in Major Version
```python
# In version 3.0.0, remove the deprecated function entirely
# Document the removal in CHANGELOG.md
```

## Migration Guides

### Configuration Migration Example

#### From v1.x to v2.x
```yaml
# v1.x configuration
screen:
  width: 1920
  height: 1080
  
images:
  directory: "/home/pi/Pictures"
  duration: 10

# v2.x configuration
display:  # Renamed from 'screen'
  width: 1920
  height: 1080
  
slideshow:  # Renamed from 'images'
  image_dir: "/home/pi/Pictures"  # Renamed from 'directory'
  duration: 10
```

#### Migration Script
```python
#!/usr/bin/env python3
"""
PicFrame Configuration Migration Script

Usage: python migrate_config.py old_config.yaml new_config.yaml
"""

import sys
import yaml
from pathlib import Path

def migrate_v1_to_v2(old_config):
    """Migrate v1 configuration to v2 format."""
    new_config = {}
    
    # Migrate screen -> display
    if 'screen' in old_config:
        new_config['display'] = old_config['screen']
        print("✓ Migrated 'screen' section to 'display'")
    
    # Migrate images -> slideshow
    if 'images' in old_config:
        images_config = old_config['images']
        slideshow_config = {}
        
        if 'directory' in images_config:
            slideshow_config['image_dir'] = images_config['directory']
            print("✓ Migrated 'images.directory' to 'slideshow.image_dir'")
        
        if 'duration' in images_config:
            slideshow_config['duration'] = images_config['duration']
            print("✓ Migrated 'images.duration' to 'slideshow.duration'")
        
        new_config['slideshow'] = slideshow_config
    
    return new_config

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python migrate_config.py old_config.yaml new_config.yaml")
        sys.exit(1)
    
    old_path = Path(sys.argv[1])
    new_path = Path(sys.argv[2])
    
    # Load old configuration
    with open(old_path) as f:
        old_config = yaml.safe_load(f)
    
    # Migrate configuration
    new_config = migrate_v1_to_v2(old_config)
    
    # Save new configuration
    with open(new_path, 'w') as f:
        yaml.dump(new_config, f, default_flow_style=False)
    
    print(f"✓ Configuration migrated from {old_path} to {new_path}")
```

## Testing Compatibility

### Compatibility Test Suite
```python
import pytest
import yaml
from picframe.config import load_config
from picframe.compatibility import migrate_config

class TestBackwardCompatibility:
    """Test backward compatibility features."""
    
    def test_v1_config_loading(self):
        """Test that v1 configuration files still work."""
        v1_config = {
            'screen': {'width': 1920, 'height': 1080},
            'images': {'directory': '/photos', 'duration': 10}
        }
        
        # Should load without errors (with warnings)
        with pytest.warns(DeprecationWarning):
            config = load_config(v1_config)
        
        # Should have migrated values
        assert config['display']['width'] == 1920
        assert config['slideshow']['image_dir'] == '/photos'
    
    def test_deprecated_api_warnings(self):
        """Test that deprecated APIs issue warnings."""
        from picframe.controller import Controller
        
        controller = Controller()
        
        with pytest.warns(DeprecationWarning, match="old_method is deprecated"):
            controller.old_method()
    
    @pytest.mark.parametrize("version,should_work", [
        ("1.5.0", True),   # Should work with compatibility layer
        ("2.0.0", True),   # Should work natively
        ("3.0.0", False),  # Should fail (deprecated features removed)
    ])
    def test_version_compatibility(self, version, should_work):
        """Test compatibility across versions."""
        # Test configuration and API compatibility
        pass
```

### Regression Testing
```python
def test_no_regression_in_basic_functionality():
    """Ensure basic functionality hasn't regressed."""
    # Test core features that should always work
    controller = Controller()
    assert controller.get_status() is not None
    
    # Test configuration loading
    config = load_config("test/fixtures/v1_config.yaml")
    assert config is not None
    
    # Test image loading
    cache = ImageCache()
    image = cache.load_image("test/fixtures/sample.jpg")
    assert image is not None
```

## Documentation Standards

### Changelog Format
```markdown
## [2.0.0] - 2024-01-15

### Breaking Changes
- **Configuration**: Renamed `screen` section to `display`
- **API**: Removed deprecated `old_method()` from Controller class

### Migration Guide
- Update configuration files using the migration script: `python migrate_config.py`
- Replace `controller.old_method()` with `controller.new_method()`

### Added
- New `brightness` setting in display configuration
- Support for HEIC image format

### Deprecated
- `images.directory` setting (use `slideshow.image_dir` instead)
- HTTP endpoint `/status` (use `/api/status` instead)

### Fixed
- Memory leak in image cache
- MQTT reconnection issues
```

### API Documentation
```python
def load_image(self, path, resize=None):
    """
    Load an image from the specified path.
    
    Args:
        path (str): Path to the image file
        resize (tuple, optional): Target size as (width, height).
            Added in v1.2.0.
    
    Returns:
        PIL.Image: Loaded image object
    
    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If image format is not supported
    
    .. versionadded:: 1.0.0
    .. versionchanged:: 1.2.0
        Added optional resize parameter
    
    Example:
        >>> cache = ImageCache()
        >>> image = cache.load_image("/path/to/photo.jpg")
        >>> resized = cache.load_image("/path/to/photo.jpg", resize=(800, 600))
    """
```

This backward compatibility guide ensures that PicFrame users can upgrade confidently while maintaining their existing configurations and integrations.