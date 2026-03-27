#!/usr/bin/env python3
"""
USB Forensics Tool - Analyzes USB device activity and memory dumps.

Features:
- List connected USB devices
- Parse system logs for USB events
- Analyze memory dumps using Volatility3
- Detect suspicious USB activity
- Generate forensic reports
"""

import usb.core
import usb.util
import argparse
import sys
from pathlib import Path

import pandas as pd

from volatility3.framework import contexts, symbols
from volatility3.framework.configuration import requirements
from volatility3.framework import interfaces


def list_usb_devices():
    """List all connected USB devices."""
    devices = []
    try:
        found_devices = usb.core.find(find_all=True)
        for device in found_devices:
            info = {
                'idVendor': hex(device.idVendor),
                'idProduct': hex(device.idProduct),
                'serial_number': None,
                'manufacturer': None,
                'product': None
            }
            try:
                if device.iSerialNumber:
                    info['serial_number'] = usb.util.get_string(device, device.iSerialNumber)
                if device.iManufacturer:
                    info['manufacturer'] = usb.util.get_string(device, device.iManufacturer)
                if device.iProduct:
                    info['product'] = usb.util.get_string(device, device.iProduct)
            except (usb.core.USBError, ValueError) as e:
                print(f"Warning: Could not read device info: {e}")
            devices.append(info)
    except usb.core.NoBackendError:
        print("Error: No USB backend found. Please install libusb.")
        return []
    except Exception as e:
        print(f"Error listing USB devices: {e}")
        return []
    return devices


def extract_logs(log_file_path):
    """Extract logs from a log file."""
    if not Path(log_file_path).exists():
        print(f"Error: Log file '{log_file_path}' not found.")
        return []
    try:
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
            logs = file.readlines()
        return logs
    except PermissionError:
        print(f"Error: Permission denied reading '{log_file_path}'. Try running with sudo.")
        return []
    except Exception as e:
        print(f"Error reading log file: {e}")
        return []


def parse_logs(logs):
    """Parse logs for USB-related events."""
    usb_events = []
    keywords = ['usb', 'usb-storage', 'uhci', 'ehci', 'xhci', 'mass storage', 'sd[a-z]']
    for log in logs:
        log_lower = log.lower()
        if any(keyword in log_lower for keyword in keywords):
            usb_events.append(log.strip())
    return usb_events


def analyze_memory(memory_file):
    """
    Analyze a memory dump using Volatility3.
    Returns a list of processes found in the memory dump.
    """
    if not Path(memory_file).exists():
        print(f"Error: Memory file '{memory_file}' not found.")
        return []

    try:
        # Create Volatility 3 context
        ctx = contexts.ContextInterface()

        # Set up the location for the memory file
        single_location = f"file://{memory_file}"
        ctx.config['automagic.LayerStacker.single_location'] = single_location

        # Initialize symbol path
        ctx.config['automagic.LayerStacker.symbol_path'] = None

        # Run automagics to configure the context
        automagics = automagic.available(ctx)
        for automagic in automagics:
            try:
                automagic(ctx, None, {})
            except Exception:
                continue

        # Try to determine the OS and load appropriate plugins
        # This is a simplified example - real usage would need more sophisticated detection
        from volatility3.plugins.windows import pslist
        from volatility3.cli import text_renderer

        plugin = pslist.PsList(ctx)
        renderer = text_renderer.TreeRenderer()

        results = []
        for level, line in plugin.render():
            results.append(line)

        return results

    except ImportError:
        print("Note: Volatility3 Windows plugins not available. Skipping Windows analysis.")
        return []
    except Exception as e:
        print(f"Error analyzing memory dump: {e}")
        return []


