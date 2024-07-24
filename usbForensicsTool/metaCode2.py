import objc
from Cocoa import *
from Foundation import *
from IOKit import *

import tkinter as tk
from tkinter import messagebox

# Create a tkinter window
window = tk.Tk()
window.title("USB Port Monitor")

# Create a listbox to display USB devices
listbox = tk.Listbox(window, width=50)
listbox.pack(padx=10, pady=10)

# Create a label to display the number of connected devices
label = tk.Label(window, text="Connected devices: 0")
label.pack(padx=10, pady=10)

def get_usb_devices():
    matching_dict = IOServiceMatching("IOUSBDevice")
    iterator = IOServiceGetMatchingServices(kIOMasterPortDefault, matching_dict, None)
    devices = []

    while True:
        device = IOIteratorNext(iterator)
        if device == 0:
            break

        devices.append(device)

    return devices

# Function to update the listbox and label
def update_devices():
    devices = get_usb_devices()
    listbox.delete(0, tk.END)
    for device in devices:
        name = IORegistryEntryCreateCFProperty(device, "USB Product Name", kCFAllocatorDefault, 0)
        listbox.insert(tk.END, name)
        IOObjectRelease(device)
    label.config(text=f"Connected devices: {len(devices)}")
    window.update_idletasks()
    window.after(1000, update_devices)  # Update every 1 second

# Start the monitoring loop
update_devices()

# Run the GUI event loop
window.mainloop()
