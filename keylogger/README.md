# Keylogger

Input monitoring tool for security research and detection training.

## ⚠️ Legal Notice

**This tool is for authorized security testing only.**

- Use only on systems you own or have explicit written authorization to test
- Unauthorized use may violate federal and state laws
- See [WARNINGS.md](../WARNINGS.md) for complete legal information

## Overview

Keylogger tool for keyboard input capture and detection training. Designed for security professionals to understand input monitoring techniques and test detection capabilities.

## Features

- **Cross-platform support** - Windows, macOS, Linux
- **Keystroke logging** - Capture all keyboard input
- **Clipboard monitoring** - Log clipboard changes
- **Screenshot capture** - Capture screenshots on trigger keywords
- **Log encryption** - AES-256 encrypted logs
- **Detection tool** - Detect other keyloggers on the system

## Installation

### Prerequisites

- Python 3.8+
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

### System Dependencies

**Linux:**
```bash
sudo apt-get install python3-tk python3-dev
```

**macOS:**
```bash
brew install python-tk
```

## Usage

### Basic Keylogger

```bash
# Start with default settings (encrypted logs)
python3 keylogger.py

# Start with custom log file
python3 keylogger.py -o /path/to/log.txt

# Disable encryption
python3 keylogger.py --no-encrypt

# Enable clipboard logging
python3 keylogger.py -c

# Enable screenshots on password keyword
python3 keylogger.py -s -t password
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output log file path |
| `-e, --encrypt` | Encrypt logs (default: True) |
| `--no-encrypt` | Disable log encryption |
| `-k, --key` | Custom encryption key |
| `-c, --clipboard` | Log clipboard changes |
| `-s, --screenshots` | Capture screenshots on triggers |
| `-t, --trigger` | Keyword trigger for screenshots |
| `-d, --debug` | Enable debug logging |

### Detection Tool

```bash
# Run full system scan
python3 detector.py

# Output as JSON
python3 detector.py -j

# Debug mode
python3 detector.py -d
```

### Decrypt Logs

```python
from keylogger.encrypt import LogEncryptor

encryptor = LogEncryptor(key="your-encryption-key")
encryptor.decrypt_file("encrypted.log", "decrypted.log")
```

## Programmatic Usage

```python
from keylogger import Keylogger

kl = Keylogger(
    log_file="/tmp/.kl.log",
    encrypt_logs=True,
    log_clipboard=True,
    log_screenshots=True,
    screenshot_trigger="password",
    debug=True
)

try:
    kl.start()
    while kl.is_running():
        time.sleep(1)
except KeyboardInterrupt:
    kl.stop()
    print(f"Keys captured: {kl.get_stats()['keys_captured']}")
```

## Log Format

Logs are stored as JSON lines:

```json
{"timestamp": "2024-01-15T10:30:00", "type": "keypress", "data": {"key": "a", "char": "a"}}
{"timestamp": "2024-01-15T10:30:01", "type": "keypress", "data": {"key": "enter", "pressed": true}}
{"timestamp": "2024-01-15T10:30:02", "type": "clipboard", "data": {"content": "copied text"}}
```

## Detection Methods

Use the included detector tool or look for:

1. Unknown processes in process list
2. Global keyboard hooks
3. Suspicious network connections
4. Log files in temp directories
5. Unauthorized startup entries

## License

MIT License - See LICENSE file
