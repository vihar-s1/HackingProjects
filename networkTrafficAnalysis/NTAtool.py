import scapy.all as scapy
from scapy.layers.http import HTTPRequest
from scapy.layers.inet import IP, TCP, UDP, ICMP
import pandas as pd
from openpyxl import Workbook
from datetime import datetime
import matplotlib.pyplot as plt
import time


# Global variable to store captured packets
captured_packets = []
workbook = Workbook()

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
        return
    #     packet_info.update({
    #         'protocol': 'Other',
    #         'info': 'Other type of packet'
    #     })

    captured_packets.append(packet_info)
    save_packet_to_excel(packet_info)
    print(packet_info)


def save_packet_to_excel(packet_info):
    ws = workbook.active
    ws.append(list(packet_info.values()))


def start_packet_capture(interface, duration):
    if duration <= 0:
        scapy.sniff(iface=interface, prn=packet_callback, store=False)
    else:
        scapy.sniff(iface=interface, prn=packet_callback, store=False, timeout=duration)


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
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    interface = input("Enter the network interface (e.g., eth0, wlan0): ")
    capture_duration = int(input("Enter the duration to capture packets (in seconds, 0 for non-stop): "))
    output_path = input("Enter the output file path (default: captured_packets.xlsx): ")

    if not output_path:
        output_path = "captured_packets.xslx"

    worksheet = workbook.active
    worksheet.append(['timestamp', 'source_ip', 'destination_ip', 'protocol', 'info'])

    capture_duration = min(capture_duration, 0)
    print(f"Starting packet capture on {interface} for {capture_duration} seconds...")
    start_packet_capture(interface, capture_duration)
    workbook.save(output_path)

    print(f"Packet capture complete. Data saved to {output_path}")
    
    visualize_traffic()

