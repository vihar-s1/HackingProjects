import tkinter as tk
from tkinter import messagebox
import pyudev

# Create a tkinter window
window = tk.Tk()
window.title("USB Port Monitor")

# Create a listbox to display USB devices
listbox = tk.Listbox(window, width=50)
listbox.pack(padx=10, pady=10)

# Create a label to display the number of connected devices
label = tk.Label(window, text="Connected devices: 0")
label.pack(padx=10, pady=10)

# Initialize the pyudev context
context = pyudev.Context()

# Function to update the listbox and label
def update_devices():
    devices = context.list_devices(subsystem='usb')
    listbox.delete(0, tk.END)
    for device in devices:
        listbox.insert(tk.END, f"{device.device_path} - {device.device_node}")
    label.config(text=f"Connected devices: {len(devices)}")
    window.update_idletasks()
    window.after(1000, update_devices)  # Update every 1 second

# Start the monitoring loop
update_devices()

# Run the GUI event loop
window.mainloop()