# PicFrame Architecture Documentation

## System Overview

PicFrame is a sophisticated digital picture frame application built on the pi3d graphics library, designed primarily for Raspberry Pi devices. The system provides advanced image and video display capabilities with extensive smart home integration through MQTT and HTTP interfaces.

### Key Features
- **Advanced Image Processing**: Support for multiple formats including HEIF/HEIC, with automatic rotation, matting, and Ken Burns effects
- **Video Support**: Full video playback with VLC integration
- **Smart Home Integration**: Native Home Assistant integration via MQTT discovery protocol
- **Multiple Control Interfaces**: MQTT, HTTP REST API, keyboard, touch, and mouse input
- **Geolocation Services**: Automatic location tagging using reverse geocoding
- **Database-Driven**: SQLite-based image cache with metadata extraction
- **Configurable Display**: Flexible text overlays, clock display, and visual effects

## MVC Architecture Pattern Implementation

PicFrame follows a clean Model-View-Controller (MVC) architecture pattern that separates concerns and enables maintainable, extensible code.

```mermaid
graph TB
    subgraph "MVC Core"
        M[Model<br/>model.py]
        V[ViewerDisplay<br/>viewer_display.py]
        C[Controller<br/>controller.py]
    end
    
    subgraph "External Interfaces"
        MQTT[MQTT Interface<br/>interface_mqtt.py]
        HTTP[HTTP Interface<br/>interface_http.py]
        PERIPH[Peripheral Interface<br/>interface_peripherals.py]
    end
    
    subgraph "Data Layer"
        IC[Image Cache<br/>image_cache.py]
        GR[Geo Reverse<br/>geo_reverse.py]
        META[Image Metadata<br/>get_image_meta.py]
    end
    
    subgraph "Presentation Layer"
        MAT[Mat Image<br/>mat_image.py]
        VIDEO[Video Streamer<br/>video_streamer.py]
    end
    
    C --> M
    C --> V
    M --> IC
    M --> GR
    V --> MAT
    V --> VIDEO
    V --> META
    
    MQTT --> C
    HTTP --> C
    PERIPH --> C
    
    IC --> META
    IC --> GR
```

### Model (model.py)
**Responsibilities:**
- Configuration management and validation
- Business logic for image selection and filtering
- Database query orchestration
- File system monitoring and management
- State management for display properties

**Key Components:**
- `Pic` class: Data structure representing image metadata
- Configuration loading and validation from YAML
- Image filtering logic (location, tags, date ranges)
- File list management with shuffle and sorting capabilities
- Integration with ImageCache for data persistence

### View (viewer_display.py)
**Responsibilities:**
- Graphics rendering using pi3d
- Image and video display management
- Text overlay rendering
- Visual effects (Ken Burns, transitions, matting)
- Display power management

**Key Components:**
- pi3d integration for hardware-accelerated graphics
- Image transformation and scaling algorithms
- Text rendering with configurable fonts and positioning
- Video playback integration with VLC
- Transition effects and timing management

### Controller (controller.py)
**Responsibilities:**
- Orchestrating interactions between Model and View
- Handling user input from all interface types
- Managing application lifecycle and timing
- State synchronization across interfaces
- Error handling and recovery

**Key Components:**
- Main application loop with timing control
- Property-based interface for external control
- Signal handling for graceful shutdown
- Interface coordination (MQTT, HTTP, peripherals)

## Data Flow Diagrams

### Image Processing Pipeline

```mermaid
flowchart TD
    START([Application Start]) --> INIT[Initialize Components]
    INIT --> CACHE[Image Cache Scan]
    CACHE --> FILTER[Apply Filters]
    FILTER --> SELECT[Select Next Image]
    SELECT --> LOAD[Load Image File]
    LOAD --> META[Extract Metadata]
    META --> TRANSFORM[Apply Transformations]
    TRANSFORM --> RENDER[Render to Display]
    RENDER --> WAIT[Wait for Time Delay]
    WAIT --> SELECT
    
    subgraph "Parallel Processes"
        MQTT_IN[MQTT Commands] --> CONTROLLER[Controller Updates]
        HTTP_IN[HTTP Requests] --> CONTROLLER
        PERIPH_IN[Peripheral Input] --> CONTROLLER
        CONTROLLER --> MODEL_UPDATE[Update Model State]
        MODEL_UPDATE --> VIEW_UPDATE[Update View State]
    end
    
    CONTROLLER --> SELECT
```

### Database Update Flow

