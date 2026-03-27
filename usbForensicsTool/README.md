# USB Forensics Tool

A comprehensive USB forensics toolkit for device enumeration, log analysis, memory dump analysis, and real-time USB monitoring.

## Features

- **USB Device Enumeration**: List all connected USB devices with vendor/product IDs, serial numbers, and manufacturer info
- **Log Analysis**: Parse system logs for USB-related events
- **Memory Analysis**: Analyze memory dumps using Volatility3 framework
- **Suspicious Activity Detection**: Identify potentially malicious USB activity
- **Forensic Reporting**: Generate CSV reports of findings
- **Real-time Monitoring**: GUI tools for monitoring USB connections (Linux and macOS)

## Installation

### Prerequisites

- Python 3.8+
- libusb (for USB device access)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### System Dependencies

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install libusb-1.0-0-dev

# Fedora/RHEL
sudo dnf install libusb-devel
```

**macOS:**
```bash
brew install libusb
```

## Usage

### Main Forensics Tool

```bash
# List connected USB devices
python3 UsbForensics.py --list-devices

# Analyze system logs (default: /var/log/syslog)
python3 UsbForensics.py --log-file /var/log/syslog

# Analyze a memory dump
python3 UsbForensics.py --memory-file memory.dmp

# Full analysis with custom output
python3 UsbForensics.py --list-devices --log-file /var/log/syslog --output report.csv

# Exclude known vendors from suspicious detection
python3 UsbForensics.py --log-file /var/log/syslog --known-vendors 0x8087 0x046d
```

#### Command Line Options

| Option | Description |
|--------|-------------|
| `--list-devices`, `-l` | List connected USB devices |
| `--log-file`, `-f` | Path to system log file |
| `--memory-file`, `-m` | Path to memory dump file |
| `--output`, `-o` | Output file for report (default: usb_forensics_report.csv) |
| `--known-vendors`, `-k` | List of known/safe vendor IDs to exclude |

### USB Port Monitor (Linux)

Real-time USB device monitoring for Linux systems using pyudev.

```bash
python3 usb_monitor_linux.py
```

**Features:**
- Auto-refresh every second
- Shows device path, node, vendor, model, and serial
- Clean exit on window close

### USB Port Monitor (macOS)

Real-time USB device monitoring for macOS using IOKit.

```bash
python3 usb_monitor_macos.py
```

**Features:**
- Auto-refresh every second
- Shows device name and vendor/product IDs
- Proper memory management for IOKit objects

## Project Structure

```
usbForensicsTool/
├── UsbForensics.py       # Main forensics tool
├── usb_monitor_linux.py  # Linux USB monitor GUI (pyudev)
├── usb_monitor_macos.py  # macOS USB monitor GUI (IOKit)
├── requirements.txt      # Python dependencies
├── __init__.py           # Package initialization
└── README.md             # This file
```

## Output Format

The forensic report is generated as a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| Type | Category of suspicious activity (suspicious_pattern, unknown_vendor, general) |
| Event | The full log event text |

## Detection Patterns

The tool detects suspicious activity based on:

1. **Suspicious Keywords**: unauthorized, failed, error, disconnect, reset, overflow, malicious, infection, virus
2. **Unknown Vendors**: Vendor IDs not in the known/safe list

## Troubleshooting

### "No USB backend found"
Install libusb for your system (see Prerequisites above).

### "Permission denied" for log files
Run with sudo: `sudo python3 UsbForensics.py ...`

### Volatility3 analysis fails
Ensure the memory dump is valid and you have the correct version of Volatility3. Note that cross-platform analysis (Windows dumps on Linux) may have limitations.

## License

This tool is for educational and authorized forensic analysis only.

## Contributing

Contributions are welcome! Please ensure all changes are tested on both Linux and macOS where applicable.
