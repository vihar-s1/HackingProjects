#!/usr/bin/env python3

import scapy.all as scapy
from scapy.layers.http import HTTPRequest
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Global variable to store captured packets
captured_packets = []


# Function to capture and process network packets
def packet_callback(packet):
    # print(packet)
    if packet.haslayer(HTTPRequest):
        packet_info = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_ip': packet[scapy.IP].src,
            'destination_ip': packet[scapy.IP].dst,
            'method': packet[HTTPRequest].Method.decode(),
            'host': packet[HTTPRequest].Host.decode(),
            'path': packet[HTTPRequest].Path.decode()
        }
        captured_packets.append(packet_info)
        print(packet_info)


# Function to start packet capture
def start_packet_capture(target_interface):
    scapy.sniff(iface=target_interface, prn=packet_callback, store=False)


# Function to save captured packets to CSV
def save_packets_to_csv(file_path):
    df = pd.DataFrame(captured_packets)
    df.to_csv(file_path, index=True)


# Function to visualize network traffic
def visualize_traffic():
    df = pd.DataFrame(captured_packets)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    traffic = df.groupby(df['timestamp'].dt.minute).size()

    plt.figure(figsize=(10, 6))
    plt.plot(traffic.index, traffic.values, marker='o')
    plt.title('Network Traffic Over Time')
    plt.xlabel('Time (minute)')
    plt.ylabel('Number of Requests')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    interface = input("Enter the network interface (e.g., eth0, wlan0): ")
    output_csv = input("Enter the name of the CSV file to save the captured packets: ")
    print(f"Starting packet capture on {interface}...")
    start_packet_capture(interface)

    print(f"Packet capture complete. Saving captured packets to '{output_csv}'...")
    save_packets_to_csv(output_csv)

    print("Visualizing network traffic...")
    visualize_traffic()
