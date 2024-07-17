import scapy.all as scapy
from threading import Event

from scapy.layers.http import HTTPRequest
from scapy.layers.inet import IP, TCP, UDP, ICMP
import pandas as pd
from openpyxl import Workbook
from datetime import datetime
import matplotlib.pyplot as plt

# Global variable to store captured packets
captured_packets = []
workbook = Workbook()

class NTA:
    def __init__(self, logEnabled:bool=False) -> None:
        self.captured_packets = []
        self.workbook = Workbook()
        self.logEnabled = logEnabled
        self.stop_event = Event()
        
        worksheet = self.workbook.active
        worksheet.title = 'Captured Packets'
        worksheet.append(['timestamp', 'source_ip', 'source_port', 'destination_ip', 'destination_port', 'protocol', 'info'])
        
    def packet_callback(self, packet):
        packet_info = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_ip': packet[IP].src if packet.haslayer(IP) else None,
            'source_port': None,
            'destination_ip': packet[IP].dst if packet.haslayer(IP) else None,
            'destination_port': None,
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
                'source_port': packet[TCP].sport,
                'destination_port': packet[TCP].dport,
            })
        elif packet.haslayer(UDP):
            packet_info.update({
                'protocol': 'UDP',
                'source_port': packet[UDP].sport,
                'destination_port': packet[UDP].dport,
            })
        elif packet.haslayer(ICMP):
            packet_info.update({
                'protocol': 'ICMP',
                'source_port': packet[ICMP].sport,
                'destination_port': packet[ICMP].dport,
            })
        else:
            return
        #     packet_info.update({
        #         'protocol': 'Other',
        #         'info': 'Other type of packet'
        #     })

        self.captured_packets.append(packet_info)
        self.workbook.active.append(list(packet_info.values()))
        if self.logEnabled: print(packet_info) 
        
    def start_packet_capture(self, interface, duration):
        self.stop_event.clear()
        if duration <= 0:
            while not self.stop_event.is_set():
                scapy.sniff(iface=interface, prn=self.packet_callback, store=False, timeout=1)
        else:
            scapy.sniff(iface=interface, prn=self.packet_callback, store=False, timeout=duration)

    def stop_packet_capture(self):
        self.stop_event.set()
            
    def visualize_traffic(self):
        df = pd.DataFrame(self.captured_packets)
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

    def save_excel(self, output_path: str):
        self.workbook.save(output_path)    
        if self.logEnabled: print(f"Packet capture complete. Data saved to {output_path}")

    def clear_packets(self):
        self.captured_packets.clear()
        self.workbook.close()
        self.workbook = Workbook()
        if self.logEnabled: print("Packets cleared.")

    def enableLogging(self):
        self.logEnabled = True
    
    def disableLogging(self):
        self.logEnabled = False
       

if __name__ == "__main__":
    interface = input("Enter the network interface (e.g., eth0, wlan0): ")
    capture_duration = int(input("Enter the duration to capture packets (in seconds, 0 for non-stop): "))
    output_path = input("Enter the output file path (default: captured_packets.xlsx): ")

    if not output_path:
        output_path = "captured_packets.xslx"
        
    capture_duration = min(capture_duration, 0)

    nta = NTA(True)
    nta.start_packet_capture(interface=interface, duration=capture_duration)
    nta.save_excel(output_path)
    nta.visualize_traffic()
        
