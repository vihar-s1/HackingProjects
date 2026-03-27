#!/usr/bin/env python3
"""
USB Port Monitor for macOS - Real-time USB device monitoring using IOKit.
"""

import sys
import tkinter as tk
from tkinter import ttk

try:
    import objc
    from Foundation import NSObject, NSRunLoop, NSTimer
    from IOKit import usb
    from IOKit.usb import IOUSBLib
except ImportError:
    print("Error: pyobjc-framework-Cocoa not installed.")
    print("Install with: pip install pyobjc-framework-Cocoa pyobjc-framework-IOKit")
    sys.exit(1)

# Import IOKit constants
try:
    from IOKit.usb.IOUSBLib import kIOUSBDeviceClass
    from IOKit import kIOMainPortDefault
except ImportError:
    # Fallback for older macOS versions
    kIOMainPortDefault = 0


def get_usb_devices():
    """Get list of connected USB devices using IOKit."""
    devices = []

    try:
        # Create matching dictionary for USB devices
        matching_dict = usb.IOServiceMatching("IOUSBDevice")
        if matching_dict is None:
            return devices

        # Get iterator of matching services
        # Use kIOMainPortDefault for macOS 12+, or 0 for older versions
        iterator = usb.IOServiceGetMatchingServices(kIOMainPortDefault, matching_dict)
        if iterator == 0:
            return devices

        # Iterate through devices
        while True:
            device = usb.IOIteratorNext(iterator)
            if device == 0:
                break

            # Get device name
            name = None
            try:
                name_ref = usb.IORegistryEntryCreateCFProperty(
                    device,
                    b"USB Product Name",
                    None,
                    0
                )
                if name_ref:
                    name = str(name_ref)
                    # Release the CFStringRef
                    from CoreFoundation import CFRelease
                    CFRelease(name_ref)
            except Exception:
                pass

            # Get vendor ID and product ID
            vendor_id = None
            product_id = None

            try:
                vendor_ref = usb.IORegistryEntryCreateCFProperty(
                    device,
                    b"idVendor",
                    None,
                    0
                )
                if vendor_ref:
                    vendor_id = int(vendor_ref)
                    from CoreFoundation import CFRelease
                    CFRelease(vendor_ref)
            except Exception:
                pass

            try:
                product_ref = usb.IORegistryEntryCreateCFProperty(
                    device,
                    b"idProduct",
                    None,
                    0
                )
                if product_ref:
                    product_id = int(product_ref)
                    from CoreFoundation import CFRelease
                    CFRelease(product_ref)
            except Exception:
                pass

            # Build device info string
            if name:
                device_info = name
            else:
                device_info = "Unknown Device"

            if vendor_id is not None and product_id is not None:
                device_info += f" ({vendor_id:#06x}:{product_id:#06x})"
            elif vendor_id is not None:
                device_info += f" (Vendor: {vendor_id:#06x})"

            devices.append(device_info)

            # Release the device object
            usb.IOObjectRelease(device)

        # Release the iterator
        usb.IOObjectRelease(iterator)

    except Exception as e:
        print(f"Error enumerating USB devices: {e}")

    return devices


class USBMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("USB Port Monitor - macOS")
        self.root.geometry("600x400")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

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

    def update_devices(self):
        """Update the listbox with current USB devices."""
        if not self.monitoring:
            return

        try:
            devices = get_usb_devices()
            self.listbox.delete(0, tk.END)

            if devices:
                for device in devices:
                    self.listbox.insert(tk.END, device)
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
