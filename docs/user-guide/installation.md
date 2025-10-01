# PicFrame Installation Guide

This guide provides step-by-step installation instructions for PicFrame on different platforms, including dependency installation, configuration, and troubleshooting for common issues.

## Table of Contents

- [System Requirements](#system-requirements)
- [Platform-Specific Installation](#platform-specific-installation)
  - [Raspberry Pi (Recommended)](#raspberry-pi-recommended)
  - [Ubuntu/Debian](#ubuntudebian)
  - [Other Linux Distributions](#other-linux-distributions)
- [Dependency Installation](#dependency-installation)
- [Initial Setup](#initial-setup)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **Operating System**: Linux-based system (Raspberry Pi OS, Ubuntu 20.04+, Debian 10+)
- **Python**: Python 3.7 or higher
- **Memory**: 1GB RAM minimum (2GB+ recommended for 4K displays)
- **Storage**: 500MB free space for application + space for your image collection
- **Display**: Any display supported by your system (HDMI, DSI, etc.)

### Recommended Hardware
- **Raspberry Pi 4B** with 4GB+ RAM for optimal performance
- **High-speed SD card** (Class 10 or better) for Raspberry Pi installations
- **Dedicated GPU** for hardware acceleration (optional but recommended)

### Required System Libraries
The following system libraries must be installed before PicFrame:
- OpenGL ES 2.0 support
- SDL2 development libraries
- Image processing libraries (libjpeg, libpng, libtiff)
- Video codec libraries (for video support)

## Platform-Specific Installation

### Raspberry Pi (Recommended)

PicFrame is optimized for Raspberry Pi and provides the best experience on this platform.

#### Step 1: Update System
```bash
sudo apt update
sudo apt upgrade -y
```

#### Step 2: Install System Dependencies
```bash
# Essential system packages
sudo apt install -y python3 python3-pip python3-venv git

# Graphics and multimedia libraries
sudo apt install -y libgl1-mesa-dev libgles2-mesa-dev
sudo apt install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

# Image processing libraries
sudo apt install -y libjpeg-dev libpng-dev libtiff-dev libwebp-dev
sudo apt install -y libopenjp2-7-dev liblcms2-dev libfreetype6-dev

# Video support libraries
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev
sudo apt install -y vlc-bin vlc-plugin-base

# Optional: Hardware acceleration (for Pi 4)
sudo apt install -y libdrm-dev libgbm-dev
```

#### Step 3: Enable GPU Memory Split (Raspberry Pi)
```bash
# Allocate more memory to GPU for better graphics performance
sudo raspi-config
# Navigate to: Advanced Options > Memory Split > Set to 128 or 256
# Or edit directly:
echo 'gpu_mem=128' | sudo tee -a /boot/config.txt
```

#### Step 4: Install PicFrame
```bash
# Create virtual environment (recommended)
python3 -m venv ~/picframe-env
source ~/picframe-env/bin/activate

# Install PicFrame
pip install picframe

# Or install from source for latest features
git clone https://github.com/helgeerbe/picframe.git
cd picframe
pip install -e .
```

### Ubuntu/Debian

#### Step 1: Update Package Lists
```bash
sudo apt update
```

#### Step 2: Install System Dependencies
```bash
# Python and development tools
sudo apt install -y python3 python3-pip python3-venv build-essential

# Graphics libraries
sudo apt install -y libgl1-mesa-dev libgles2-mesa-dev
sudo apt install -y libsdl2-dev libsdl2-image-dev

# Image processing
sudo apt install -y libjpeg-dev libpng-dev libtiff-dev
sudo apt install -y libfreetype6-dev liblcms2-dev libwebp-dev

# Video support
sudo apt install -y vlc-bin libvlc-dev
sudo apt install -y libavcodec-dev libavformat-dev

# X11 support (if using desktop environment)
sudo apt install -y libx11-dev libxext-dev
```

#### Step 3: Install PicFrame
```bash
# Create and activate virtual environment
python3 -m venv ~/picframe-env
source ~/picframe-env/bin/activate

# Install PicFrame
pip install picframe
```

### Other Linux Distributions

#### Fedora/CentOS/RHEL
```bash
# Install system dependencies
sudo dnf install -y python3 python3-pip python3-virtualenv
sudo dnf install -y mesa-libGL-devel mesa-libGLES-devel
sudo dnf install -y SDL2-devel libjpeg-turbo-devel libpng-devel
sudo dnf install -y freetype-devel vlc-devel

# Create virtual environment and install
python3 -m venv ~/picframe-env
source ~/picframe-env/bin/activate
pip install picframe
```

#### Arch Linux
```bash
# Install system dependencies
sudo pacman -S python python-pip python-virtualenv
sudo pacman -S mesa sdl2 libjpeg-turbo libpng freetype2
sudo pacman -S vlc opencv

# Create virtual environment and install
python3 -m venv ~/picframe-env
source ~/picframe-env/bin/activate
pip install picframe
```

## Dependency Installation

### Python Dependencies

PicFrame automatically installs the following Python packages:

- **Pillow (>=10.2.0)**: Image processing and manipulation
- **pi3d (>=2.54)**: 3D graphics engine for display rendering
- **PyYAML**: Configuration file parsing
- **paho-mqtt (>=2.1.0)**: MQTT client for smart home integration
- **IPTCInfo3**: IPTC metadata extraction from images
- **numpy**: Numerical computing for image operations
- **ninepatch (>=0.2.0)**: Nine-patch image processing for matting
- **pi_heif (>=0.8.0)**: HEIF/HEIC image format support
- **python-vlc**: Video playback support
- **opencv-python**: Computer vision and image processing
- **defusedxml**: Secure XML parsing

### Verifying Dependencies

After installation, verify all dependencies are correctly installed:

```bash
# Activate your virtual environment
source ~/picframe-env/bin/activate

# Check PicFrame version and dependencies
picframe -v
```

This command will display the PicFrame version and check all required packages.

## Initial Setup

### Step 1: Initialize PicFrame Directory Structure

```bash
# Activate virtual environment
source ~/picframe-env/bin/activate

# Initialize PicFrame in your home directory
picframe -i ~

# This creates ~/picframe_data/ with the following structure:
# ~/picframe_data/
# ├── config/
# │   ├── configuration.yaml
# │   └── configuration_example.yaml
# ├── data/
# │   ├── fonts/
# │   ├── mat/
# │   ├── shaders/
# │   └── pictureframe.db3
# └── html/
#     ├── index.html
#     └── pf_functions.js
```

### Step 2: Configure Your Picture Directory

During initialization, you'll be prompted to configure:

1. **Picture Directory**: Where your images are stored (default: `~/Pictures`)
2. **Deleted Pictures Directory**: Where deleted images are moved (default: `~/DeletedPictures`)
3. **Locale**: System locale for date formatting (auto-detected)

Example initialization session:
```
This will configure /home/user/picframe_data/config/configuration.yaml
To keep default, just hit enter
Enter picture directory [~/Pictures]: /media/photos
Enter picture directory [~/DeletedPictures]: /media/deleted
Enter locale [en_US.utf8]: 
```

### Step 3: Create Picture Directories

```bash
# Create your picture directories
mkdir -p ~/Pictures
mkdir -p ~/DeletedPictures

# Or use custom paths you specified during setup
mkdir -p /media/photos
mkdir -p /media/deleted
```

### Step 4: Add Some Test Images

```bash
# Copy some test images to your picture directory
cp /path/to/your/images/* ~/Pictures/

# Or create a test subdirectory
mkdir ~/Pictures/test
cp /path/to/test/images/* ~/Pictures/test/
```

## Verification

### Test Installation

1. **Check PicFrame Version**:
   ```bash
   source ~/picframe-env/bin/activate
   picframe -v
   ```

2. **Verify Configuration**:
   ```bash
   # Check that configuration file was created
   ls -la ~/picframe_data/config/
   cat ~/picframe_data/config/configuration.yaml
   ```

3. **Test Run (Dry Run)**:
   ```bash
   # Test configuration without starting display
   python3 -c "from picframe import model; m = model.Model('~/picframe_data/config/configuration.yaml'); print('Configuration loaded successfully')"
   ```

### First Run

```bash
# Activate virtual environment
source ~/picframe-env/bin/activate

# Start PicFrame with default configuration
picframe

# Or specify custom configuration
picframe ~/picframe_data/config/configuration.yaml
```

**Expected Behavior**:
- PicFrame should start and begin scanning your picture directory
- Images should appear on the display with smooth transitions
- Check the console output for any error messages

## Troubleshooting

### Common Installation Issues

#### 1. Permission Denied Errors

**Problem**: Permission errors during installation or file creation.

**Solution**:
```bash
# Don't use sudo with pip in virtual environments
# Instead, ensure proper ownership:
sudo chown -R $USER:$USER ~/picframe-env
sudo chown -R $USER:$USER ~/picframe_data

# For system-wide installation issues:
sudo apt install --fix-missing
```

#### 2. SDL2 Library Not Found

**Problem**: `ImportError: libSDL2-2.0.so.0: cannot open shared object file`

**Solution**:
```bash
# Ubuntu/Debian:
sudo apt install libsdl2-2.0-0 libsdl2-dev

# Fedora:
sudo dnf install SDL2 SDL2-devel

# Check library path:
ldconfig -p | grep SDL2
```

#### 3. OpenGL/Graphics Issues

**Problem**: Graphics initialization fails or black screen.

**Solution**:
```bash
# Check OpenGL support:
glxinfo | grep "OpenGL version"

# For Raspberry Pi, ensure GPU memory split:
sudo raspi-config
# Advanced Options > Memory Split > 128

# Check display configuration:
echo $DISPLAY
export DISPLAY=:0.0  # if needed
```

#### 4. Python Version Issues

**Problem**: `python3: command not found` or version conflicts.

**Solution**:
```bash
# Check Python version:
python3 --version

# Install Python 3.7+ if needed:
sudo apt install python3.8 python3.8-venv python3.8-pip

# Use specific Python version:
python3.8 -m venv ~/picframe-env
```

#### 5. Virtual Environment Issues

**Problem**: Cannot activate virtual environment or import errors.

**Solution**:
```bash
# Recreate virtual environment:
rm -rf ~/picframe-env
python3 -m venv ~/picframe-env
source ~/picframe-env/bin/activate

# Upgrade pip and reinstall:
pip install --upgrade pip setuptools wheel
pip install picframe
```

#### 6. Image Loading Issues

**Problem**: Images not displaying or format not supported.

**Solution**:
```bash
# Check image formats in your directory:
file ~/Pictures/*

# Install additional image format support:
pip install pillow-heif  # for HEIF/HEIC
sudo apt install libwebp-dev  # for WebP

# Check image permissions:
ls -la ~/Pictures/
chmod 644 ~/Pictures/*
```

#### 7. Database Issues

**Problem**: SQLite database errors or corruption.

**Solution**:
```bash
# Remove and recreate database:
rm ~/picframe_data/data/pictureframe.db3

# PicFrame will recreate it on next run
picframe
```

#### 8. Memory Issues

**Problem**: Out of memory errors or system freezing.

**Solution**:
```bash
# Check memory usage:
free -h

# Reduce image cache size in configuration:
# Edit ~/picframe_data/config/configuration.yaml
# Reduce blur_amount, display resolution, or enable fit mode

# For Raspberry Pi, increase swap:
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile  # Set CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### Getting Help

If you encounter issues not covered here:

1. **Check the logs**: Look for error messages in the console output
2. **Verify configuration**: Ensure your `configuration.yaml` is valid YAML
3. **Test with minimal setup**: Try with a small number of images first
4. **Check system resources**: Monitor CPU, memory, and disk usage
5. **Community support**: Visit the [PicFrame GitHub repository](https://github.com/helgeerbe/picframe) for issues and discussions

### Performance Optimization

For optimal performance:

1. **Use high-speed storage**: Class 10+ SD cards for Raspberry Pi
2. **Optimize images**: Resize large images to your display resolution
3. **Adjust configuration**: Tune `blur_amount`, `fps`, and cache settings
4. **Monitor resources**: Use `htop` to monitor system performance
5. **Regular maintenance**: Periodically clean up logs and temporary files

## Next Steps

After successful installation:

1. **Configure PicFrame**: See the [Configuration Guide](configuration.md)
2. **Set up integrations**: Follow the [Integration Tutorials](integrations.md)
3. **Customize display**: Explore display options and effects
4. **Automate startup**: Set up PicFrame to start automatically on boot

For detailed configuration options, see the [Configuration Reference](configuration.md).