```mermaid
flowchart TD
    MONITOR[File System Monitor] --> DETECT[Detect Changes]
    DETECT --> QUEUE[Queue Modified Files]
    QUEUE --> PROCESS[Process File]
    PROCESS --> EXTRACT[Extract EXIF/IPTC]
    EXTRACT --> GEO{Has GPS Data?}
    GEO -->|Yes| REVERSE[Reverse Geocode]
    GEO -->|No| STORE[Store in Database]
    REVERSE --> STORE
    STORE --> NEXT{More Files?}
    NEXT -->|Yes| PROCESS
    NEXT -->|No| COMPLETE[Update Complete]
```

### Video Processing Pipeline

```mermaid
flowchart TD
    VIDEO_SELECT[Select Video File] --> VIDEO_CHECK[Check Format Support]
    VIDEO_CHECK --> VLC_INIT[Initialize VLC Player]
    VLC_INIT --> VIDEO_LOAD[Load Video]
    VIDEO_LOAD --> VIDEO_PLAY[Start Playback]
    VIDEO_PLAY --> FRAME_RENDER[Render Frame]
    FRAME_RENDER --> INPUT_CHECK[Check for Input]
    INPUT_CHECK --> CONTINUE{Continue Playing?}
    CONTINUE -->|Yes| FRAME_RENDER
    CONTINUE -->|No| VIDEO_STOP[Stop Video]
    VIDEO_STOP --> NEXT_IMAGE[Return to Image Display]
```

## Integration Patterns

### MQTT Integration Pattern

The MQTT interface implements the Home Assistant MQTT Discovery protocol for seamless smart home integration.

**Architecture:**
- **Discovery Protocol**: Automatic device registration with Home Assistant
- **State Synchronization**: Bidirectional state updates between PicFrame and Home Assistant
- **Entity Types**: Sensors, switches, buttons, numbers, selects, and text inputs
- **Availability Tracking**: Last Will and Testament for connection status

**Topic Structure:**
```
homeassistant/{component}/{device_id}_{entity}/config  # Discovery
homeassistant/{component}/{device_id}_{entity}/state   # State updates
{device_id}/{entity}                                   # Commands
```

**Key Features:**
- Automatic entity creation in Home Assistant
- Real-time state synchronization
- Comprehensive device information
- Graceful connection handling with reconnection logic

### HTTP Interface Pattern

The HTTP interface provides a RESTful API for web-based control and integration.

**Architecture:**
- **RESTful Design**: GET/POST requests for state queries and updates
- **Authentication**: Optional HTTP Basic Authentication
- **Static File Serving**: Web interface hosting
- **Real-time Image Access**: Current image streaming endpoint

**API Patterns:**
```
GET /?all                           # Get all current states
GET /?{property}                    # Get specific property value
POST /?{property}={value}           # Set property value
GET /current_image                  # Stream current image
GET /{static_file}                  # Serve static web files
```

**Security Features:**
- Optional HTTP Basic Authentication
- SSL/TLS support with certificate configuration
- Input validation and sanitization
- Configurable access controls

### Peripheral Interface Pattern

The peripheral interface provides direct hardware input support for standalone operation.

**Architecture:**
- **Input Abstraction**: Unified handling of keyboard, touch, and mouse input
- **Menu System**: pi3d-based GUI with configurable buttons
- **Navigation Areas**: Screen regions for image navigation
- **Power Management**: Display control integration

**Input Handling:**
- **Keyboard**: Direct key mapping with shortcuts
- **Touch**: Gesture-based navigation with menu overlay
- **Mouse**: Pointer-based interaction with hover effects
- **Menu System**: Configurable action buttons with visual feedback

## Component Interactions

### Startup Sequence

```mermaid
sequenceDiagram
    participant Start as start.py
    participant Model as model.py
    participant View as viewer_display.py
    participant Controller as controller.py
    participant Interfaces as External Interfaces
    
    Start->>Model: Initialize with config
    Model->>Model: Load configuration
    Model->>Model: Initialize ImageCache
    Start->>View: Initialize with viewer config
    View->>View: Setup pi3d display
    Start->>Controller: Initialize with Model & View
    Controller->>Interfaces: Start MQTT interface
    Controller->>Interfaces: Start HTTP interface
    Controller->>Interfaces: Start peripheral interface
    Controller->>Controller: Begin main loop
```

### Image Display Cycle

```mermaid
sequenceDiagram
    participant Controller as controller.py
    participant Model as model.py
    participant View as viewer_display.py
    participant Cache as image_cache.py
    
    Controller->>Model: get_next_file()
    Model->>Cache: query_cache()
    Cache-->>Model: file_list
    Model->>Model: select_image()
    Model-->>Controller: Pic object
    Controller->>View: slideshow_is_running(pics)
    View->>View: load_and_render()
    View-->>Controller: (running, skip, video_playing)
    Controller->>Controller: update_timing()
```

