# PicFrame External Interface Contracts

This document provides comprehensive documentation for all external interfaces supported by PicFrame, including MQTT topics, HTTP API endpoints, and configuration file schemas.

## Table of Contents

- [MQTT Interface Contract](#mqtt-interface-contract)
- [HTTP API Interface Contract](#http-api-interface-contract)
- [Configuration File Schema](#configuration-file-schema)
- [Message Format Specifications](#message-format-specifications)

---

## MQTT Interface Contract

PicFrame provides comprehensive MQTT integration with Home Assistant auto-discovery support. The interface follows standard MQTT conventions and Home Assistant discovery protocols.

### Connection Configuration

```yaml
mqtt:
  use_mqtt: true                    # Enable MQTT interface
  server: "mqtt.example.com"        # MQTT broker hostname/IP
  port: 8883                        # MQTT broker port (1883 for plain, 8883 for TLS)
  login: "username"                 # MQTT authentication username
  password: "password"              # MQTT authentication password
  tls: "/path/to/ca.crt"           # TLS certificate file (optional)
  device_id: "picframe_living_room" # Unique device identifier
  device_url: "http://192.168.1.100:9000" # Web interface URL (optional)
```

### Topic Structure

All MQTT topics follow a hierarchical structure based on the device ID and Home Assistant discovery conventions.

#### Command Topics (Inbound)
Commands sent TO PicFrame to control its operation:

```
{device_id}/{parameter}
```

**Examples:**
- `picframe_living_room/brightness` - Set display brightness
- `picframe_living_room/paused` - Pause/resume slideshow
- `picframe_living_room/time_delay` - Set image display duration

#### State Topics (Outbound)
Status information sent FROM PicFrame:

```
homeassistant/sensor/{device_id}/state
```

**Example:**
- `homeassistant/sensor/picframe_living_room/state` - Current device state

#### Discovery Topics (Outbound)
Home Assistant auto-discovery configuration:

```
homeassistant/{entity_type}/{device_id}_{parameter}/config
```

**Examples:**
- `homeassistant/switch/picframe_living_room_paused/config`
- `homeassistant/number/picframe_living_room_brightness/config`
- `homeassistant/sensor/picframe_living_room_image/config`

#### Availability Topic (Outbound)
Device online/offline status:

```
homeassistant/switch/{device_id}/available
```

**Payloads:**
- `online` - Device is connected and operational
- `offline` - Device is disconnected (Last Will and Testament)

### Supported Entity Types

#### Sensors (Read-Only Information)

##### Image Sensor
- **Topic**: `homeassistant/sensor/{device_id}_image/state`
- **Purpose**: Current image information with metadata attributes
- **Payload**: JSON object with image details
- **Attributes Topic**: `homeassistant/sensor/{device_id}_image/attributes`

**Example State Message:**
```json
{
  "image": "/home/user/Pictures/vacation/beach.jpg"
}
```

**Example Attributes Message:**
```json
{
  "PICFRAME GPS": "40.7128,-74.0060",
  "PICFRAME LOCATION": "New York, NY, USA",
  "EXIF FNumber": "f/2.8",
  "EXIF ExposureTime": "1/125",
  "EXIF ISOSpeedRatings": "200",
  "Image Make": "Canon",
  "Image Model": "EOS R5"
}
```

##### Image Counter Sensor
- **Topic**: `homeassistant/sensor/{device_id}_image_counter/state`
- **Purpose**: Total number of available images
- **Payload**: Numeric value

**Example:**
```json
{
  "image_counter": 1247
}
```

#### Switches (On/Off Controls)

##### Display Switch
- **Command Topic**: `homeassistant/switch/{device_id}_display/set`
- **State Topic**: `homeassistant/switch/{device_id}_display/state`
- **Purpose**: Control display power state
- **Payloads**: `ON` / `OFF`

##### Paused Switch
- **Command Topic**: `homeassistant/switch/{device_id}_paused/set`
- **State Topic**: `homeassistant/switch/{device_id}_paused/state`
- **Purpose**: Pause/resume slideshow
- **Payloads**: `ON` (paused) / `OFF` (playing)

##### Shuffle Switch
- **Command Topic**: `homeassistant/switch/{device_id}_shuffle/set`
- **State Topic**: `homeassistant/switch/{device_id}_shuffle/state`
- **Purpose**: Enable/disable random image order
- **Payloads**: `ON` (shuffled) / `OFF` (sequential)

##### Text Overlay Switches
Control visibility of various text overlays:

- `{device_id}_name_toggle` - Image filename display
- `{device_id}_title_toggle` - Image title from metadata
- `{device_id}_caption_toggle` - Image caption from metadata
- `{device_id}_date_toggle` - Image date display
- `{device_id}_location_toggle` - GPS location display
- `{device_id}_directory_toggle` - Current directory display

**Payloads**: `ON` (visible) / `OFF` (hidden)

##### Utility Switches
- `{device_id}_text_refresh` - Refresh text overlays
- `{device_id}_text_off` - Hide all text overlays
- `{device_id}_clock` - Show/hide clock overlay

#### Numbers (Numeric Controls)

##### Brightness Control
- **Command Topic**: `{device_id}/brightness`
- **Range**: 0.0 to 1.0
- **Step**: 0.1
- **Purpose**: Control display brightness

**Example:**
```
Topic: picframe_living_room/brightness
Payload: 0.8
```

##### Time Delay Control
- **Command Topic**: `{device_id}/time_delay`
- **Range**: 1 to 400 seconds
- **Step**: 1
- **Purpose**: Set image display duration

##### Fade Time Control
- **Command Topic**: `{device_id}/fade_time`
- **Range**: 1 to 50 seconds
- **Step**: 1
- **Purpose**: Set transition duration between images

##### Matting Images Control
- **Command Topic**: `{device_id}/matting_images`
- **Range**: 0.0 to 1.0
- **Step**: 0.01
- **Purpose**: Control automatic image matting threshold

#### Selects (Dropdown Controls)

##### Directory Selection
- **Command Topic**: `{device_id}/directory`
- **Purpose**: Select image subdirectory
- **Options**: Dynamically populated from available directories

**Example:**
```
Topic: picframe_living_room/directory
Payload: "vacation_photos"
```

#### Buttons (Action Triggers)

##### Navigation Buttons
- **Next Button**: `homeassistant/button/{device_id}_next/set`
- **Back Button**: `homeassistant/button/{device_id}_back/set`
- **Delete Button**: `homeassistant/button/{device_id}_delete/set`

**Payload**: `ON` (trigger action)

#### Text Inputs (String Controls)

##### Date Filters
- **Date From**: `{device_id}/date_from`
- **Date To**: `{device_id}/date_to`
- **Format**: "YYYY/MM/DD" or Unix timestamp

**Examples:**
```
Topic: picframe_living_room/date_from
Payload: "2023/01/01"

Topic: picframe_living_room/date_to  
Payload: "2023/12/31"
```

##### Content Filters
- **Location Filter**: `{device_id}/location_filter`
- **Tags Filter**: `{device_id}/tags_filter`
- **Format**: Text string with boolean operators

**Examples:**
```
Topic: picframe_living_room/location_filter
Payload: "Paris OR London"

Topic: picframe_living_room/tags_filter
Payload: "vacation AND beach"
```

### Home Assistant Discovery Configuration

Each entity is automatically registered with Home Assistant using discovery messages. Here's an example configuration for a brightness control:

```json
{
  "name": "brightness",
  "min": 0.0,
  "max": 1.0,
  "step": 0.1,
  "icon": "mdi:brightness-6",
  "entity_category": "config",
  "state_topic": "homeassistant/sensor/picframe_living_room/state",
  "command_topic": "picframe_living_room/brightness",
  "value_template": "{{ value_json.brightness }}",
  "avty_t": "homeassistant/switch/picframe_living_room/available",
  "uniq_id": "picframe_living_room_brightness",
  "dev": {
    "ids": ["picframe_living_room"],
    "name": "picframe_living_room",
    "mdl": "PictureFrame",
    "sw": "2.0.0",
    "mf": "pi3d PictureFrame project",
    "cu": "http://192.168.1.100:9000"
  }
}
```

### State Message Format

The main state message contains all current parameter values:

```json
{
  "brightness": 0.8,
  "time_delay": 30.0,
  "fade_time": 10.0,
  "paused": false,
  "shuffle": true,
  "display": true,
  "directory": "vacation_photos",
  "date_from": "2023/01/01",
  "date_to": "2023/12/31",
  "location_filter": "",
  "tags_filter": "",
  "image": "/home/user/Pictures/vacation/beach.jpg",
  "image_counter": 1247
}
```

---

## HTTP API Interface Contract

PicFrame provides a RESTful HTTP API for web-based control and monitoring. The API supports both GET and POST requests with optional HTTP Basic Authentication.

### Server Configuration

```yaml
http:
  use_http: true                    # Enable HTTP interface
  path: "~/picframe_data/html"      # Web interface files directory
  port: 9000                        # HTTP server port
  auth: true                        # Enable HTTP Basic Authentication
  username: "admin"                 # Authentication username
  password: "secure_password"       # Authentication password
  use_ssl: false                    # Enable SSL/TLS encryption
  keyfile: "/path/to/key.pem"      # SSL private key file
  certfile: "/path/to/cert.pem"    # SSL certificate file
```

### Authentication

When authentication is enabled, all requests must include HTTP Basic Authentication headers:

```bash
curl -u admin:secure_password "http://picframe:9000/?brightness"
```

### API Endpoints

#### Parameter Query
Get current value of a parameter:

```
GET /?{parameter}
```

**Example:**
```bash
curl "http://picframe:9000/?brightness"
```

**Response:**
```json
{
  "brightness": 0.8
}
```

#### Parameter Update
Set new value for a parameter:

```
GET /?{parameter}={value}
POST /?{parameter}={value}
```

**Example:**
```bash
curl "http://picframe:9000/?brightness=0.5"
```

**Response:**
```json
{
  "brightness": 0.5
}
```

#### Bulk Parameter Query
Get all available parameters and their current values:

```
GET /?all
```

**Example:**
```bash
curl "http://picframe:9000/?all"
```

**Response:**
```json
{
  "brightness": 0.8,
  "time_delay": 30.0,
  "fade_time": 10.0,
  "paused": false,
  "shuffle": true,
  "display_is_on": true,
  "subdirectory": "vacation_photos",
  "date_from": 1672531200.0,
  "date_to": 1703980800.0,
  "location_filter": "",
  "tags_filter": "",
  "matting_images": 0.01
}
```

#### Current Image Access
Stream the currently displayed image:

```
GET /current_image
GET /current_image.jpg
```

**Example:**
```bash
curl "http://picframe:9000/current_image" > current.jpg
```

**Response:** Binary image data (JPEG format)

#### Static File Serving
Serve web interface files:

```
GET /{filename}
GET /  (serves index.html)
```

**Examples:**
```bash
curl "http://picframe:9000/"              # Serves index.html
curl "http://picframe:9000/style.css"     # Serves CSS file
curl "http://picframe:9000/script.js"     # Serves JavaScript file
```

### Supported Parameters

All Controller properties and methods are accessible via HTTP:

#### Display Control
- `brightness` (float 0.0-1.0): Display brightness level
- `display_is_on` (boolean): Display power state
- `paused` (boolean): Slideshow pause state

#### Navigation Control
- `next()`: Advance to next image (method call)
- `back()`: Return to previous image (method call)
- `delete()`: Delete current image (method call)

#### Timing Control
- `time_delay` (float): Image display duration in seconds (minimum 5.0)
- `fade_time` (float): Transition duration between images

#### Content Filtering
- `subdirectory` (string): Current subdirectory filter
- `date_from` (string/float): Start date filter ("YYYY/MM/DD" or timestamp)
- `date_to` (string/float): End date filter ("YYYY/MM/DD" or timestamp)
- `location_filter` (string): Geographic location filter with boolean operators
- `tags_filter` (string): Tag-based filter with boolean operators

#### Display Effects
- `shuffle` (boolean): Random image order state
- `matting_images` (float 0.0-1.0): Automatic matting threshold

#### Text Overlays
- `set_show_text()`: Configure text overlay display (method call with JSON parameters)

### Value Format Conversion

The HTTP interface automatically converts string values to appropriate types:

#### Boolean Values
- `"true"`, `"on"`, `"yes"` → `True`
- `"false"`, `"off"`, `"no"` → `False`

#### Method Calls with Parameters
For methods requiring parameters, use JSON format:

```bash
curl "http://picframe:9000/?set_show_text={\"txt_key\":\"location\",\"val\":\"ON\"}"
```

### Error Handling

#### HTTP Status Codes
- `200 OK`: Successful request
- `400 Bad Request`: Server error or malformed parameters
- `401 Unauthorized`: Missing authentication credentials
- `403 Forbidden`: Invalid authentication credentials
- `404 Not Found`: Invalid endpoint or file not found

#### Error Response Format
```json
{
  "ERROR": "Exception:parameter_name>error_description;"
}
```

### Image Format Support

The HTTP interface automatically handles different image formats:

#### Standard Formats
- JPEG, PNG: Served directly with appropriate MIME types

#### HEIF/HEIC Formats
- Automatically converted to JPEG for web browser compatibility
- Conversion uses temporary file in `/dev/shm/temp.jpg`

### Security Considerations

#### Authentication
- HTTP Basic Authentication with configurable credentials
- Auto-generated secure passwords stored in `basic_auth.txt`
- Base64 encoding for credential transmission

#### Network Security
- Designed for local network use only
- Should not be exposed to external internet access
- Optional SSL/TLS encryption support

#### Input Validation
- Parameter name validation against Controller attributes
- SQL injection prevention in filter parameters
- JSON parsing with error handling

---

## Configuration File Schema

PicFrame uses YAML configuration files with a hierarchical structure. The configuration is validated and merged with default values at startup.

### File Location
- Default: `~/picframe_data/config/configuration.yaml`
- Customizable via command line argument

### Schema Structure

```yaml
# Top-level configuration sections
viewer:      # Display and rendering settings
model:       # Core application and data settings  
mqtt:        # MQTT interface configuration
http:        # HTTP interface configuration
peripherals: # Input device configuration
```

### Viewer Configuration Section

Controls display rendering, visual effects, and text overlays:

```yaml
viewer:
  # Image Processing
  blur_amount: 12                    # Background blur intensity (default: 12)
  blur_zoom: 1.0                     # Background zoom factor (≥1.0, default: 1.0)
  blur_edges: false                  # Use blurred image for edge filling (default: false)
  edge_alpha: 0.5                    # Background opacity at edges (0.0-1.0, default: 0.5)
  
  # Display Settings
  fps: 20.0                          # Frame rate (default: 20.0)
  background: [0.2, 0.2, 0.3, 1.0]  # RGBA background color (default: [0.2, 0.2, 0.3, 1.0])
  fit: false                         # Scale to fit vs crop to fill (default: false)
  kenburns: false                    # Enable Ken Burns effect (default: false)
  
  # Display Positioning
  display_x: 0                       # Horizontal offset (default: 0)
  display_y: 0                       # Vertical offset (default: 0)
  display_w: null                    # Display width (null = auto, default: null)
  display_h: null                    # Display height (null = auto, default: null)
  display_power: 2                   # Power management method (0-2, default: 2)
  
  # Graphics Backend
  use_glx: false                     # Use GLX on X11 systems (default: false)
  use_sdl2: true                     # Use SDL2 backend (default: true)
  
  # Text Overlays
  font_file: "~/picframe_data/data/fonts/NotoSans-Regular.ttf"  # Font file path
  show_text: "title caption name date folder location"          # Text elements to show
  show_text_fm: "%b %d, %Y"         # Date format string (default: "%b %d, %Y")
  show_text_tm: 20.0                 # Text display duration (default: 20.0)
  show_text_sz: 40                   # Text size in pixels (default: 40)
  text_justify: "L"                  # Text alignment: L, C, R (default: "L")
  text_bkg_hgt: 0.25                 # Text background height (0.0-1.0, default: 0.25)
  text_opacity: 1.0                  # Text opacity (0.0-1.0, default: 1.0)
  
  # Image Matting
  mat_images: 0.01                   # Auto-matting threshold (default: 0.01)
  mat_type: null                     # Mat style selection (default: null = all types)
  outer_mat_color: null              # Outer mat RGB color (default: null = auto)
  inner_mat_color: null              # Inner mat RGB color (default: null = auto)
  outer_mat_border: 75               # Outer mat border pixels (default: 75)
  inner_mat_border: 40               # Inner mat border pixels (default: 40)
  outer_mat_use_texture: true        # Use texture for outer mat (default: true)
  inner_mat_use_texture: false       # Use texture for inner mat (default: false)
  mat_resource_folder: "~/picframe_data/data/mat"  # Mat texture directory
  
  # Clock Display
  show_clock: false                  # Enable clock overlay (default: false)
  clock_justify: "R"                 # Clock alignment: L, C, R (default: "R")
  clock_text_sz: 120                 # Clock text size (default: 120)
  clock_format: "%-I:%M"             # Clock format string (default: "%-I:%M")
  clock_opacity: 1.0                 # Clock opacity (0.0-1.0, default: 1.0)
  clock_top_bottom: "T"              # Clock position: T, B (default: "T")
  clock_wdt_offset_pct: 3.0          # Clock horizontal offset % (default: 3.0)
  clock_hgt_offset_pct: 3.0          # Clock vertical offset % (default: 3.0)
  
  # Menu System
  menu_text_sz: 40                   # Menu text size (default: 40)
  menu_autohide_tm: 10.0             # Menu auto-hide timeout (default: 10.0)
  
  # Geolocation
  geo_suppress_list: []              # Location text substrings to remove (default: [])
```

### Model Configuration Section

Controls core application behavior, file management, and data processing:

```yaml
model:
  # File System
  pic_dir: "~/Pictures"              # Root image directory (default: "~/Pictures")
  deleted_pictures: "~/DeletedPictures"  # Deleted images destination (default: "~/DeletedPictures")
  follow_links: false                # Follow symbolic links (default: false)
  no_files_img: "~/picframe_data/data/no_pictures.jpg"  # Default image when none available
  
  # Image Selection
  subdirectory: ""                   # Current subdirectory filter (default: "")
  shuffle: true                      # Random image order (default: true)
  recent_n: 7                        # Recent images priority days (default: 7)
  reshuffle_num: 1                   # Reshuffles before reload (default: 1)
  
  # Timing
  time_delay: 200.0                  # Image display duration seconds (default: 200.0)
  fade_time: 10.0                    # Transition duration seconds (default: 10.0)
  update_interval: 2.0               # File scan interval seconds (default: 2.0)
  
  # Database
  db_file: "~/picframe_data/data/pictureframe.db3"  # SQLite database file
  sort_cols: "fname ASC"             # Database sort order (default: "fname ASC")
  portrait_pairs: false              # Enable portrait image pairing (default: false)
  
  # Filtering
  location_filter: ""                # Geographic location filter (default: "")
  tags_filter: ""                    # Tag-based filter (default: "")
  
  # Geolocation Services
  load_geoloc: false                 # Enable reverse geocoding (default: false)
  geo_key: "your_email@example.com"  # Geolocation service API key (REQUIRED if load_geoloc=true)
  key_list:                          # Location hierarchy for reverse geocoding
    - ["tourism", "amenity", "isolated_dwelling"]
    - ["suburb", "village"]
    - ["city", "county"]
    - ["region", "state", "province"]
    - ["country"]
  
  # MQTT Attributes
  image_attr:                        # Image metadata sent via MQTT
    - "PICFRAME GPS"                 # GPS coordinates
    - "PICFRAME LOCATION"            # Reverse geocoded location
    - "EXIF FNumber"                 # Camera aperture
    - "EXIF ExposureTime"            # Shutter speed
    - "EXIF ISOSpeedRatings"         # ISO sensitivity
    - "Image Make"                   # Camera manufacturer
    - "Image Model"                  # Camera model
    - "IPTC Keywords"                # Image tags
  
  # Localization
  locale: "en_US.utf8"               # System locale (default: "en_US.utf8")
  
  # Logging
  log_level: "WARNING"               # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
  log_file: ""                       # Log file path (default: "" = console only)
```

### MQTT Configuration Section

Controls MQTT broker connection and Home Assistant integration:

```yaml
mqtt:
  use_mqtt: false                    # Enable MQTT interface (default: false)
  server: "mqtt.example.com"         # MQTT broker hostname/IP (REQUIRED)
  port: 8883                         # MQTT broker port (default: 8883 for TLS, 1883 for plain)
  login: "username"                  # MQTT authentication username (REQUIRED)
  password: "password"               # MQTT authentication password (REQUIRED)
  tls: "/path/to/ca.crt"            # TLS certificate file path (optional, "" for plain)
  device_id: "picframe"              # Unique device identifier (default: "picframe")
  device_url: "http://192.168.1.100:9000"  # Web interface URL for Home Assistant (optional)
```

### HTTP Configuration Section

Controls web server and HTTP API settings:

```yaml
http:
  use_http: false                    # Enable HTTP interface (default: false)
  path: "~/picframe_data/html"       # Web interface files directory (REQUIRED)
  port: 9000                         # HTTP server port (default: 9000)
  auth: false                        # Enable HTTP Basic Authentication (default: false)
  username: "admin"                  # Authentication username (optional)
  password: null                     # Authentication password (null = auto-generate)
  use_ssl: false                     # Enable SSL/TLS encryption (default: false)
  keyfile: "/path/to/key.pem"       # SSL private key file (REQUIRED if use_ssl=true)
  certfile: "/path/to/cert.pem"     # SSL certificate file (REQUIRED if use_ssl=true)
```

### Peripherals Configuration Section

Controls direct input devices and menu system:

```yaml
peripherals:
  input_type: null                   # Input device type: null, "keyboard", "touch", "mouse"
  buttons:                           # Menu button configuration
    pause:                           # Pause/resume slideshow
      enable: true                   # Enable this menu item (default: true)
      label: "Pause"                 # Display label (default: "Pause")
      shortcut: " "                  # Keyboard shortcut (default: space)
    display_off:                     # Turn off display
      enable: true                   # Enable this menu item (default: true)
      label: "Display off"           # Display label (default: "Display off")
      shortcut: "o"                  # Keyboard shortcut (default: "o")
    location:                        # Toggle location display
      enable: false                  # Enable this menu item (default: false)
      label: "Location"              # Display label (default: "Location")
      shortcut: "l"                  # Keyboard shortcut (default: "l")
    exit:                            # Exit application
      enable: false                  # Enable this menu item (default: false)
      label: "Exit"                  # Display label (default: "Exit")
      shortcut: "e"                  # Keyboard shortcut (default: "e")
    power_down:                      # System shutdown
      enable: false                  # Enable this menu item (default: false)
      label: "Power down"            # Display label (default: "Power down")
      shortcut: "p"                  # Keyboard shortcut (default: "p")
```

### Configuration Validation Rules

#### Required Fields
- `mqtt.server`, `mqtt.login`, `mqtt.password` (if `mqtt.use_mqtt = true`)
- `http.path` (if `http.use_http = true`)
- `http.keyfile`, `http.certfile` (if `http.use_ssl = true`)
- `model.geo_key` (if `model.load_geoloc = true`)

#### Value Constraints
- `viewer.blur_zoom` ≥ 1.0
- `viewer.edge_alpha`, `viewer.text_opacity`, `viewer.clock_opacity` ∈ [0.0, 1.0]
- `viewer.display_power` ∈ {0, 1, 2}
- `viewer.text_justify`, `viewer.clock_justify` ∈ {"L", "C", "R"}
- `viewer.clock_top_bottom` ∈ {"T", "B"}
- `model.time_delay` ≥ 5.0 (enforced at runtime)
- `peripherals.input_type` ∈ {null, "keyboard", "touch", "mouse"}

#### Path Expansion
All file and directory paths support tilde (`~`) expansion for user home directory.

---

## Message Format Specifications

### MQTT Message Formats

#### State Message Format
```json
{
  "brightness": 0.8,
  "time_delay": 30.0,
  "fade_time": 10.0,
  "paused": false,
  "shuffle": true,
  "display": true,
  "directory": "vacation_photos",
  "date_from": "2023/01/01",
  "date_to": "2023/12/31",
  "location_filter": "",
  "tags_filter": "",
  "image": "/home/user/Pictures/vacation/beach.jpg",
  "image_counter": 1247
}
```

#### Image Attributes Format
```json
{
  "PICFRAME GPS": "40.7128,-74.0060",
  "PICFRAME LOCATION": "New York, NY, USA",
  "EXIF FNumber": "f/2.8",
  "EXIF ExposureTime": "1/125",
  "EXIF ISOSpeedRatings": "200",
  "EXIF FocalLength": "85mm",
  "EXIF DateTimeOriginal": "2023:07:15 14:30:22",
  "Image Make": "Canon",
  "Image Model": "EOS R5",
  "IPTC Caption/Abstract": "Beautiful sunset at the beach",
  "IPTC Object Name": "Beach Sunset",
  "IPTC Keywords": "beach, sunset, vacation, nature"
}
```

#### Home Assistant Discovery Format
```json
{
  "name": "brightness",
  "min": 0.0,
  "max": 1.0,
  "step": 0.1,
  "icon": "mdi:brightness-6",
  "entity_category": "config",
  "state_topic": "homeassistant/sensor/picframe_living_room/state",
  "command_topic": "picframe_living_room/brightness",
  "value_template": "{{ value_json.brightness }}",
  "avty_t": "homeassistant/switch/picframe_living_room/available",
  "uniq_id": "picframe_living_room_brightness",
  "dev": {
    "ids": ["picframe_living_room"],
    "name": "picframe_living_room",
    "mdl": "PictureFrame",
    "sw": "2.0.0",
    "mf": "pi3d PictureFrame project",
    "cu": "http://192.168.1.100:9000"
  }
}
```

### HTTP Response Formats

#### Parameter Query Response
```json
{
  "brightness": 0.8
}
```

#### Bulk Query Response
```json
{
  "brightness": 0.8,
  "time_delay": 30.0,
  "fade_time": 10.0,
  "paused": false,
  "shuffle": true,
  "display_is_on": true,
  "subdirectory": "vacation_photos"
}
```

#### Error Response
```json
{
  "ERROR": "Exception:brightness>could not convert string to float: 'invalid';"
}
```

### Filter Expression Syntax

Both location and tags filters support boolean expressions:

#### Operators
- `AND` - Logical AND operation
- `OR` - Logical OR operation  
- `NOT` - Logical NOT operation
- `()` - Grouping parentheses

#### Examples
```
# Simple text matching
"Paris"

# Boolean combinations
"Paris OR London"
"vacation AND beach"
"NOT work"

# Complex expressions with grouping
"(Paris OR London) AND (vacation OR holiday)"
"beach AND (sunset OR sunrise) AND NOT cloudy"
```

#### SQL Translation
Filters are converted to SQL LIKE clauses with case-insensitive matching:
- `"Paris"` → `location LIKE '%Paris%'`
- `"Paris OR London"` → `(location LIKE '%Paris%' OR location LIKE '%London%')`

This comprehensive documentation covers all external interface contracts for PicFrame, enabling developers and integrators to build custom applications and integrations with the digital picture frame system.