def detect_suspicious_activity(usb_events, known_vendors=None):
    """
    Detect suspicious USB activity.

    Args:
        usb_events: List of USB event strings
        known_vendors: Optional list of known/safe vendor IDs

    Returns:
        List of suspicious events
    """
    if known_vendors is None:
        known_vendors = []

    suspicious_events = []

    # Common suspicious patterns
    suspicious_patterns = [
        'unauthorized',
        'failed',
        'error',
        'disconnect',
        'reset',
        'overflow',
        'malicious',
        'infection',
        'virus'
    ]

    for event in usb_events:
        event_lower = event.lower()
        # Check for suspicious patterns
        if any(pattern in event_lower for pattern in suspicious_patterns):
            suspicious_events.append({
                'type': 'suspicious_pattern',
                'event': event
            })
        # Check for unknown vendors
        for vendor in known_vendors:
            if vendor.lower() in event_lower:
                break
        else:
            if known_vendors and any(vid in event_lower for vid in ['0x']):
                suspicious_events.append({
                    'type': 'unknown_vendor',
                    'event': event
                })

    return suspicious_events


def generate_report(suspicious_events, output_file='usb_forensics_report.csv'):
    """Generate a CSV report of suspicious USB events."""
    if not suspicious_events:
        print("No suspicious events to report.")
        # Create empty report
        df = pd.DataFrame(columns=['Type', 'Event'])
        df.to_csv(output_file, index=False)
        print(f"Empty report saved to: {output_file}")
        return

    # Convert to DataFrame with proper structure
    data = []
    for event in suspicious_events:
        if isinstance(event, dict):
            data.append({
                'Type': event.get('type', 'unknown'),
                'Event': event.get('event', str(event))
            })
        else:
            data.append({
                'Type': 'general',
                'Event': str(event)
            })

    df = pd.DataFrame(data, columns=['Type', 'Event'])
    df.to_csv(output_file, index=False)
    print(f"Report saved to: {output_file}")
    print(f"Total suspicious events: {len(data)}")


def main():
    parser = argparse.ArgumentParser(
        description='USB Forensics Tool - Analyze USB device activity and memory dumps'
    )
    parser.add_argument(
        '--list-devices', '-l',
        action='store_true',
        help='List connected USB devices'
    )
    parser.add_argument(
        '--log-file', '-f',
        type=str,
        help='Path to system log file (default: /var/log/syslog)'
    )
    parser.add_argument(
        '--memory-file', '-m',
        type=str,
        help='Path to memory dump file for Volatility analysis'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='usb_forensics_report.csv',
        help='Output file for forensic report (default: usb_forensics_report.csv)'
    )
    parser.add_argument(
        '--known-vendors', '-k',
        type=str,
        nargs='+',
        help='List of known/safe vendor IDs to exclude from suspicious detection'
    )

    args = parser.parse_args()

    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # List USB devices
    if args.list_devices:
        print("=" * 50)
        print("Connected USB Devices:")
        print("=" * 50)
        devices = list_usb_devices()
        if devices:
            for device in devices:
                print(f"Vendor: {device['idVendor']}, Product: {device['idProduct']}")
                if device['serial_number']:
                    print(f"  Serial: {device['serial_number']}")
                if device['manufacturer']:
                    print(f"  Manufacturer: {device['manufacturer']}")
                if device['product']:
                    print(f"  Product: {device['product']}")
                print()
        else:
            print("No USB devices found or unable to enumerate.")
        print()

    # Analyze logs
    log_file = args.log_file or '/var/log/syslog'
    if Path(log_file).exists() or args.log_file:
        print("=" * 50)
        print(f"Analyzing log file: {log_file}")
        print("=" * 50)
        logs = extract_logs(log_file)
        if logs:
            usb_events = parse_logs(logs)
            print(f"Found {len(usb_events)} USB-related events")

            # Detect suspicious activity
            suspicious_events = detect_suspicious_activity(usb_events, args.known_vendors)
            if suspicious_events:
                print(f"Detected {len(suspicious_events)} suspicious events")
                generate_report(suspicious_events, args.output)
            else:
                print("No suspicious activity detected.")
        else:
            print("No logs to analyze or unable to read log file.")
        print()

    # Analyze memory dump
    if args.memory_file:
        print("=" * 50)
        print(f"Analyzing memory dump: {args.memory_file}")
        print("=" * 50)
        results = analyze_memory(args.memory_file)
        if results:
            print(f"Found {len(results)} entries in memory dump")
            for result in results[:10]:  # Show first 10
                print(result)
        else:
            print("No results from memory analysis or analysis failed.")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