### External Command Processing

```mermaid
sequenceDiagram
    participant Interface as External Interface
    participant Controller as controller.py
    participant Model as model.py
    participant View as viewer_display.py
    
    Interface->>Controller: set_property(value)
    Controller->>Model: update_state()
    Model->>Model: validate_and_apply()
    Controller->>View: update_display()
    View->>View: refresh_rendering()
    Controller->>Interface: publish_state()
```

## Configuration Architecture

PicFrame uses a hierarchical YAML configuration system with sensible defaults and validation.

### Configuration Structure
```yaml
viewer:          # Display and rendering settings
model:           # Business logic and data settings  
mqtt:            # MQTT integration settings
http:            # HTTP interface settings
peripherals:     # Hardware input settings
```

### Configuration Loading Process
1. **Default Configuration**: Built-in defaults ensure system functionality
2. **File Loading**: YAML configuration file parsing with error handling
3. **Validation**: Type checking and range validation
4. **Merging**: Section-wise merging with defaults
5. **Expansion**: Path expansion and environment variable resolution

## Error Handling Strategy

### Graceful Degradation
- **Missing Files**: Automatic fallback to "no images" display
- **Network Failures**: Continue operation without external interfaces
- **Hardware Issues**: Fallback display modes and input methods

### Logging Architecture
- **Hierarchical Loggers**: Module-specific logging with configurable levels
- **File and Console Output**: Flexible logging destination configuration
- **Error Recovery**: Automatic retry mechanisms for transient failures

### Resource Management
- **Database Connections**: Proper connection lifecycle management
- **Graphics Resources**: pi3d resource cleanup and memory management
- **Thread Safety**: Synchronized access to shared resources

## Performance Considerations

### Image Processing Optimization
- **Caching Strategy**: Multi-level caching for images and metadata
- **Lazy Loading**: On-demand image processing and loading
- **Memory Management**: Efficient texture management in pi3d
- **Background Processing**: Asynchronous metadata extraction

### Database Performance
- **Indexing Strategy**: Optimized database indexes for common queries
- **Query Optimization**: Efficient SQL queries with proper WHERE clauses
- **Connection Pooling**: Managed database connection lifecycle
- **Batch Processing**: Bulk operations for file system updates

### Network Optimization
- **Connection Management**: Persistent connections with reconnection logic
- **Message Batching**: Efficient MQTT message handling
- **Compression**: Image compression for HTTP streaming
- **Caching Headers**: Proper HTTP caching for static resources

This architectural documentation provides a comprehensive overview of PicFrame's design, implementation patterns, and system interactions. The MVC pattern ensures clean separation of concerns, while the multiple integration interfaces provide flexible control options for various deployment scenarios.
##
 Detailed Component Diagrams

### Core System Components

```mermaid
graph TB
    subgraph "Application Entry Point"
        START[start.py<br/>- Argument parsing<br/>- Component initialization<br/>- Main execution loop]
    end
    
    subgraph "MVC Core Components"
        MODEL[model.py<br/>- Configuration management<br/>- Business logic<br/>- File selection<br/>- State management]
        
        VIEW[viewer_display.py<br/>- pi3d graphics rendering<br/>- Image/video display<br/>- Text overlays<br/>- Visual effects]
        
        CONTROLLER[controller.py<br/>- User input handling<br/>- Interface coordination<br/>- Application lifecycle<br/>- State synchronization]
    end
    
    subgraph "Data Management Layer"
        CACHE[image_cache.py<br/>- SQLite database<br/>- File system monitoring<br/>- Metadata extraction<br/>- Background updates]
        
        META[get_image_meta.py<br/>- EXIF data extraction<br/>- IPTC metadata parsing<br/>- Image analysis<br/>- Format detection]
        
        GEO[geo_reverse.py<br/>- GPS coordinate processing<br/>- Reverse geocoding API<br/>- Location caching<br/>- Address formatting]
    end
    
    subgraph "Presentation Layer"
        MAT[mat_image.py<br/>- Image matting effects<br/>- Border generation<br/>- Texture application<br/>- Visual enhancement]
        
        VIDEO[video_streamer.py<br/>- VLC integration<br/>- Video format support<br/>- Playback control<br/>- Frame extraction]
    end
    
    subgraph "Interface Layer"
        MQTT[interface_mqtt.py<br/>- Home Assistant discovery<br/>- State synchronization<br/>- Command processing<br/>- Connection management]
        
        HTTP[interface_http.py<br/>- REST API endpoints<br/>- Static file serving<br/>- Authentication<br/>- Image streaming]
        
        PERIPH[interface_peripherals.py<br/>- Hardware input handling<br/>- Menu system<br/>- Touch/mouse/keyboard<br/>- Display control]
    end
    
    START --> MODEL
    START --> VIEW
    START --> CONTROLLER
    
    CONTROLLER --> MODEL
    CONTROLLER --> VIEW
    
    MODEL --> CACHE
    MODEL --> GEO
    
    VIEW --> MAT
    VIEW --> VIDEO
    VIEW --> META
    
    CACHE --> META
    CACHE --> GEO
    
    MQTT --> CONTROLLER
    HTTP --> CONTROLLER
    PERIPH --> CONTROLLER
```

