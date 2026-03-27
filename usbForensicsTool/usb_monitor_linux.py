#!/usr/bin/env python3
"""
USB Port Monitor for Linux - Real-time USB device monitoring using pyudev.
"""

import sys
import tkinter as tk
from tkinter import ttk

try:
    import pyudev
except ImportError:
    print("Error: pyudev not installed. Install with: pip install pyudev")
    sys.exit(1)


class USBMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("USB Port Monitor - Linux")
        self.root.geometry("600x400")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create context
        try:
            self.context = pyudev.Context()
        except Exception as e:
            self.show_error(f"Failed to initialize pyudev: {e}")
            return

        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create USB devices listbox with scrollbar
        list_frame = ttk.LabelFrame(main_frame, text="Connected USB Devices", padding="5")
        list_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(list_frame, width=70, height=15, yscrollcommand=scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        # Status label
        self.status_label = ttk.Label(main_frame, text="Connected devices: 0")
        self.status_label.grid(row=1, column=0, sticky=tk.W, pady=5)

        # Refresh button
        self.refresh_btn = ttk.Button(main_frame, text="Refresh", command=self.update_devices)
        self.refresh_btn.grid(row=1, column=1, sticky=tk.E, pady=5)

        # Start monitoring
        self.monitoring = True
        self.update_devices()

    def show_error(self, message):
        """Display error message."""
        tk.messagebox.showerror("Error", message)

    def get_usb_device_info(self, device):
        """Get formatted device information."""
        info_parts = []

        # Get device path
        if hasattr(device, 'device_path'):
            info_parts.append(str(device.device_path))

        # Get device node
        if hasattr(device, 'device_node') and device.device_node:
            info_parts.append(f"({device.device_node})")

        # Get vendor/product info if available
        vendor = device.get('ID_VENDOR', None)
        model = device.get('ID_MODEL', None)

        if vendor or model:
            vendor_model = " ".join(filter(None, [vendor, model]))
            info_parts.append(f"- {vendor_model}")

        # Get serial if available
        serial = device.get('ID_SERIAL_SHORT', None)
        if serial:
            info_parts.append(f"[{serial}]")

        return " ".join(info_parts)

    def update_devices(self):
        """Update the listbox with current USB devices."""
        if not self.monitoring:
            return

        try:
            devices = list(self.context.list_devices(subsystem='usb'))
            self.listbox.delete(0, tk.END)

            if devices:
                for device in devices:
                    info = self.get_usb_device_info(device)
                    self.listbox.insert(tk.END, info)
            else:
                self.listbox.insert(tk.END, "No USB devices found")

            self.status_label.config(text=f"Connected devices: {len(devices)}")

        except Exception as e:
            self.status_label.config(text=f"Error: {e}")

        # Schedule next update
        self.root.after(1000, self.update_devices)

    def on_closing(self):
        """Handle window close event."""
        self.monitoring = False
        self.root.destroy()


def main():
    try:
        root = tk.Tk()
        app = USBMonitorApp(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("\nMonitor stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
