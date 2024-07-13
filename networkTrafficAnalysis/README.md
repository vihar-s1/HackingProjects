# Network Traffic Analysis Tool

## Overview

The Network Traffic Analysis Tool is designed to monitor and analyze network traffic to detect anomalies and potential security threats. It captures HTTP requests, logs packet information, and provides visualizations to help identify unusual patterns in network activity.

## Features

- Captures HTTP request packets.
- Logs source and destination IPs, HTTP method, host, and path.
- Saves captured packet data to a CSV file.
- Visualizes network traffic over time.

## Requirements

- Python 3.x
- Scapy library
- Pandas library
- Matplotlib library

<!-- ## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/vihar-s1/network-traffic-analysis-tool.git
    cd network-traffic-analysis-tool
    ```

2. **Set up a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ``` -->

## Usage

1. **Run the tool**:
    ```sh
    python3 NTAtool.py
    ```

2. **Input required information**:
    - Enter the network interface (e.g., `eth0`, `wlan0`).
    - Enter the name of the CSV file to save the captured packets.

3. **Monitor the output**:
    - The tool will capture and log HTTP request packets, displaying packet information in real-time.
    - Once the capture is complete, the data will be saved to the csv file with the given name.

4. **Visualize network traffic**:
    - After packet capturing process is terminated, a plot will be displayed showing the number of HTTP requests over time.

## Example

```sh
Enter the network interface (e.g., eth0, wlan0): eth0
Enter the name of the CSV file to save the captured packets: captured_packets.csv
Starting packet capture on eth0...
{'timestamp': '2023-07-11 12:00:01', 'source_ip': '192.168.1.2', 'destination_ip': '93.184.216.34', 'method': 'GET', 'host': 'example.com', 'path': '/index.html'}
...
Packet capture complete. Saving captured packets to 'captured_packets.csv'...
Visualizing network traffic...