### Database Schema and Relationships

```mermaid
erDiagram
    FILES {
        integer file_id PK
        text fname
        integer last_modified
        integer orientation
        integer exif_datetime
        real f_number
        text exposure_time
        integer iso
        real focal_length
        text make
        text model
        text lens
        integer rating
        real latitude
        real longitude
        integer width
        integer height
        integer is_portrait
        text location
        text title
        text caption
        text tags
    }
    
    FOLDERS {
        text folder_path PK
        integer last_modified
        integer last_checked
    }
    
    LOCATION_CACHE {
        text coordinates PK
        text location
        integer timestamp
    }
    
    FILES ||--o{ FOLDERS : "contained_in"
    FILES ||--o{ LOCATION_CACHE : "references"
```

### Interface Communication Patterns

```mermaid
graph LR
    subgraph "External Systems"
        HA[Home Assistant]
        WEB[Web Browser]
        USER[User Input]
    end
    
    subgraph "Interface Layer"
        MQTT_IF[MQTT Interface]
        HTTP_IF[HTTP Interface]
        PERIPH_IF[Peripheral Interface]
    end
    
    subgraph "Controller Layer"
        CTRL[Controller]
    end
    
    subgraph "Business Logic"
        MODEL[Model]
        VIEW[View]
    end
    
    HA <-->|MQTT Messages| MQTT_IF
    WEB <-->|HTTP Requests| HTTP_IF
    USER <-->|Hardware Input| PERIPH_IF
    
    MQTT_IF -->|Commands| CTRL
    HTTP_IF -->|Commands| CTRL
    PERIPH_IF -->|Commands| CTRL
    
    CTRL <-->|State Updates| MODEL
    CTRL <-->|Display Updates| VIEW
    
    CTRL -->|State Publishing| MQTT_IF
    CTRL -->|Response Data| HTTP_IF
    CTRL -->|Visual Feedback| PERIPH_IF
```

## Threading and Concurrency Model

### Thread Architecture

```mermaid
graph TB
    subgraph "Main Thread"
        MAIN[Main Application Loop<br/>- Image display cycle<br/>- User input processing<br/>- Interface coordination]
    end
    
    subgraph "Background Threads"
        CACHE_THREAD[Image Cache Thread<br/>- File system monitoring<br/>- Database updates<br/>- Metadata extraction]
        
        MQTT_THREAD[MQTT Client Thread<br/>- Message processing<br/>- Connection management<br/>- State publishing]
        
        HTTP_THREAD[HTTP Server Thread<br/>- Request handling<br/>- Response generation<br/>- Static file serving]
        
        VIDEO_THREAD[Video Playback Thread<br/>- VLC integration<br/>- Frame rendering<br/>- Playback control]
    end
    
    subgraph "Synchronization"
        LOCKS[Thread Locks<br/>- Database write lock<br/>- State update locks<br/>- Resource access control]
    end
    
    MAIN <--> CACHE_THREAD
    MAIN <--> MQTT_THREAD
    MAIN <--> HTTP_THREAD
    MAIN <--> VIDEO_THREAD
    
    CACHE_THREAD -.-> LOCKS
    MQTT_THREAD -.-> LOCKS
    HTTP_THREAD -.-> LOCKS
    VIDEO_THREAD -.-> LOCKS
```

### Synchronization Mechanisms

1. **Database Write Lock**: Serializes database write operations across threads
2. **State Update Coordination**: Ensures consistent state across interfaces
3. **Resource Access Control**: Manages shared resources like display and files
4. **Graceful Shutdown**: Coordinated thread termination on application exit

## Memory Management Strategy

