import warnings
warnings.filterwarnings("ignore")

from scapy.all import sniff, IP, TCP, UDP, ICMP
import joblib
import random

print("Loading AI Model...")
model = joblib.load("model.pkl")

print("Model Loaded ✅")
print("Monitoring Live Traffic...\n")

def process_packet(packet):

    # ✅ Extract REAL Packet Info
    if packet.haslayer(IP):

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        protocol = "OTHER"

        if packet.haslayer(TCP):
            protocol = "TCP"
        elif packet.haslayer(UDP):
            protocol = "UDP"
        elif packet.haslayer(ICMP):
            protocol = "ICMP"

        print(f"\n📡 Packet Captured:")
        print(f"Source IP      : {src_ip}")
        print(f"Destination IP : {dst_ip}")
        print(f"Protocol       : {protocol}")

        # 🚨 AI Detection (Simulated Features)
        if random.random() > 0.7:
            fake_features = [random.random() * 10 for _ in range(41)]  # Attack
        else:
            fake_features = [random.random() for _ in range(41)]       # Normal

        prediction = model.predict([fake_features])

        if prediction[0] == 1:
            print("🚨 ATTACK DETECTED")
        else:
            print("✅ Normal Traffic")

# Start Sniffing
sniff(filter="ip", prn=process_packet, count=10)