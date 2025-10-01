# PicFrame Configuration Reference

This comprehensive guide documents all configuration options available in PicFrame, including examples, valid value ranges, and configuration templates for common use cases.

## Table of Contents

- [Configuration File Structure](#configuration-file-structure)
- [Viewer Configuration](#viewer-configuration)
- [Model Configuration](#model-configuration)
- [MQTT Configuration](#mqtt-configuration)
- [HTTP Configuration](#http-configuration)
- [Peripherals Configuration](#peripherals-configuration)
- [Configuration Templates](#configuration-templates)
- [Migration Guide](#migration-guide)
- [Validation and Troubleshooting](#validation-and-troubleshooting)

## Configuration File Structure

PicFrame uses YAML format for configuration. The main configuration file is located at:
```
~/picframe_data/config/configuration.yaml
```

The configuration is organized into five main sections:
- `viewer`: Display and visual settings
- `model`: Image management and data handling
- `mqtt`: MQTT integration settings
- `http`: HTTP server settings
- `peripherals`: Input device configuration

### Basic Configuration Template

```yaml
viewer:
  # Display settings
  
model:
  # Image and data management
  
mqtt:
  # MQTT integration (optional)
  
http:
  # HTTP server (optional)
  
peripherals:
  # Input devices (optional)
```

## Viewer Configuration

The `viewer` section controls all display-related settings, visual effects, and rendering options.

### Display Settings

#### Basic Display Configuration
```yaml
viewer:
  # Display dimensions and positioning
  display_x: 0                    # Horizontal offset from screen edge (pixels)
  display_y: 0                    # Vertical offset from screen edge (pixels)
  display_w: null                 # Display width (null = auto-detect)
  display_h: null                 # Display height (null = auto-detect)
  
  # Display power management
  display_power: 2                # Power control method
                                  # 0: vcgencmd (legacy)
                                  # 1: xset (X11 systems)
                                  # 2: wlr-randr (Wayland)
```

**Valid Ranges:**
- `display_x`, `display_y`: Any integer (can be negative)
- `display_w`, `display_h`: Positive integers or `null`
- `display_power`: 0, 1, or 2

#### Graphics Backend Settings
```yaml
viewer:
  use_glx: False                  # Use GLX on X11 systems
  use_sdl2: True                  # Use SDL2 backend (recommended)
  fps: 20.0                       # Target frames per second
```

**Valid Ranges:**
- `use_glx`, `use_sdl2`: `True` or `False`
- `fps`: 1.0 to 60.0 (float)

### Image Display and Effects

#### Image Fitting and Scaling
```yaml
viewer:
  fit: False                      # Image fitting behavior
                                  # True: Scale to fit (may show gaps)
                                  # False: Crop to fill (no gaps)
  
  kenburns: False                 # Enable Ken Burns effect
                                  # Automatically sets fit=False, blur_edges=False
  
  video_fit_display: False        # Video scaling behavior
                                  # True: Scale to display (may distort)
                                  # False: Scale maintaining aspect ratio
```

#### Background and Edge Handling
```yaml
viewer:
  background: [0.2, 0.2, 0.3, 1.0]  # RGBA background color
  blur_edges: False               # Use blurred image for edges
  blur_amount: 12                 # Blur intensity for backgrounds
  blur_zoom: 1.0                  # Background zoom factor (>=1.0)
  edge_alpha: 0.5                 # Edge transparency (0.0-1.0)
```

**Valid Ranges:**
- `background`: Array of 4 floats [R, G, B, A] (0.0-1.0 each)
- `blur_amount`: 1 to 50 (higher values increase processing load)
- `blur_zoom`: 1.0 to 3.0
- `edge_alpha`: 0.0 to 1.0

#### Blend Effects
```yaml
viewer:
  blend_type: "blend"             # Transition effect type
                                  # Options: "blend", "burn", "bump"
```

### Text Overlays

#### Image Information Display
```yaml
viewer:
  show_text: "title caption name date folder location"  # Text elements to show
  show_text_fm: "%b %d, %Y"       # Date format string
  show_text_tm: 20.0              # Text display duration (seconds)
  show_text_sz: 40                # Text size (pixels)
  text_justify: "L"               # Text alignment: "L", "C", "R"
  text_bkg_hgt: 0.25              # Background height (0.0-1.0)
  text_opacity: 1.0               # Text opacity (0.0-1.0)
```

**Text Elements Available:**
- `title`: Image title from metadata
- `caption`: Image caption/description
- `name`: Filename
- `date`: Date taken or modified
- `folder`: Directory name
- `location`: GPS location (if available)

**Valid Ranges:**
- `show_text_tm`: 0.0 to 300.0 seconds
- `show_text_sz`: 10 to 200 pixels
- `text_bkg_hgt`: 0.0 to 1.0
- `text_opacity`: 0.0 to 1.0

#### Clock Display
```yaml
viewer:
  show_clock: False               # Enable clock overlay
  clock_justify: "R"              # Clock position: "L", "C", "R"
  clock_text_sz: 120              # Clock text size
  clock_format: "%-I:%M"          # Time format (strftime)
  clock_opacity: 1.0              # Clock transparency
  clock_top_bottom: "T"           # Position: "T" (top), "B" (bottom)
  clock_wdt_offset_pct: 3.0       # Horizontal offset percentage
  clock_hgt_offset_pct: 3.0       # Vertical offset percentage
```

**Common Clock Formats:**
- `"%-I:%M"`: 12-hour format without leading zero (3:45)
- `"%H:%M"`: 24-hour format (15:45)
- `"%-I:%M %p"`: 12-hour with AM/PM (3:45 PM)
- `"%A, %B %-d"`: Full day and date (Monday, January 15)

### Image Matting

#### Automatic Matting
```yaml
viewer:
  mat_images: 0.01                # Auto-mat threshold
                                  # False: No auto-matting
                                  # True: Mat all images
                                  # Float: Mat if aspect ratio difference > value
  
  mat_type: null                  # Mat styles to use (null = all)
                                  # Options: "float float_polaroid float_color_wrap 
                                  #          single_bevel double_bevel double_flat"
```

#### Mat Appearance
```yaml
viewer:
  outer_mat_color: null           # RGB color [R, G, B] or null (auto)
  inner_mat_color: null           # RGB color [R, G, B] or null (auto)
  outer_mat_border: 75            # Outer border width (pixels)
  inner_mat_border: 40            # Inner border width (pixels)
  outer_mat_use_texture: True     # Use texture for outer mat
  inner_mat_use_texture: False    # Use texture for inner mat
  mat_resource_folder: "~/picframe_data/data/mat"  # Mat texture location
```

### Menu System
```yaml
viewer:
  menu_text_sz: 40                # Menu text size
  menu_autohide_tm: 10.0          # Auto-hide timeout (0 = disabled)
```

### Font and Shader Configuration
```yaml
viewer:
  font_file: "~/picframe_data/data/fonts/NotoSans-Regular.ttf"
  shader: "~/picframe_data/data/shaders/blend_new"
```

### Geographic Display
```yaml
viewer:
  geo_suppress_list: []           # Substrings to remove from location text
                                  # Example: ["Street", "Road", "Avenue"]
```

## Model Configuration

The `model` section handles image management, database operations, and file processing.

### Directory Configuration
```yaml
model:
  pic_dir: "~/Pictures"           # Root directory for images
  deleted_pictures: "~/DeletedPictures"  # Deleted images destination
  subdirectory: ""                # Subdirectory within pic_dir
  follow_links: False             # Follow symbolic links
```

### Image Selection and Timing
```yaml
model:
  time_delay: 200.0               # Seconds between image changes
  fade_time: 10.0                 # Transition duration (seconds)
  shuffle: True                   # Randomize image order
  reshuffle_num: 1                # Times through before reshuffling
  recent_n: 7                     # Days to prioritize recent images
```

**Valid Ranges:**
- `time_delay`: 1.0 to 3600.0 seconds
- `fade_time`: 0.1 to 60.0 seconds
- `recent_n`: 0 to 365 days

### Database and Caching
```yaml
model:
  db_file: "~/picframe_data/data/pictureframe.db3"  # Database location
  update_interval: 2.0            # File scan interval (seconds)
  sort_cols: 'fname ASC'          # Database sort order
```

**Available Sort Columns:**
- `fname`: Filename
- `last_modified`: File modification date
- `file_id`: Database ID
- `orientation`: Image orientation
- `exif_datetime`: EXIF date/time
- `f_number`: Camera f-number
- `exposure_time`: Exposure time
- `iso`: ISO setting
- `focal_length`: Lens focal length
- `make`, `model`: Camera make/model
- `lens`: Lens information
- `rating`: Image rating
- `latitude`, `longitude`: GPS coordinates
- `width`, `height`: Image dimensions
- `title`, `caption`: Metadata text
- `tags`: IPTC keywords
- `location`: Geographic location

### Filtering Options
```yaml
model:
  location_filter: ""             # SQL WHERE clause for location
  tags_filter: ""                 # SQL WHERE clause for tags
```

**Filter Examples:**
```yaml
# Show only images from specific locations
location_filter: "location LIKE '%Paris%' OR location LIKE '%London%'"

# Filter by IPTC tags
tags_filter: "tags LIKE '%vacation%' OR tags LIKE '%family%'"

# Date range filtering
location_filter: "exif_datetime > '2023-01-01'"
```

### Metadata Configuration
```yaml
model:
  image_attr: [                   # Metadata attributes for MQTT
    "PICFRAME GPS",
    "PICFRAME LOCATION",
    "EXIF FNumber",
    "EXIF ExposureTime",
    "EXIF ISOSpeedRatings",
    "EXIF FocalLength",
    "EXIF DateTimeOriginal",
    "Image Model",
    "Image Make",
    "IPTC Caption/Abstract",
    "IPTC Object Name",
    "IPTC Keywords"
  ]
```

### Geolocation Services
```yaml
model:
  load_geoloc: False              # Enable reverse geocoding
  geo_key: "your_email@domain.com"  # Unique identifier for API
  locale: "en_US.utf8"            # System locale
  key_list: [                     # Location hierarchy
    ["tourism","amenity","isolated_dwelling"],
    ["suburb","village"],
    ["city","county"],
    ["region","state","province"],
    ["country"]
  ]
```

### Portrait Pairing and Logging
```yaml
model:
  portrait_pairs: False           # Pair portrait images
  no_files_img: "~/picframe_data/data/no_pictures.jpg"  # Default image
  log_level: "WARNING"            # Logging level
  log_file: ""                    # Log file path (empty = console)
```

**Log Levels:**
- `DEBUG`: Detailed debugging information
- `INFO`: General information
- `WARNING`: Warning messages (default)
- `ERROR`: Error messages only
- `CRITICAL`: Critical errors only

## MQTT Configuration

MQTT enables smart home integration and remote control capabilities.

### Basic MQTT Settings
```yaml
mqtt:
  use_mqtt: False                 # Enable MQTT integration
  server: "your_mqtt_broker"      # MQTT broker hostname/IP
  port: 8883                      # MQTT port (8883 for TLS, 1883 for plain)
  login: "username"               # MQTT username
  password: "password"            # MQTT password
```

### Security Configuration
```yaml
mqtt:
  tls: "/path/to/ca.crt"          # TLS certificate file
                                  # Use "" for no TLS (port should be 1883)
```

### Device Configuration
```yaml
mqtt:
  device_id: "picframe"           # Unique device identifier
  device_url: ""                  # URL to PicFrame web interface
                                  # Must be valid URL or empty string
```

**MQTT Topics Structure:**
PicFrame automatically creates the following topic structure:
```
homeassistant/
├── switch/picframe_[device_id]/
├── sensor/picframe_[device_id]/
└── camera/picframe_[device_id]/
```

### Home Assistant Integration
When `use_mqtt: True`, PicFrame automatically:
1. Publishes device discovery information
2. Creates entities for remote control
3. Sends image metadata and status updates
4. Responds to commands (next, previous, pause, etc.)

## HTTP Configuration

The HTTP interface provides web-based control and configuration.

### Basic HTTP Settings
```yaml
http:
  use_http: False                 # Enable HTTP server
  port: 9000                      # HTTP port (>1024 recommended)
  path: "~/picframe_data/html"    # Web files location
```

### Authentication
```yaml
http:
  auth: false                     # Enable basic authentication
  username: admin                 # Username for basic auth
  password: null                  # Password (null = auto-generate)
```

When `password: null`, PicFrame generates a random password and saves it to `basic_auth.txt` in the HTTP directory.

### SSL/TLS Configuration
```yaml
http:
  use_ssl: False                  # Enable HTTPS
  keyfile: "path/to/key.pem"      # Private key file
  certfile: "path/to/cert.pem"    # Certificate file
```

**Security Note:** The HTTP server is designed for local network use only and should not be exposed to external access without proper security measures.

## Peripherals Configuration

Configure input devices for local control of PicFrame.

### Input Device Selection
```yaml
peripherals:
  input_type: null                # Input device type
                                  # Options: null, "keyboard", "touch", "mouse"
```

### Button Configuration
```yaml
peripherals:
  buttons:
    pause:                        # Pause/unpause slideshow
      enable: True
      label: "Pause"
      shortcut: " "               # Spacebar
    
    display_off:                  # Turn off display
      enable: True
      label: "Display off"
      shortcut: "o"
    
    location:                     # Toggle location display
      enable: False
      label: "Location"
      shortcut: "l"
    
    exit:                         # Exit PicFrame
      enable: False
      label: "Exit"
      shortcut: "e"
    
    power_down:                   # System shutdown
      enable: False
      label: "Power down"
      shortcut: "p"
```

**Button Actions:**
- `pause`: Toggle slideshow pause/resume
- `display_off`: Turn display off (any input turns it back on)
- `location`: Show/hide location information overlay
- `exit`: Gracefully exit PicFrame
- `power_down`: Execute system shutdown (requires sudo privileges)

## Configuration Templates

### Basic Digital Picture Frame
```yaml
viewer:
  time_delay: 300.0               # 5 minutes per image
  fade_time: 5.0                  # 5-second transitions
  fit: False                      # Fill screen completely
  show_text: "date location"      # Show minimal info
  show_text_tm: 10.0              # Show for 10 seconds
  show_clock: True                # Display clock
  clock_justify: "R"              # Clock in top-right

model:
  pic_dir: "~/Pictures"
  shuffle: True
  recent_n: 30                    # Prioritize last 30 days

mqtt:
  use_mqtt: False

http:
  use_http: False

peripherals:
  input_type: "keyboard"
  buttons:
    pause:
      enable: True
    display_off:
      enable: True
```

### Smart Home Integrated Frame
```yaml
viewer:
  time_delay: 180.0               # 3 minutes per image
  show_text: "title date location"
  show_clock: True
  mat_images: 0.02                # Auto-mat different aspect ratios

model:
  pic_dir: "~/Pictures"
  load_geoloc: True               # Enable location lookup
  geo_key: "your_email@domain.com"
  shuffle: True

mqtt:
  use_mqtt: True
  server: "homeassistant.local"
  port: 1883
  login: "picframe_user"
  password: "secure_password"
  device_id: "living_room_frame"
  tls: ""                         # No TLS for local network

http:
  use_http: True
  port: 9000
  auth: true
  username: "admin"

peripherals:
  input_type: "touch"
```

### High-Performance Display
```yaml
viewer:
  fps: 30.0                       # Smooth animations
  blur_amount: 8                  # Reduce processing load
  kenburns: True                  # Ken Burns effect
  time_delay: 120.0               # 2 minutes per image
  fade_time: 3.0                  # Quick transitions
  
model:
  pic_dir: "/media/photos"        # High-speed storage
  update_interval: 5.0            # Less frequent scanning
  
# Minimal integrations for performance
mqtt:
  use_mqtt: False
http:
  use_http: False
```

### Family Photo Frame
```yaml
viewer:
  show_text: "title caption date location"
  show_text_tm: 15.0              # Show info longer
  text_justify: "C"               # Center text
  show_clock: True
  clock_format: "%A, %B %-d"      # Show full date
  mat_images: True                # Mat all images
  mat_type: "float double_bevel"  # Family-friendly mat styles

model:
  pic_dir: "~/Family_Photos"
  tags_filter: "tags LIKE '%family%' OR tags LIKE '%vacation%'"
  recent_n: 14                    # Prioritize last 2 weeks
  portrait_pairs: True            # Pair portrait images

peripherals:
  input_type: "touch"
  buttons:
    pause:
      enable: True
    location:
      enable: True
```

## Migration Guide

### Upgrading Configuration Files

When upgrading PicFrame, configuration files may need updates for new features or changed defaults.

#### Version Compatibility Check
```bash
# Check your current configuration
picframe -v

# Backup current configuration
cp ~/picframe_data/config/configuration.yaml ~/picframe_data/config/configuration.yaml.backup

# Compare with new example
diff ~/picframe_data/config/configuration.yaml ~/picframe_data/config/configuration_example.yaml
```

#### Common Migration Tasks

**From v1.x to v2.x:**
1. **Display Power Management**: Update `display_power` values
   ```yaml
   # Old format
   display_power: True
   
   # New format
   display_power: 2  # Use wlr-randr
   ```

2. **MQTT Port Configuration**: Explicit TLS configuration
   ```yaml
   # Old format
   mqtt:
     port: 8883
   
   # New format
   mqtt:
     port: 8883
     tls: "/path/to/ca.crt"  # or "" for no TLS
   ```

3. **HTTP Authentication**: Enhanced security options
   ```yaml
   # Old format
   http:
     use_auth: True
   
   # New format
   http:
     auth: true
     username: admin
     password: null  # Auto-generate
   ```

#### Automated Migration Script
```bash
#!/bin/bash
# migration_helper.sh

CONFIG_FILE="$HOME/picframe_data/config/configuration.yaml"
BACKUP_FILE="$CONFIG_FILE.backup.$(date +%Y%m%d)"

# Create backup
cp "$CONFIG_FILE" "$BACKUP_FILE"
echo "Backup created: $BACKUP_FILE"

# Update deprecated settings
sed -i 's/display_power: True/display_power: 2/' "$CONFIG_FILE"
sed -i 's/display_power: False/display_power: 0/' "$CONFIG_FILE"

echo "Migration completed. Please review your configuration."
```

### Configuration Validation

#### Syntax Validation
```bash
# Check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('~/picframe_data/config/configuration.yaml'))"
```

#### Semantic Validation
```bash
# Test configuration loading
python3 -c "
from picframe import model
try:
    m = model.Model('~/picframe_data/config/configuration.yaml')
    print('Configuration is valid')
except Exception as e:
    print(f'Configuration error: {e}')
"
```

## Validation and Troubleshooting

### Configuration Validation

#### Required Settings Check
Ensure these critical settings are properly configured:

1. **Picture Directory Exists**:
   ```bash
   ls -la ~/Pictures  # or your configured pic_dir
   ```

2. **Database Directory Writable**:
   ```bash
   touch ~/picframe_data/data/test.tmp && rm ~/picframe_data/data/test.tmp
   ```

3. **Font Files Available**:
   ```bash
   ls -la ~/picframe_data/data/fonts/
   ```

#### Common Configuration Errors

**Invalid YAML Syntax:**
```yaml
# Wrong - missing quotes around time format
show_text_fm: %b %d, %Y

# Correct
show_text_fm: "%b %d, %Y"
```

**Invalid Color Values:**
```yaml
# Wrong - values outside 0.0-1.0 range
background: [255, 255, 255, 1.0]

# Correct
background: [1.0, 1.0, 1.0, 1.0]
```

**Path Issues:**
```yaml
# Wrong - path doesn't exist
pic_dir: "/nonexistent/directory"

# Correct - use expandable paths
pic_dir: "~/Pictures"
```

### Performance Tuning

#### For Low-End Hardware:
```yaml
viewer:
  fps: 15.0                       # Reduce frame rate
  blur_amount: 6                  # Less blur processing
  fit: True                       # Avoid cropping calculations
  
model:
  update_interval: 10.0           # Less frequent file scanning
```

#### For High-End Hardware:
```yaml
viewer:
  fps: 30.0                       # Smooth animations
  blur_amount: 20                 # High-quality blur
  kenburns: True                  # Enable Ken Burns effect
  
model:
  update_interval: 1.0            # Frequent updates
```

### Debugging Configuration Issues

#### Enable Debug Logging:
```yaml
model:
  log_level: "DEBUG"
  log_file: "/tmp/picframe_debug.log"
```

#### Test Individual Components:
```bash
# Test MQTT connection
python3 -c "
from picframe import interface_mqtt
# Test connection with your settings
"

# Test HTTP server
curl http://localhost:9000  # Replace with your port
```

#### Monitor Resource Usage:
```bash
# Monitor while PicFrame is running
htop
iotop  # For disk I/O
```

For additional help with configuration issues, consult the [Troubleshooting Guide](troubleshooting.md) or visit the [PicFrame GitHub repository](https://github.com/helgeerbe/picframe).