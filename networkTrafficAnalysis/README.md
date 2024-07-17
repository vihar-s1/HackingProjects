# Network Traffic Analysis Tool

## Overview

The Network Traffic Analysis Tool captures and analyzes network traffic on a specified network interface. It supports capturing various types of network packets, storing the captured data in an Excel file, and visualizing the traffic over time. The tool can be run either via the command line or using a graphical user interface (GUI).

## Features

- Capture HTTP, TCP, UDP, and ICMP packets.
- Store captured packet data in an Excel file.
- Visualize network traffic over time.
- Run in both terminal mode and GUI mode.

## Requirements

- Python 3.x
- Required Python packages:
  - `scapy`
  - `pandas`
  - `openpyxl`
  - `matplotlib`
  - `tkinter` (for GUI)

## Usage

### Terminal Mode

1. Run the backend script:
    ```sh
    sudo python3 NTAtool.py
    ```

2. Follow the prompts to enter the network interface, capture duration, and output file path.

3. The captured packet data will be saved to the specified Excel file, and a visualization of the network traffic will be displayed.

### GUI Mode

1. Run the GUI script:
    ```sh
    sudo python3 gui.py
    ```

2. Enter the network interface and capture duration, and select the output file path.

3. Click "Start Capture" to begin capturing packets. Once the capture is complete, the data will be saved to the specified Excel file.
	1. If running in end-less mode *(capture_duration = 0)*, then click "Stop Capture" to stop capturing the packets. Data is automatically saved on stoping packet capture.

4. Click "Visualize Traffic" to display a plot of the network traffic over time.

## Project Structure

- `NTAtool.py`: The backend script containing the core functionality for packet capture and analysis.
- `gui.py`: The GUI script for interacting with the tool through a graphical user interface.
- `README.md`: This file.

## Example

### Terminal Mode

```sh
$ sudo python3 NTAtool.py
Enter the network interface (e.g., eth0, wlan0): eth0
Enter the duration to capture packets (in seconds, 0 for non-stop): 60
Enter the output file path (default: captured_packets.xlsx): captured_packets.xlsx
Starting packet capture on eth0 for 60 seconds...
...
Packet capture complete. Data saved to captured_packets.xlsx
