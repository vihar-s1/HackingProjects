# Development Plan & TODO - HackingProjects

A structured development roadmap for the HackingProjects security toolkit.

---

## 📋 Project Status Overview

| Project | Status | Priority | Phase |
|---------|--------|----------|-------|
| networkTrafficAnalysis | ✅ Stable | High | Phase 2 |
| scripts/macChanger | ✅ Stable | Medium | Phase 2 |
| usbForensicsTool | ✅ Stable | High | Phase 2 |
| keylogger | ⏳ Planned | High | Phase 1 |
| bluetoothCloner | ⏳ Planned | Medium | Phase 1 |
| wifiAuditor | ⏳ Planned | Medium | Phase 3 |

---

## 🗓️ Development Phases

### Phase 1: Foundation (Weeks 1-4)
**Goal:** Establish new tools and fix critical issues in existing tools

### Phase 2: Enhancement (Weeks 5-8)
**Goal:** Add high-impact features to existing tools

### Phase 3: Advanced Features (Weeks 9-16)
**Goal:** Implement complex features and integrations

### Phase 4: Polish & Scale (Weeks 17+)
**Goal:** Testing, documentation, and advanced tooling

---

## 🔑 NEW: Keylogger Project

**Path:** `keylogger/`  
**Status:** ⏳ Planned  
**Priority:** 🔴 High  
**Estimated Effort:** 3-4 weeks

### Description
Educational keylogger demonstrating input capture techniques for security awareness and detection training.

### TODOs

#### Core Functionality
- [ ] **Create project structure** - Set up `keylogger/` directory with `__init__.py`
- [ ] **Implement keyboard hook (Linux)** - Use `evdev` or `X11` for key capture
- [ ] **Implement keyboard hook (macOS)** - Use `Quartz` framework via pyobjc
- [ ] **Implement keyboard hook (Windows)** - Use `pynput` or native hooks
- [ ] **Add keystroke logging** - Log keys to encrypted file
- [ ] **Add timestamp tracking** - Record timing between keystrokes
- [ ] **Add clipboard monitoring** - Log clipboard changes
- [ ] **Add screenshot capture** - Capture screen on trigger events

#### Stealth & Evasion
- [ ] **Process hiding** - Run as background service/daemon
- [ ] **Log encryption** - Encrypt logs with AES-256
- [ ] **Anti-detection** - Avoid common keylogger signatures
- [ ] **Secure log storage** - Hidden/temp directory storage

#### Data Exfiltration (Educational)
- [ ] **Email exfiltration** - Send logs via SMTP
- [ ] **HTTP exfiltration** - POST logs to remote server
- [ ] **DNS tunneling** - Encode logs in DNS queries
- [ ] **Cloud storage** - Upload to Google Drive/Dropbox

#### Detection & Defense
- [ ] **Detection module** - Detect other keyloggers on system
- [ ] **Process monitoring** - Watch for suspicious keyboard hooks
- [ ] **Network monitoring** - Detect exfiltration attempts
- [ ] **Log analysis** - Identify keylogger artifacts

#### Documentation
- [ ] **README.md** - Installation, usage, legal disclaimer
- [ ] **Detection guide** - How to detect keyloggers
- [ ] **Defense guide** - How to protect against keyloggers
- [ ] **Legal disclaimer** - Educational use only warning

### Tech Stack
- Python 3.8+
- `pynput` - Cross-platform input monitoring
- `pyX11` / `evdev` - Linux input
- `pyobjc-framework-Quartz` - macOS input
- `cryptography` - Log encryption
- `requests` - HTTP exfiltration

---

## 📡 NEW: Bluetooth Cloning Attack Project

**Path:** `bluetoothCloner/`  
**Status:** ⏳ Planned  
**Priority:** 🟡 Medium  
**Estimated Effort:** 4-5 weeks

### Description
Educational tool demonstrating Bluetooth device spoofing and cloning attacks for security research.

### TODOs