### Image Memory Management

```mermaid
flowchart TD
    LOAD[Load Image File] --> DECODE[Decode to PIL Image]
    DECODE --> RESIZE[Resize if Needed]
    RESIZE --> TEXTURE[Create pi3d Texture]
    TEXTURE --> DISPLAY[Display on Screen]
    DISPLAY --> CACHE_CHECK{Keep in Cache?}
    CACHE_CHECK -->|Yes| MEMORY_CACHE[Store in Memory]
    CACHE_CHECK -->|No| CLEANUP[Release Memory]
    MEMORY_CACHE --> EXPIRE[Cache Expiration]
    EXPIRE --> CLEANUP
    CLEANUP --> GC[Garbage Collection]
```

### Resource Lifecycle Management

1. **Texture Management**: Automatic cleanup of pi3d textures
2. **Database Connections**: Proper connection lifecycle with cleanup
3. **File Handles**: Automatic file handle management with context managers
4. **Memory Monitoring**: Periodic memory usage assessment and cleanup

## Security Architecture

### Authentication and Authorization

```mermaid
graph TB
    subgraph "HTTP Interface Security"
        HTTP_AUTH[HTTP Basic Auth<br/>- Username/password<br/>- Base64 encoding<br/>- Optional SSL/TLS]
    end
    
    subgraph "MQTT Interface Security"
        MQTT_AUTH[MQTT Authentication<br/>- Username/password<br/>- TLS encryption<br/>- Certificate validation]
    end
    
    subgraph "File System Security"
        FS_SEC[File System Access<br/>- Path validation<br/>- Directory traversal protection<br/>- Permission checking]
    end
    
    subgraph "Input Validation"
        INPUT_VAL[Input Sanitization<br/>- SQL injection prevention<br/>- Command injection protection<br/>- Data type validation]
    end
    
    HTTP_AUTH --> INPUT_VAL
    MQTT_AUTH --> INPUT_VAL
    FS_SEC --> INPUT_VAL
```

### Security Measures

1. **Input Sanitization**: All user inputs are validated and sanitized
2. **Path Validation**: File system access is restricted to configured directories
3. **Authentication**: Optional but recommended authentication for remote interfaces
4. **Encryption**: TLS/SSL support for secure communication
5. **Permission Management**: Proper file system permission handling

## Deployment Architecture

### Raspberry Pi Deployment

```mermaid
graph TB
    subgraph "Hardware Layer"
        RPI[Raspberry Pi<br/>- ARM processor<br/>- GPU acceleration<br/>- GPIO interfaces]
        DISPLAY[Display Device<br/>- HDMI/DSI connection<br/>- Touch capability<br/>- Power management]
        STORAGE[Storage<br/>- SD card<br/>- USB storage<br/>- Network storage]
    end
    
    subgraph "Operating System"
        RASPIOS[Raspberry Pi OS<br/>- Linux kernel<br/>- Graphics drivers<br/>- System services]
    end
    
    subgraph "Runtime Environment"
        PYTHON[Python Runtime<br/>- Python 3.x<br/>- Virtual environment<br/>- Package dependencies]
        PI3D[pi3d Graphics<br/>- OpenGL ES<br/>- Hardware acceleration<br/>- Shader support]
    end
    
    subgraph "Application Layer"
        PICFRAME[PicFrame Application<br/>- Main process<br/>- Background services<br/>- Configuration files]
    end
    
    subgraph "External Services"
        MQTT_BROKER[MQTT Broker<br/>- Home Assistant<br/>- Mosquitto<br/>- Cloud services]
        GEO_API[Geocoding API<br/>- OpenStreetMap<br/>- Google Maps<br/>- Custom services]
    end
    
    RPI --> RASPIOS
    DISPLAY --> RPI
    STORAGE --> RPI
    
    RASPIOS --> PYTHON
    RASPIOS --> PI3D
    
    PYTHON --> PICFRAME
    PI3D --> PICFRAME
    
    PICFRAME <--> MQTT_BROKER
    PICFRAME <--> GEO_API
```

### System Integration Points

1. **Hardware Integration**: Direct hardware access for display and input
2. **Service Integration**: Systemd service configuration for automatic startup
3. **Network Integration**: WiFi/Ethernet connectivity for remote interfaces
4. **Storage Integration**: Flexible storage options for images and database
5. **Power Management**: Display power control and system power management

This comprehensive architectural documentation covers all aspects of the PicFrame system, from high-level design patterns to detailed implementation specifics. The documentation serves as a complete reference for understanding the system's structure, data flows, and integration patterns.