#!/usr/bin/env python3

import usb.core
import usb.util
import os

from volatility3.framework import contexts, interfaces, automagic
from volatility3.framework.configuration import requirements
from volatility3.cli import text_renderer
from volatility3.plugins.windows import pslist

import pandas as pd


def list_usb_devices():
    devices = usb.core.find(find_all=True)
    device_info = []
    for device in devices:
        info = {
            'idVendor': hex(device.idVendor),
            'idProduct': hex(device.idProduct),
            'serial_number': usb.util.get_string(device, 256, device.iSerialNumber)
        }
        device_info.append(info)
    return device_info


def extract_logs(log_file_path):
    with open(log_file_path, 'r') as file:
        logs = file.readlines()
    return logs


def parse_logs(logs):
    usb_events = []
    for log in logs:
        if 'usb' in log.lower():
            usb_events.append(log)
    return usb_events


def analyze_memory(memory_file):
    # Create a Volatility 3 context
    ctx = contexts.ContextInterface()
    automagics = automagic.available(ctx)
    requirements.RequirementInterface.provide_requirements(ctx, automagics, {}, {})

    # Load the memory file
    single_location = f"file://{memory_file}"
    ctx.config['automagic.LayerStacker.single_location'] = single_location

    # Run pslist plugin to list processes (as an example)
    plugin = pslist.PsList(ctx, config_path=None, progress_callback=None)
    renderer = text_renderer.JsonRenderer()
    plugin.render(renderer)

    # Collect results
    results = renderer.finalize()
    return results


def detect_suspicious_activity(usb_events):
    # Implement detection logic
    # This is a placeholder for actual detection algorithms
    suspicious_events = [event for event in usb_events if 'suspicious' in event.lower()]
    return suspicious_events


def generate_report(suspicious_events):
    df = pd.DataFrame(suspicious_events, columns=['Event'])
    df.to_csv('usb_forensics_report.csv', index=False)


if __name__ == "__main__":
    devices = list_usb_devices()
    for device in devices:
        print(device)

    log_file_path = '/var/log/syslog'  # Update this path for your system
    logs = extract_logs(log_file_path)
    usb_events = parse_logs(logs)
    for event in usb_events:
        print(event)

    memory_file = 'memory.dmp'  # Update this path for your memory dump file
    analyze_memory(memory_file)

    suspicious_events = detect_suspicious_activity(usb_events)
    generate_report(suspicious_events)