#### Core Functionality
- [ ] **Create project structure** - Set up `bluetoothCloner/` directory
- [ ] **Bluetooth scanner** - Discover nearby Bluetooth devices
- [ ] **Device fingerprinting** - Extract device characteristics
- [ ] **MAC address extraction** - Get target device MAC
- [ ] **Service enumeration** - List available Bluetooth services
- [ ] **Device spoofing** - Clone MAC address of target device
- [ ] **Service spoofing** - Advertise cloned services

#### Attack Simulations
- [ ] **Bluejacking** - Send unsolicited messages to devices
- [ ] **Bluesnarfing demo** - Demonstrate data extraction vulnerabilities
- [ ] **MITM positioning** - Position between paired devices
- [ ] **Pairing bypass** - Exploit weak pairing implementations
- [ ] **BLE spoofing** - Bluetooth Low Energy device cloning

#### Defense & Detection
- [ ] **Detection module** - Detect Bluetooth spoofing attempts
- [ ] **Anomaly detection** - Identify unusual Bluetooth behavior
- [ ] **Secure pairing guide** - Best practices for Bluetooth security
- [ ] **Monitoring tool** - Real-time Bluetooth traffic monitor

#### Hardware Integration
- [ ] **External adapter support** - Work with multiple Bluetooth adapters
- [ ] **Range extension** - Support for high-gain antennas
- [ ] **Ubertooth integration** - Optional Ubertooth hardware support

#### Documentation
- [ ] **README.md** - Setup, usage, legal warnings
- [ ] **Attack scenarios** - Document various attack vectors
- [ ] **Defense guide** - Protect against Bluetooth attacks
- [ ] **Hardware guide** - Recommended adapters and setup

### Tech Stack
- Python 3.8+
- `pybluez` - Bluetooth operations
- `bleak` - BLE support
- `scapy` - Packet crafting
- Optional: Ubertooth One hardware

---

## 🌐 networkTrafficAnalysis/

**Status:** ✅ Stable  
**Priority:** 🔴 High  
**Current Phase:** Phase 2

### Phase 1 Tasks (Weeks 1-4)
- [ ] **Add BPF filter support** - Berkeley Packet Filter expressions
- [ ] **Add protocol filtering** - Filter by HTTP/TCP/UDP/ICMP
- [ ] **Fix endless mode race condition** - Clean thread termination
- [ ] **Add capture profiles** - Save/load configurations

### Phase 2 Tasks (Weeks 5-8)
- [ ] **Add PCAP export** - Standard PCAP/PCAPNG format
- [ ] **Add packet payload capture** - Optional payload logging
- [ ] **Add statistics dashboard** - Top talkers, protocol distribution
- [ ] **Memory optimization** - Buffer/flush for long captures

### Phase 3 Tasks (Weeks 9-16)
- [ ] **Add TCP stream reassembly** - Reconstruct conversations
- [ ] **Add alerting system** - Detect port scans, anomalies
- [ ] **Improve visualization** - Interactive plots, pie charts
- [ ] **Add geographic IP mapping** - World map visualization

### Phase 4 Tasks (Weeks 17+)
- [ ] **Multi-interface capture** - Monitor multiple NICs
- [ ] **Add timeline export** - Export for external analysis
- [ ] **Add web interface** - Flask/FastAPI dashboard

---

## 🎭 scripts/ (MAC Changer)

**Status:** ✅ Stable  
**Priority:** 🟡 Medium  
**Current Phase:** Phase 2

### Phase 1 Tasks (Weeks 1-4)
- [ ] **Add systemd service file** - `macchanger-daemon.service`
- [ ] **Add logging to syslog** - Timestamped audit trail
- [ ] **Add configuration file** - `/etc/macchanger.conf`

### Phase 2 Tasks (Weeks 5-8)
- [ ] **Add MAC whitelist** - Restore known-good addresses
- [ ] **Add network connectivity check** - Auto-rollback on failure
- [ ] **Add dry-run mode** - Preview changes

