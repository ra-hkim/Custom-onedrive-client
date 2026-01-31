# Custom OneDrive Client

A lightweight OneDrive client with system tray integration.

## Requirements

- Python 3.7+
- rclone

## Installation

### 1. Install Python Dependencies
```bash
pip install pystray pillow
```

### 2. Install rclone

**Windows:**
```bash
winget install rclone
```

**Fedora:**
```bash
sudo dnf install rclone
```

## Setup

### 1. Configure rclone
Run the interactive rclone configuration:
```bash
rclone config
```

Follow the prompts to set up your OneDrive remote storage.
### 2.1 Run the Application via Python
Download ["Ondrive.py"](/Ondrive.py) and ["icon.ico"](/icon.ico)
```bash
python Ondrive.py
```
### 2.2 Use the Application via EXE
Download ["Ondrive.exe"](dist/Ondrive.exe) from the "dist" folder


The application will run in your system tray.
