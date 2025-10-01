# PicFrame API Reference

This document provides comprehensive API reference documentation for the PicFrame digital picture frame application. The API is organized into core modules that implement the MVC (Model-View-Controller) architecture pattern.

## Table of Contents

- [Core Application Modules](#core-application-modules)
  - [start.py - Application Entry Point](#startpy---application-entry-point)
  - [controller.py - Application Controller](#controllerpy---application-controller)
  - [model.py - Business Logic and Data Management](#modelpy---business-logic-and-data-management)
- [Interface Modules](#interface-modules)
  - [interface_mqtt.py - MQTT Communication](#interface_mqttpy---mqtt-communication)
  - [interface_http.py - HTTP Web Interface](#interface_httppy---http-web-interface)
  - [interface_peripherals.py - Direct Input Control](#interface_peripheralspy---direct-input-control)
- [Utility Modules](#utility-modules)
  - [viewer_display.py - Display Rendering](#viewer_displaypy---display-rendering)
  - [image_cache.py - Image Database Management](#image_cachepy---image-database-management)
  - [get_image_meta.py - Metadata Extraction](#get_image_metapy---metadata-extraction)

---

## Core Application Modules

### start.py - Application Entry Point

The main entry point for the PicFrame application, handling initialization, configuration setup, and application lifecycle management.

#### Functions

##### `copy_files(pkgdir: str, dest: str, target: str) -> None`

Copy resource files from the package directory to the destination directory.

**Parameters:**
- `pkgdir` (str): Source package directory path containing the resource files
- `dest` (str): Destination directory where files should be copied
- `target` (str): Specific subdirectory to copy (e.g., 'html', 'config', 'data')

**Raises:**
- `Exception`: Re-raises any exception that occurs during the copy operation

**Example:**
```python
copy_files('/usr/local/lib/python3.x/site-packages/picframe', 
          '/home/user', 'config')
# Creates: /home/user/picframe_data/config/
```

##### `create_config(root: str) -> None`

Create a personalized configuration file from the example template through interactive prompts.

**Parameters:**
- `root` (str): Root directory where the picframe_data structure exists

**Configuration Parameters Prompted:**
- Picture directory: Where images are stored (default: ~/Pictures)
- Deleted pictures directory: Where deleted images are moved (default: ~/DeletedPictures)
- Locale: System locale for date/time formatting (auto-detected)

**Files Created:**
- `{root}/picframe_data/config/configuration.yaml`: Main configuration file
- `{root}/picframe_data/run_start.py`: Execution wrapper script

##### `check_packages(packages: List[str]) -> None`

Verify the availability and versions of required Python packages.

**Parameters:**
- `packages` (list): List of package names to check

**Output:**
Prints to stdout the status and version of each package:
- Package name and version if available
- "installed, but no version info" for packages without version attributes
- "Not found!" for missing packages

**Example:**
```python
check_packages(['PIL', 'yaml', 'paho.mqtt'])
# Output:
# PIL :  8.3.2
# yaml :  6.0
# paho.mqtt :  1.6.1
```

##### `main() -> None`

Main entry point for the PicFrame application with three operational modes:

1. **Initialize Mode** (`-i/--initialize`): Sets up directory structure and configuration
2. **Version Mode** (`-v/--version`): Displays version and dependency information
3. **Run Mode** (default): Starts the PicFrame application

**Command Line Arguments:**
- `-i, --initialize DIRECTORY`: Initialize PicFrame structure in DIRECTORY
- `-v, --version`: Show version and dependency information
- `configfile`: Path to configuration YAML file (optional, positional)

**Application Architecture (Run Mode):**
- **Model**: Handles configuration, image database, and business logic
- **ViewerDisplay**: Manages display rendering and visual presentation
- **Controller**: Coordinates user input, interfaces, and application flow

---

### controller.py - Application Controller

The Controller component of the MVC architecture, managing user interactions, interface communications, and application lifecycle.

#### Utility Functions

##### `make_date(txt: str) -> float`

Convert a date string to Unix timestamp for database queries and date filtering.

**Parameters:**
- `txt` (str): Date string in various formats (e.g., "2023/12/25", "2023-12-25")

**Returns:**
- `float`: Unix timestamp representing the parsed date

**Example:**
```python
make_date("2023/12/25")  # Returns: 1703462400.0
make_date("2023-01-01")  # Returns: 1672531200.0
```

#### Classes

##### `Controller`

Central Controller for PicFrame Application implementing the MVC pattern.

**Constructor:**
```python
Controller(model: Model, viewer: ViewerDisplay)
```

**Parameters:**
- `model` (Model): The Model instance containing business logic and configuration
- `viewer` (ViewerDisplay): The ViewerDisplay instance handling presentation

**Properties:**

###### `paused: bool`
Get or set the current state for pausing image display.

```python
controller.paused = True   # Pause slideshow
is_paused = controller.paused  # Check pause state
```

###### `subdirectory: str`
Get or set the current subdirectory filter for image selection.

```python
controller.subdirectory = "vacation_photos"
current_dir = controller.subdirectory
```

###### `date_from: float`
Get or set the start date filter for image selection (Unix timestamp).

```python
controller.date_from = "2023/01/01"  # String format
controller.date_from = 1672531200.0  # Unix timestamp
```

###### `date_to: float`
Get or set the end date filter for image selection (Unix timestamp).

```python
controller.date_to = "2023/12/31"
controller.date_to = 1703980800.0
```

###### `display_is_on: bool`
Get or set the current display power state.

```python
controller.display_is_on = False  # Turn off display
is_on = controller.display_is_on  # Check display state
```

###### `shuffle: bool`
Get or set the random image order state.

```python
controller.shuffle = True  # Enable random order
is_shuffled = controller.shuffle
```

###### `time_delay: float`
Get or set the display duration for each image (minimum 5 seconds).

```python
controller.time_delay = 30.0  # 30 seconds per image
delay = controller.time_delay
```

###### `brightness: float`
Get or set the display brightness level (0.0 to 1.0).

```python
controller.brightness = 0.8  # 80% brightness
current_brightness = controller.brightness
```

**Methods:**

###### `next() -> None`
Advance to the next image in the slideshow.

```python
controller.next()  # Move to next image
```

###### `back() -> None`
Navigate to the previous image in the slideshow.

```python
controller.back()  # Move to previous image
```

###### `delete() -> None`
Delete the currently displayed image and move to deleted folder.

```python
controller.delete()  # Delete current image
```

###### `get_number_of_files() -> int`
Get the total count of available images.

```python
count = controller.get_number_of_files()
print(f"Total images: {count}")
```

###### `get_directory_list() -> Tuple[str, List[str]]`
Get the current directory and list of available subdirectories.

```python
current_dir, dir_list = controller.get_directory_list()
print(f"Current: {current_dir}, Available: {dir_list}")
```

###### `get_current_path() -> str`
Get the file path of the currently displayed image.

```python
current_image = controller.get_current_path()
print(f"Now showing: {current_image}")
```

###### `start() -> None`
Initialize interfaces and begin slideshow operation.

```python
controller.start()  # Start all interfaces
```

###### `loop() -> None`
Main application loop for slideshow operation.

```python
controller.loop()  # Run main slideshow loop
```

###### `stop() -> None`
Graceful shutdown of all components.

```python
controller.stop()  # Clean shutdown
```

---

### model.py - Business Logic and Data Management

The Model component handling configuration, image database, and business logic.

#### Classes

##### `Pic`

Image metadata container class representing a single image file with all associated metadata.

**Constructor:**
```python
Pic(fname: str, last_modified: float, file_id: int, 
    orientation: int = 1, exif_datetime: float = 0, ...)
```

**Attributes:**
- `fname` (str): Full file path to the image
- `width` (int): Image width in pixels
- `height` (int): Image height in pixels
- `exif_datetime` (float): Unix timestamp from EXIF date/time
- `latitude` (float): GPS latitude coordinate
- `longitude` (float): GPS longitude coordinate
- `location` (str): Reverse-geocoded location description
- `make` (str): Camera manufacturer
- `model` (str): Camera model
- `tags` (str): Comma-separated tags for categorization

**Example:**
```python
pic = Pic(fname="/path/to/image.jpg", file_id=123, width=1920, height=1080)
print(f"Image: {pic.fname}, Size: {pic.width}x{pic.height}")
```

##### `Model`

Core business logic and data management for PicFrame.

**Constructor:**
```python
Model(configfile: str = DEFAULT_CONFIGFILE)
```

**Parameters:**
- `configfile` (str): Path to YAML configuration file

**Configuration Access Methods:**

###### `get_viewer_config() -> dict`
Get display/rendering configuration section.

```python
viewer_config = model.get_viewer_config()
font_file = viewer_config['font_file']
```

###### `get_model_config() -> dict`
Get core application configuration section.

```python
model_config = model.get_model_config()
pic_dir = model_config['pic_dir']
```

###### `get_mqtt_config() -> dict`
Get MQTT interface configuration section.

```python
mqtt_config = model.get_mqtt_config()
if mqtt_config['use_mqtt']:
    server = mqtt_config['server']
```

###### `get_http_config() -> dict`
Get HTTP interface configuration section.

```python
http_config = model.get_http_config()
if http_config['use_http']:
    port = http_config['port']
```

**Image Management Methods:**

###### `get_next_file() -> Tuple[Pic, Pic]`
Get the next image(s) for display (returns tuple for portrait pairs).

```python
pic1, pic2 = model.get_next_file()
if pic1:
    print(f"Next image: {pic1.fname}")
```

###### `get_current_pics() -> Tuple[Pic, Pic]`
Get currently displayed image(s).

```python
current_pic, pair_pic = model.get_current_pics()
if current_pic:
    print(f"Current: {current_pic.fname}")
```

###### `get_number_of_files() -> int`
Get total available image count.

```python
total = model.get_number_of_files()
print(f"Total images available: {total}")
```

###### `delete_file() -> None`
Move current image to deleted folder.

```python
model.delete_file()  # Move to deleted pictures folder
```

**Directory Operations:**

###### `get_directory_list() -> Tuple[str, List[str]]`
Get current directory and available subdirectories.

```python
current, directories = model.get_directory_list()
print(f"Current: {current}")
print(f"Available: {directories}")
```

###### `force_reload() -> None`
Trigger image list refresh from file system.

```python
model.force_reload()  # Refresh image database
```

---

## Interface Modules

### interface_mqtt.py - MQTT Communication

MQTT interface for remote control and Home Assistant integration.

#### Classes

##### `InterfaceMQTT`

MQTT communication interface with Home Assistant auto-discovery.

**Constructor:**
```python
InterfaceMQTT(controller: Controller, mqtt_config: dict)
```

**Parameters:**
- `controller` (Controller): PicFrame controller instance
- `mqtt_config` (dict): MQTT configuration parameters

**Configuration Requirements:**
```yaml
mqtt:
  use_mqtt: true
  server: "mqtt.example.com"
  port: 8883
  login: "username"
  password: "password"
  device_id: "picframe_living_room"
  tls: "/path/to/ca.crt"  # Optional
```

**Supported Entity Types:**
- **Sensors**: image, image_counter (diagnostic information)
- **Switches**: display, paused, shuffle, text toggles
- **Numbers**: brightness, time_delay, fade_time, matting_images
- **Selects**: directory selection with dynamic options
- **Buttons**: next, back, delete (navigation controls)
- **Text Inputs**: date_from, date_to, location_filter, tags_filter

**MQTT Topic Structure:**
- Commands: `{device_id}/{parameter}` for setting values
- States: `homeassistant/sensor/{device_id}/state` for status
- Configs: `homeassistant/{type}/{device_id}_{param}/config` for discovery
- Availability: `homeassistant/switch/{device_id}/available` for connection status

**Methods:**

###### `stop() -> None`
Graceful shutdown of MQTT interface.

```python
mqtt_interface.stop()  # Clean MQTT shutdown
```

###### `publish_state(fname: str = None, image_attr: dict = None) -> None`
Publish current device state to MQTT broker.

```python
# Called automatically by controller
mqtt_interface.publish_state(current_image, metadata)
```

**Example Usage:**
```python
# MQTT interface is automatically initialized by Controller
controller = Controller(model, viewer)
controller.start()  # Starts MQTT if configured

# Control via MQTT messages:
# Topic: picframe_living_room/brightness
# Payload: 0.8

# Topic: picframe_living_room/paused  
# Payload: true
```

---

### interface_http.py - HTTP Web Interface

HTTP server interface providing web-based control and monitoring.

#### Functions

##### `heif_to_jpg(fname: str) -> str`

Convert HEIF/HEIC image files to JPEG format for web compatibility.

**Parameters:**
- `fname` (str): Full path to the HEIF/HEIC image file to convert

**Returns:**
- `str`: Path to converted JPEG file if successful, empty string if conversion fails

**Example:**
```python
converted_path = heif_to_jpg("/path/to/image.heic")
if converted_path:
    # Serve the converted JPEG file
    serve_file(converted_path)
```

#### Classes

##### `RequestHandler(BaseHTTPRequestHandler)`

HTTP request handler for PicFrame web interface.

**Supported HTTP Methods:**
- `GET`: Static files, API queries, image streaming
- `POST`: API parameter updates (delegates to GET handler)

**Authentication:**
- HTTP Basic Authentication (optional)
- Configurable username/password
- Auto-generated secure credentials

**API Endpoints:**
- `GET /?parameter`: Query current parameter values
- `GET /?parameter=value`: Set parameter values  
- `GET /?all`: Retrieve all available parameters
- `GET /current_image`: Stream currently displayed image
- `GET /filename.ext`: Serve static files

**Example API Calls:**
```bash
# Query current brightness
curl "http://picframe:9000/?brightness"

# Set brightness to 80%
curl "http://picframe:9000/?brightness=0.8"

# Get all parameters
curl "http://picframe:9000/?all"

# Get current image
curl "http://picframe:9000/current_image" > current.jpg
```

##### `InterfaceHttp(HTTPServer)`

HTTP server interface for web-based PicFrame control.

**Constructor:**
```python
InterfaceHttp(controller, html_path, pic_dir, no_files_img, 
              port=9000, auth=False, username=None, password=None)
```

**Parameters:**
- `controller`: PicFrame Controller instance
- `html_path`: Directory containing web interface files
- `pic_dir`: Picture directory for image access
- `no_files_img`: Default image when no pictures available
- `port`: TCP port for HTTP server (default: 9000)
- `auth`: Enable HTTP Basic Authentication (default: False)
- `username`: Authentication username (auto-generated if None)
- `password`: Authentication password (auto-generated if None)

**Methods:**

###### `stop() -> None`
Graceful server shutdown with thread cleanup.

```python
http_interface.stop()  # Clean HTTP shutdown
```

**Configuration Example:**
```yaml
http:
  use_http: true
  path: "~/picframe_data/html"
  port: 9000
  use_ssl: false
  auth: true
  username: "admin"
  password: "secure_password"
```

---

### interface_peripherals.py - Direct Input Control

Peripheral input interface for keyboard, touch, and mouse control.

#### Classes

##### `InterfacePeripherals`

Peripheral input interface for direct PicFrame control.

**Constructor:**
```python
InterfacePeripherals(model, viewer, controller)
```

**Parameters:**
- `model` (Model): PicFrame model containing configuration
- `viewer` (ViewerDisplay): Display viewer for screen dimensions
- `controller` (Controller): Application controller for command execution

**Supported Input Types:**
- **Keyboard**: Arrow keys, shortcuts, menu navigation
- **Touch**: Touch screen with gesture recognition
- **Mouse**: Mouse pointer with click detection

**Input Method Behaviors:**

**Keyboard Mode:**
- Arrow keys: LEFT/RIGHT for previous/next image
- Shortcut keys: Configurable per menu item
- ESCAPE: Application exit
- Space bar: Pause/resume slideshow

**Touch Mode:**
- Left/right screen areas: Image navigation
- Top area touch: Menu activation
- Menu auto-hide: Configurable timeout
- Touch anywhere: Wake display when off

**Mouse Mode:**
- Left/right click areas: Image navigation
- Mouse hover in top area: Show menu
- Left click: Menu item activation
- Mouse movement: Wake display when off

**Properties:**

###### `menu_is_on: bool`
Current menu visibility state with auto-hide management.

```python
peripherals.menu_is_on = True   # Show menu
is_visible = peripherals.menu_is_on  # Check menu state
```

**Methods:**

###### `check_input() -> None`
Main input processing loop (called from controller).

```python
# Called automatically by Controller.loop()
peripherals.check_input()  # Process input events
```

###### `stop() -> None`
Graceful shutdown of input devices.

```python
peripherals.stop()  # Clean input shutdown
```

**Configuration Example:**
```yaml
peripherals:
  input_type: "touch"  # "keyboard", "touch", "mouse", or null
  buttons:
    pause:
      enable: true
      label: "Pause"
      shortcut: " "  # Space bar
    display_off:
      enable: true
      label: "Display Off"
      shortcut: "o"
    exit:
      enable: false
      label: "Exit"
      shortcut: "e"
```

##### `IPMenuItem`

Base class for peripheral interface menu items.

**Subclasses:**
- `PauseMenuItem`: Toggle slideshow pause/resume
- `DisplayOffMenuItem`: Turn off display
- `LocationMenuItem`: Toggle location text overlay
- `ExitMenuItem`: Exit PicFrame application
- `PowerDownMenuItem`: Shutdown system

**Creating Custom Menu Items:**
```python
class CustomMenuItem(IPMenuItem):
    config_name = "custom_action"
    
    def action(self):
        # Implement custom functionality
        self.ip.controller.some_custom_method()
```

---

## Utility Modules

### viewer_display.py - Display Rendering

Display rendering and image presentation module (detailed documentation available in existing docstrings).

### image_cache.py - Image Database Management  

Image database management and metadata caching module (detailed documentation available in existing docstrings).

### get_image_meta.py - Metadata Extraction

EXIF metadata extraction and processing module (detailed documentation available in existing docstrings).

---

## Usage Examples

### Basic Application Startup

```python
from picframe import model, viewer_display, controller

# Initialize components
m = model.Model("~/picframe_data/config/configuration.yaml")
v = viewer_display.ViewerDisplay(m.get_viewer_config())
c = controller.Controller(m, v)

# Start application
c.start()
c.loop()
c.stop()
```

### Programmatic Control

```python
# Control slideshow
controller.paused = True        # Pause slideshow
controller.next()              # Next image
controller.back()              # Previous image
controller.brightness = 0.5    # Set brightness to 50%

# Apply filters
controller.subdirectory = "vacation"
controller.date_from = "2023/01/01"
controller.location_filter = "Paris"

# Get information
total_images = controller.get_number_of_files()
current_image = controller.get_current_path()
directories = controller.get_directory_list()
```

### Configuration Access

```python
# Access configuration sections
viewer_config = model.get_viewer_config()
model_config = model.get_model_config()
mqtt_config = model.get_mqtt_config()

# Modify runtime settings
model.time_delay = 30.0        # 30 seconds per image
model.shuffle = True           # Enable random order
model.fade_time = 5.0          # 5 second transitions
```

This API reference provides comprehensive documentation for integrating with and extending the PicFrame application. For additional examples and advanced usage, refer to the source code and configuration documentation.