#!/usr/bin/env python3

import scapy.all as scapy
from scapy.layers.http import HTTPRequest
from scapy.layers.inet import IP, TCP, UDP, ICMP
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Global variable to store captured packets
captured_packets = []


# Function to capture and process network packets
# Function to capture and process network packets
def packet_callback(packet):
    packet_info = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source_ip': packet[IP].src if packet.haslayer(IP) else None,
        'destination_ip': packet[IP].dst if packet.haslayer(IP) else None,
        'protocol': None,
        'info': None
    }

    if packet.haslayer(HTTPRequest):
        packet_info.update({
            'protocol': 'HTTP',
            'info': f"{packet[HTTPRequest].Method.decode()} {packet[HTTPRequest].Host.decode()}{packet[HTTPRequest].Path.decode()}"
        })
    elif packet.haslayer(TCP):
        packet_info.update({
            'protocol': 'TCP',
            'info': f"Src Port: {packet[TCP].sport}, Dst Port: {packet[TCP].dport}"
        })
    elif packet.haslayer(UDP):
        packet_info.update({
            'protocol': 'UDP',
            'info': f"Src Port: {packet[UDP].sport}, Dst Port: {packet[UDP].dport}"
        })
    elif packet.haslayer(ICMP):
        packet_info.update({
            'protocol': 'ICMP',
            'info': f"Type: {packet[ICMP].type}, Code: {packet[ICMP].code}"
        })
    else:
        packet_info.update({
            'protocol': 'Other',
            'info': 'Other type of packet'
        })

    captured_packets.append(packet_info)
    print(packet_info)


# Function to start packet capture
def start_packet_capture(target_interface):
    scapy.sniff(iface=target_interface, prn=packet_callback, store=False)


# Function to save captured packets to CSV
def save_packets_to_csv(file_path):
    df = pd.DataFrame(captured_packets)
    df.to_csv(file_path, index=False)


# Function to visualize network traffic
def visualize_traffic():
    df = pd.DataFrame(captured_packets)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Group by each second
    traffic = df.groupby(df['timestamp'].dt.floor('s')).size()
    
    plt.figure(figsize=(10, 6))
    plt.plot(traffic.index, traffic.values, marker='o')
    plt.title('Network Traffic Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Number of Packets')
    plt.grid(True)
    # plt.xticks(rotation=45)
    plt.tight_layout()
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
