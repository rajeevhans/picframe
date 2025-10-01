# PicFrame Integration Tutorials

This guide provides step-by-step instructions for integrating PicFrame with smart home systems, MQTT brokers, and creating custom automation scenarios.

## Table of Contents

- [Home Assistant Integration](#home-assistant-integration)
- [MQTT Broker Setup](#mqtt-broker-setup)
- [Custom Automation Scenarios](#custom-automation-scenarios)
- [Advanced Integration Examples](#advanced-integration-examples)
- [Troubleshooting Integrations](#troubleshooting-integrations)

## Home Assistant Integration

PicFrame provides seamless integration with Home Assistant through MQTT discovery, automatically creating entities for remote control and monitoring.

### Prerequisites

Before starting, ensure you have:
- Home Assistant running with MQTT integration configured
- An MQTT broker (Mosquitto recommended)
- PicFrame installed and configured
- Network connectivity between all components

### Step 1: Configure MQTT in Home Assistant

#### Enable MQTT Integration

1. **Install MQTT Broker Add-on** (if using Home Assistant OS):
   ```yaml
   # In Home Assistant: Settings > Add-ons > Add-on Store
   # Search for "Mosquitto broker" and install
   ```

2. **Configure MQTT Integration**:
   - Go to Settings > Devices & Services
   - Click "Add Integration" and search for "MQTT"
   - Configure with your broker settings:
     ```
     Broker: localhost (or your broker IP)
     Port: 1883
     Username: (your MQTT username)
     Password: (your MQTT password)
     ```

3. **Verify MQTT is Working**:
   ```yaml
   # Add to configuration.yaml for testing
   mqtt:
     sensor:
       - name: "MQTT Test"
         state_topic: "test/topic"
   ```

### Step 2: Configure PicFrame for Home Assistant

#### Update PicFrame Configuration

Edit `~/picframe_data/config/configuration.yaml`:

```yaml
mqtt:
  use_mqtt: True                    # Enable MQTT integration
  server: "homeassistant.local"     # Your Home Assistant IP/hostname
  port: 1883                        # MQTT port (1883 for non-TLS)
  login: "picframe_user"            # MQTT username
  password: "your_secure_password"  # MQTT password
  tls: ""                          # Empty for no TLS (local network)
  device_id: "living_room_frame"    # Unique identifier
  device_url: "http://192.168.1.100:9000"  # PicFrame web interface URL

# Optional: Enable HTTP interface for web control
http:
  use_http: True
  port: 9000
  auth: true
  username: "admin"
  password: null                    # Auto-generate password
```

#### Create MQTT User in Home Assistant

1. **Using Mosquitto Add-on**:
   - Go to Settings > Add-ons > Mosquitto broker
   - Click "Configuration" tab
   - Add user credentials:
     ```yaml
     logins:
       - username: picframe_user
         password: your_secure_password
     ```

2. **Restart Mosquitto broker** after configuration changes.

### Step 3: Start PicFrame and Verify Discovery

#### Launch PicFrame
```bash
# Activate virtual environment
source ~/picframe-env/bin/activate

# Start PicFrame
picframe ~/picframe_data/config/configuration.yaml
```

#### Verify Home Assistant Discovery

1. **Check MQTT Topics**:
   - Go to Developer Tools > MQTT
   - Listen to topic: `homeassistant/+/picframe_living_room_frame/+`
   - You should see discovery messages

2. **Find PicFrame Entities**:
   - Go to Settings > Devices & Services > MQTT
   - Look for "PicFrame living_room_frame" device
   - Entities should include:
     - Switch: Display On/Off
     - Sensor: Current Image Info
     - Camera: Current Image Preview

### Step 4: Create Home Assistant Dashboard

#### Basic PicFrame Card
```yaml
# Add to your dashboard (Lovelace UI)
type: entities
title: Living Room Picture Frame
entities:
  - entity: switch.picframe_living_room_frame_display
    name: Display Power
  - entity: switch.picframe_living_room_frame_paused
    name: Slideshow Paused
  - entity: sensor.picframe_living_room_frame_image
    name: Current Image
  - entity: sensor.picframe_living_room_frame_location
    name: Image Location
```

#### Advanced Picture Frame Card
```yaml
type: vertical-stack
cards:
  - type: picture-entity
    entity: camera.picframe_living_room_frame_image
    name: Current Image
    tap_action:
      action: call-service
      service: mqtt.publish
      service_data:
        topic: picframe/living_room_frame/command
        payload: "next"
    
  - type: horizontal-stack
    cards:
      - type: button
        entity: switch.picframe_living_room_frame_display
        name: Power
        icon: mdi:power
        
      - type: button
        tap_action:
          action: call-service
          service: mqtt.publish
          service_data:
            topic: picframe/living_room_frame/command
            payload: "previous"
        icon: mdi:skip-previous
        name: Previous
        
      - type: button
        entity: switch.picframe_living_room_frame_paused
        name: Pause
        icon: mdi:pause
        
      - type: button
        tap_action:
          action: call-service
          service: mqtt.publish
          service_data:
            topic: picframe/living_room_frame/command
            payload: "next"
        icon: mdi:skip-next
        name: Next
        
  - type: entities
    entities:
      - entity: sensor.picframe_living_room_frame_image
        name: Current Image
      - entity: sensor.picframe_living_room_frame_location
        name: Location
      - entity: sensor.picframe_living_room_frame_date
        name: Date Taken
```

### Step 5: Create Automations

#### Automatic Display Control
```yaml
# automation.yaml
- id: picframe_morning_on
  alias: "PicFrame: Turn on in morning"
  trigger:
    - platform: time
      at: "07:00:00"
  condition:
    - condition: state
      entity_id: binary_sensor.workday_sensor
      state: 'on'
  action:
    - service: switch.turn_on
      entity_id: switch.picframe_living_room_frame_display

- id: picframe_night_off
  alias: "PicFrame: Turn off at night"
  trigger:
    - platform: time
      at: "23:00:00"
  action:
    - service: switch.turn_off
      entity_id: switch.picframe_living_room_frame_display
```

#### Motion-Based Control
```yaml
- id: picframe_motion_control
  alias: "PicFrame: Motion-based display control"
  trigger:
    - platform: state
      entity_id: binary_sensor.living_room_motion
      to: 'on'
  condition:
    - condition: sun
      after: sunrise
      before: sunset
  action:
    - service: switch.turn_on
      entity_id: switch.picframe_living_room_frame_display
    - delay: '00:30:00'  # Keep on for 30 minutes
    - service: switch.turn_off
      entity_id: switch.picframe_living_room_frame_display
```

#### Guest Mode Automation
```yaml
- id: picframe_guest_mode
  alias: "PicFrame: Guest mode slideshow"
  trigger:
    - platform: state
      entity_id: input_boolean.guest_mode
      to: 'on'
  action:
    - service: mqtt.publish
      data:
        topic: picframe/living_room_frame/command
        payload: '{"subdirectory": "guests", "time_delay": 60}'
    - service: switch.turn_on
      entity_id: switch.picframe_living_room_frame_display
```

## MQTT Broker Setup

### Installing Mosquitto MQTT Broker

#### On Raspberry Pi / Debian / Ubuntu
```bash
# Update package lists
sudo apt update

# Install Mosquitto broker and clients
sudo apt install mosquitto mosquitto-clients

# Enable and start the service
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

#### On Docker
```bash
# Create mosquitto configuration directory
mkdir -p ~/mosquitto/config
mkdir -p ~/mosquitto/data
mkdir -p ~/mosquitto/log

# Create basic configuration
cat > ~/mosquitto/config/mosquitto.conf << EOF
persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log
log_dest stdout

# Allow anonymous connections (for testing only)
allow_anonymous true

# Standard MQTT port
listener 1883

# WebSocket support (optional)
listener 9001
protocol websockets
EOF

# Run Mosquitto in Docker
docker run -it -p 1883:1883 -p 9001:9001 \
  -v ~/mosquitto/config:/mosquitto/config \
  -v ~/mosquitto/data:/mosquitto/data \
  -v ~/mosquitto/log:/mosquitto/log \
  eclipse-mosquitto
```

### Configuring MQTT Security

#### Create User Authentication
```bash
# Create password file
sudo mosquitto_passwd -c /etc/mosquitto/passwd picframe_user

# Add additional users
sudo mosquitto_passwd /etc/mosquitto/passwd homeassistant_user
```

#### Configure Mosquitto with Authentication
```bash
# Edit mosquitto configuration
sudo nano /etc/mosquitto/mosquitto.conf
```

Add the following configuration:
```
# Disable anonymous access
allow_anonymous false

# Password file location
password_file /etc/mosquitto/passwd

# Access control list (optional)
acl_file /etc/mosquitto/acl

# Standard MQTT port
listener 1883

# Logging
log_dest file /var/log/mosquitto/mosquitto.log
log_type error
log_type warning
log_type notice
log_type information
```

#### Create Access Control List (Optional)
```bash
# Create ACL file
sudo nano /etc/mosquitto/acl
```

Add access rules:
```
# PicFrame user permissions
user picframe_user
topic readwrite picframe/+/+
topic readwrite homeassistant/+/picframe_+/+

# Home Assistant user permissions
user homeassistant_user
topic readwrite #
```

#### Restart Mosquitto
```bash
sudo systemctl restart mosquitto
sudo systemctl status mosquitto
```

### Testing MQTT Connection

#### Test with Command Line Tools
```bash
# Subscribe to PicFrame topics
mosquitto_sub -h localhost -u picframe_user -P your_password -t "picframe/+/+"

# Publish test command
mosquitto_pub -h localhost -u picframe_user -P your_password \
  -t "picframe/living_room_frame/command" -m "next"
```

#### Test PicFrame MQTT Connection
```bash
# Enable debug logging in PicFrame
# Edit configuration.yaml:
model:
  log_level: "DEBUG"
  log_file: "/tmp/picframe_mqtt.log"

# Start PicFrame and check logs
tail -f /tmp/picframe_mqtt.log
```

### MQTT Topic Structure

PicFrame uses the following MQTT topic structure:

#### Command Topics (Subscribe)
```
picframe/[device_id]/command          # General commands
picframe/[device_id]/set_config       # Configuration updates
picframe/[device_id]/display/set      # Display control
```

#### Status Topics (Publish)
```
picframe/[device_id]/status           # General status
picframe/[device_id]/image            # Current image info
picframe/[device_id]/display          # Display state
picframe/[device_id]/config           # Current configuration
```

#### Home Assistant Discovery Topics
```
homeassistant/switch/picframe_[device_id]/display/config
homeassistant/sensor/picframe_[device_id]/image/config
homeassistant/camera/picframe_[device_id]/image/config
```

## Custom Automation Scenarios

### Scenario 1: Weather-Based Slideshow

Display different image collections based on weather conditions.

#### Home Assistant Configuration
```yaml
# configuration.yaml
sensor:
  - platform: openweathermap
    api_key: YOUR_API_KEY
    monitored_conditions:
      - weather
      - temperature

automation:
  - id: picframe_weather_slideshow
    alias: "PicFrame: Weather-based slideshow"
    trigger:
      - platform: state
        entity_id: weather.openweathermap
    action:
      - choose:
          - conditions:
              - condition: state
                entity_id: weather.openweathermap
                state: 'sunny'
            sequence:
              - service: mqtt.publish
                data:
                  topic: picframe/living_room_frame/command
                  payload: '{"subdirectory": "summer_sunny", "time_delay": 180}'
          
          - conditions:
              - condition: state
                entity_id: weather.openweathermap
                state: 'rainy'
            sequence:
              - service: mqtt.publish
                data:
                  topic: picframe/living_room_frame/command
                  payload: '{"subdirectory": "cozy_indoor", "time_delay": 300}'
        
        default:
          - service: mqtt.publish
            data:
              topic: picframe/living_room_frame/command
              payload: '{"subdirectory": "", "time_delay": 200}'
```

### Scenario 2: Presence-Based Display Management

Control PicFrame based on home occupancy and room presence.

#### Configuration
```yaml
# Binary sensor for room occupancy
binary_sensor:
  - platform: template
    sensors:
      living_room_occupied:
        friendly_name: "Living Room Occupied"
        value_template: >
          {{ is_state('binary_sensor.living_room_motion', 'on') or
             is_state('media_player.living_room_tv', 'on') or
             is_state('light.living_room_main', 'on') }}
        delay_off:
          minutes: 15

automation:
  # Turn on display when room is occupied
  - id: picframe_presence_on
    alias: "PicFrame: Turn on when room occupied"
    trigger:
      - platform: state
        entity_id: binary_sensor.living_room_occupied
        to: 'on'
    condition:
      - condition: state
        entity_id: binary_sensor.home_occupied
        state: 'on'
    action:
      - service: switch.turn_on
        entity_id: switch.picframe_living_room_frame_display
      - service: mqtt.publish
        data:
          topic: picframe/living_room_frame/command
          payload: 'resume'

  # Turn off display when room is empty
  - id: picframe_presence_off
    alias: "PicFrame: Turn off when room empty"
    trigger:
      - platform: state
        entity_id: binary_sensor.living_room_occupied
        to: 'off'
        for:
          minutes: 30
    action:
      - service: switch.turn_off
        entity_id: switch.picframe_living_room_frame_display
```

### Scenario 3: Time-Based Content Rotation

Display different content based on time of day and day of week.

#### Advanced Time-Based Automation
```yaml
automation:
  - id: picframe_morning_routine
    alias: "PicFrame: Morning family photos"
    trigger:
      - platform: time
        at: "07:00:00"
    condition:
      - condition: state
        entity_id: binary_sensor.workday_sensor
        state: 'on'
    action:
      - service: mqtt.publish
        data:
          topic: picframe/living_room_frame/command
          payload: >
            {
              "subdirectory": "family_recent",
              "time_delay": 120,
              "show_text": "date location",
              "show_clock": true
            }

  - id: picframe_evening_memories
    alias: "PicFrame: Evening memory slideshow"
    trigger:
      - platform: time
        at: "19:00:00"
    action:
      - service: mqtt.publish
        data:
          topic: picframe/living_room_frame/command
          payload: >
            {
              "subdirectory": "memories",
              "time_delay": 300,
              "show_text": "title caption date location",
              "shuffle": true
            }

  - id: picframe_weekend_mode
    alias: "PicFrame: Weekend relaxed mode"
    trigger:
      - platform: time
        at: "09:00:00"
    condition:
      - condition: state
        entity_id: binary_sensor.workday_sensor
        state: 'off'
    action:
      - service: mqtt.publish
        data:
          topic: picframe/living_room_frame/command
          payload: >
            {
              "time_delay": 600,
              "kenburns": true,
              "show_text": "title caption location"
            }
```

### Scenario 4: Smart Home Event Integration

Integrate PicFrame with various smart home events and notifications.

#### Event-Driven Automations
```yaml
automation:
  # Doorbell integration
  - id: picframe_doorbell_pause
    alias: "PicFrame: Pause on doorbell"
    trigger:
      - platform: state
        entity_id: binary_sensor.front_door_bell
        to: 'on'
    action:
      - service: mqtt.publish
        data:
          topic: picframe/living_room_frame/command
          payload: 'pause'
      - delay: '00:02:00'
      - service: mqtt.publish
        data:
          topic: picframe/living_room_frame/command
          payload: 'resume'

  # Security system integration
  - id: picframe_security_mode
    alias: "PicFrame: Security mode display"
    trigger:
      - platform: state
        entity_id: alarm_control_panel.home_security
        to: 'armed_away'
    action:
      - service: switch.turn_off
        entity_id: switch.picframe_living_room_frame_display
      - service: mqtt.publish
        data:
          topic: picframe/living_room_frame/command
          payload: '{"subdirectory": "security_images"}'

  # Party mode
  - id: picframe_party_mode
    alias: "PicFrame: Party mode activation"
    trigger:
      - platform: state
        entity_id: input_boolean.party_mode
        to: 'on'
    action:
      - service: mqtt.publish
        data:
          topic: picframe/living_room_frame/command
          payload: >
            {
              "subdirectory": "party_photos",
              "time_delay": 30,
              "shuffle": true,
              "show_text": "",
              "kenburns": true
            }
```

### Scenario 5: Voice Control Integration

Integrate PicFrame with voice assistants for hands-free control.

#### Alexa/Google Assistant via Home Assistant
```yaml
# configuration.yaml
intent_script:
  PicFrameNext:
    speech:
      text: "Showing next image"
    action:
      - service: mqtt.publish
        data:
          topic: picframe/living_room_frame/command
          payload: 'next'

  PicFramePrevious:
    speech:
      text: "Showing previous image"
    action:
      - service: mqtt.publish
        data:
          topic: picframe/living_room_frame/command
          payload: 'previous'

  PicFramePause:
    speech:
      text: "Pausing slideshow"
    action:
      - service: switch.turn_off
        entity_id: switch.picframe_living_room_frame_paused

  PicFrameResume:
    speech:
      text: "Resuming slideshow"
    action:
      - service: switch.turn_on
        entity_id: switch.picframe_living_room_frame_paused

# Alexa integration
alexa:
  smart_home:
    filter:
      include_entities:
        - switch.picframe_living_room_frame_display
        - switch.picframe_living_room_frame_paused
```

## Advanced Integration Examples

### Multi-Room PicFrame Coordination

Coordinate multiple PicFrame devices across different rooms.

#### Configuration for Multiple Devices
```yaml
# Device 1: Living Room
mqtt:
  device_id: "living_room_frame"
  
# Device 2: Kitchen  
mqtt:
  device_id: "kitchen_frame"

# Device 3: Bedroom
mqtt:
  device_id: "bedroom_frame"
```

#### Synchronized Control Automation
```yaml
automation:
  - id: picframe_sync_all
    alias: "PicFrame: Synchronize all frames"
    trigger:
      - platform: state
        entity_id: input_boolean.sync_all_frames
        to: 'on'
    action:
      - service: mqtt.publish
        data:
          topic: picframe/+/command
          payload: 'sync'
      - delay: '00:00:02'
      - service: input_boolean.turn_off
        entity_id: input_boolean.sync_all_frames

  - id: picframe_bedtime_routine
    alias: "PicFrame: Bedtime routine"
    trigger:
      - platform: time
        at: "22:00:00"
    action:
      # Turn off living room and kitchen frames
      - service: switch.turn_off
        entity_id: 
          - switch.picframe_living_room_frame_display
          - switch.picframe_kitchen_frame_display
      # Switch bedroom frame to night mode
      - service: mqtt.publish
        data:
          topic: picframe/bedroom_frame/command
          payload: >
            {
              "subdirectory": "peaceful_scenes",
              "time_delay": 900,
              "show_clock": true,
              "clock_format": "%-I:%M"
            }
```

### Integration with Photo Management Systems

#### Nextcloud Integration
```bash
#!/bin/bash
# sync_nextcloud_photos.sh
# Sync photos from Nextcloud to PicFrame

NEXTCLOUD_URL="https://your-nextcloud.com"
NEXTCLOUD_USER="your-username"
NEXTCLOUD_PASS="your-app-password"
LOCAL_DIR="$HOME/Pictures/nextcloud_sync"

# Sync photos using WebDAV
rclone sync nextcloud:Photos "$LOCAL_DIR" \
  --include "*.{jpg,jpeg,png,heic,heif}" \
  --max-age 30d

# Notify PicFrame to rescan
mosquitto_pub -h localhost -u picframe_user -P your_password \
  -t "picframe/living_room_frame/command" -m "rescan"
```

#### Google Photos Integration
```python
#!/usr/bin/env python3
# google_photos_sync.py
import os
import requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def sync_google_photos():
    # Google Photos API integration
    # (Requires Google Photos API credentials)
    
    SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
    
    # Authentication and photo download logic
    # Download recent photos to PicFrame directory
    
    # Notify PicFrame via MQTT
    import paho.mqtt.client as mqtt
    
    client = mqtt.Client()
    client.username_pw_set("picframe_user", "your_password")
    client.connect("localhost", 1883, 60)
    client.publish("picframe/living_room_frame/command", "rescan")
    client.disconnect()

if __name__ == "__main__":
    sync_google_photos()
```

### Custom MQTT Commands

#### Extended Command Set
```python
# custom_picframe_commands.py
import paho.mqtt.client as mqtt
import json
import time

class PicFrameController:
    def __init__(self, broker_host, username, password, device_id):
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)
        self.client.connect(broker_host, 1883, 60)
        self.device_id = device_id
        self.command_topic = f"picframe/{device_id}/command"
    
    def set_slideshow_speed(self, speed_preset):
        """Set slideshow speed using presets"""
        speeds = {
            'slow': 600,      # 10 minutes
            'normal': 200,    # 3.3 minutes  
            'fast': 60,       # 1 minute
            'rapid': 15       # 15 seconds
        }
        
        command = json.dumps({
            "time_delay": speeds.get(speed_preset, 200)
        })
        self.client.publish(self.command_topic, command)
    
    def set_mood_lighting(self, mood):
        """Change display settings based on mood"""
        moods = {
            'energetic': {
                'time_delay': 30,
                'kenburns': True,
                'show_text': '',
                'subdirectory': 'action_photos'
            },
            'relaxing': {
                'time_delay': 300,
                'kenburns': False,
                'show_text': 'location',
                'subdirectory': 'nature_scenes'
            },
            'romantic': {
                'time_delay': 180,
                'show_text': 'title date',
                'subdirectory': 'couple_photos'
            }
        }
        
        if mood in moods:
            command = json.dumps(moods[mood])
            self.client.publish(self.command_topic, command)
    
    def schedule_slideshow(self, start_time, end_time, config):
        """Schedule a specific slideshow configuration"""
        # Implementation for scheduled configurations
        pass

# Usage example
controller = PicFrameController(
    "homeassistant.local", 
    "picframe_user", 
    "your_password", 
    "living_room_frame"
)

controller.set_slideshow_speed('fast')
controller.set_mood_lighting('relaxing')
```

## Troubleshooting Integrations

### Common MQTT Issues

#### Connection Problems
```bash
# Test MQTT broker connectivity
mosquitto_pub -h your_broker_ip -p 1883 -t test/topic -m "test message"

# Check if broker is running
sudo systemctl status mosquitto

# Check broker logs
sudo journalctl -u mosquitto -f
```

#### Authentication Issues
```bash
# Test with credentials
mosquitto_pub -h localhost -u picframe_user -P your_password \
  -t test/topic -m "authenticated test"

# Check password file
sudo cat /etc/mosquitto/passwd
```

#### Topic Permission Issues
```bash
# Check ACL configuration
sudo cat /etc/mosquitto/acl

# Test specific topic access
mosquitto_pub -h localhost -u picframe_user -P your_password \
  -t picframe/test_device/command -m "test"
```

### Home Assistant Discovery Issues

#### Discovery Not Working
1. **Check MQTT Integration**: Ensure MQTT is properly configured in Home Assistant
2. **Verify Topic Structure**: Check that discovery topics follow the correct format
3. **Check Device ID**: Ensure device_id is unique and valid
4. **Restart Services**: Restart both PicFrame and Home Assistant

#### Entities Not Appearing
```bash
# Check Home Assistant logs
tail -f /config/home-assistant.log | grep -i mqtt

# Verify discovery messages
mosquitto_sub -h localhost -u homeassistant_user -P your_password \
  -t "homeassistant/+/picframe_+/+"
```

### Performance Issues

#### MQTT Message Flooding
```yaml
# Reduce update frequency in PicFrame config
model:
  update_interval: 10.0  # Increase from default 2.0
```

#### Network Latency
```bash
# Test network latency to MQTT broker
ping your_mqtt_broker_ip

# Check MQTT message timing
mosquitto_sub -h localhost -u picframe_user -P your_password \
  -t "picframe/+/+" -v | while read line; do
    echo "$(date): $line"
  done
```

### Integration Testing

#### End-to-End Test Script
```bash
#!/bin/bash
# test_picframe_integration.sh

BROKER="localhost"
USER="picframe_user"
PASS="your_password"
DEVICE="test_frame"

echo "Testing PicFrame MQTT Integration..."

# Test 1: Basic connectivity
echo "1. Testing MQTT connectivity..."
mosquitto_pub -h $BROKER -u $USER -P $PASS -t test/connectivity -m "test" && echo "✓ Connected" || echo "✗ Connection failed"

# Test 2: Command publishing
echo "2. Testing command publishing..."
mosquitto_pub -h $BROKER -u $USER -P $PASS -t picframe/$DEVICE/command -m "next" && echo "✓ Command sent" || echo "✗ Command failed"

# Test 3: Status subscription
echo "3. Testing status subscription..."
timeout 5 mosquitto_sub -h $BROKER -u $USER -P $PASS -t picframe/$DEVICE/status -C 1 && echo "✓ Status received" || echo "✗ No status received"

# Test 4: Home Assistant discovery
echo "4. Testing HA discovery..."
timeout 5 mosquitto_sub -h $BROKER -u $USER -P $PASS -t homeassistant/+/picframe_$DEVICE/+ -C 1 && echo "✓ Discovery working" || echo "✗ No discovery messages"

echo "Integration test complete."
```

For additional troubleshooting help, consult the [PicFrame GitHub Issues](https://github.com/helgeerbe/picframe/issues) or the Home Assistant community forums.