### Phase 3 Tasks (Weeks 9-16)
- [ ] **NetworkManager integration** - Better interface handling
- [ ] **Add status command** - Show current/original MAC
- [ ] **Add change history** - Log all MAC changes

---

## 🔌 usbForensicsTool/

**Status:** ✅ Stable  
**Priority:** 🔴 High  
**Current Phase:** Phase 2

### Phase 1 Tasks (Weeks 1-4)
- [ ] **Add JSON output format** - Machine-readable output
- [ ] **Add batch processing** - Multiple files/dumps

### Phase 2 Tasks (Weeks 5-8)
- [ ] **Add USB history parsing (Linux)** - Parse syslog for events
- [ ] **Add USB history parsing (Windows)** - Parse Registry USBSTOR
- [ ] **Add timeline generation** - Forensic event timeline
- [ ] **Add device fingerprinting** - Vendor/product patterns

### Phase 3 Tasks (Weeks 9-16)
- [ ] **Fix Volatility3 integration** - Proper plugin loading
- [ ] **Add Windows memory dump support** - Cross-platform testing
- [ ] **Improve detection** - ML/signature-based detection
- [ ] **Add HTML/PDF reports** - Professional forensic reports

### Phase 4 Tasks (Weeks 17+)
- [ ] **Add SQLite backend** - Query findings
- [ ] **Add YARA integration** - Malware signature scanning
- [ ] **Add web interface** - Remote analysis dashboard

---

## 📦 General Project Improvements

### Documentation (Phase 1)
- [ ] **Add LICENSE file** - MIT/Apache 2.0
- [ ] **Add CHANGELOG.md** - Version history
- [ ] **Add CONTRIBUTING.md** - Contribution guidelines
- [ ] **Add SECURITY.md** - Security policy and disclosure

### Code Quality (Phase 1-2)
- [ ] **Add type hints** - Python type annotations
- [ ] **Add linting config** - `.flake8`, `pyproject.toml` for black/isort
- [ ] **Add pre-commit hooks** - `.pre-commit-config.yaml`

### Testing (Phase 2-3)
- [ ] **Add unit tests** - pytest for each module
- [ ] **Add integration tests** - Test with sample data
- [ ] **Add test fixtures** - Sample captures, logs, memory dumps

### CI/CD (Phase 3)
- [ ] **GitHub Actions workflow** - `.github/workflows/ci.yml`
- [ ] **Automated testing** - Run on PR and push
- [ ] **Code coverage** - Coveralls/Codecov integration

### Security (Phase 2-3)
- [ ] **Input sanitization** - Validate all user inputs
- [ ] **Privilege separation** - Minimal required privileges
- [ ] **Audit logging** - Log all tool usage

---

## 📊 Priority Matrix

```
                    Impact
            Low ──────────────── High
        ┌─────────────────────────────┐
    Low │ scripts/    │ usbForensics/ │
        │ (Medium)    │ (High)        │
        ├─────────────┼───────────────┤
   High │ bluetooth   │ keylogger     │
        │ (Medium)    │ (High)        │
        └─────────────────────────────┘
              Effort
```

---

## 🎯 Quick Start - Next Actions

1. **Start keylogger project** - Create structure and basic hooks
2. **Start bluetoothCloner project** - Set up and implement scanner
3. **Add BPF filters to NTA** - Quick win for network analysis
4. **Add systemd service for macChanger** - Improve daemon management

---

## ⚠️ Legal Disclaimer

All tools in this repository are for **educational and authorized security testing only**. 
Unauthorized use of these tools may violate laws and regulations. Always obtain proper 
authorization before testing on any system you do not own.

---

## 📝 Progress Tracking

| Week | Focus | Completed |
|------|-------|-----------|
| 1-4 | Phase 1 | - |
| 5-8 | Phase 2 | - |
| 9-16 | Phase 3 | - |
| 17+ | Phase 4 | - |
