# DIY PC Control Panel

A lightweight Python Flask application to control a Windows PC from a local network device (like a Raspberry Pi or Smartphone).

## Features
- **Remote Sleep:** Put the PC to sleep with one click.
- **Screen Sharing:** Low-latency MJPEG stream of the PC screen.
- **File Browser:** Browse drives (D:, E:, etc.) and view Images/Videos remotely.
- **Security:** Blocks access to C: drive by default.

## Requirements
- Windows 10/11
- Python 3.8+

## Installation

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt