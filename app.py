from flask import Flask, render_template, jsonify, send_file
from scapy.all import sniff
import joblib
import threading
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

# Load trained AI model
model = joblib.load("model.pkl")

# Global counters
attack_count = 0
normal_count = 0

# Store recent packets
packet_logs = []


# ✅ Packet Processing Function
def process_packet(packet):
    global attack_count, normal_count, packet_logs

    try:
        if packet.haslayer("IP"):

            src_ip = packet["IP"].src
            dst_ip = packet["IP"].dst
            protocol = packet["IP"].proto

            if protocol == 6:
                proto_name = "TCP"
            elif protocol == 17:
                proto_name = "UDP"
            else:
                proto_name = "OTHER"

            # Dummy feature vector (same structure as training)
            features = [[0] * 41]

            prediction = model.predict(features)[0]

            if prediction == 1:
                result = "ATTACK"
                attack_count += 1
            else:
                result = "NORMAL"
                normal_count += 1

            log = {
                "src": src_ip,
                "dst": dst_ip,
                "proto": proto_name,
                "result": result
            }

            packet_logs.append(log)

            # Keep only last 20 packets
            if len(packet_logs) > 20:
                packet_logs.pop(0)

            print(f"{src_ip} → {dst_ip} | {proto_name} | {result}")

    except:
        pass


# ✅ Background Sniffing
def start_sniffing():
    sniff(filter="ip", prn=process_packet, store=0)


threading.Thread(target=start_sniffing, daemon=True).start()


# ✅ HOME ROUTE (Dashboard)
@app.route("/")
def home():
    return render_template("index.html")


# ✅ LIVE DATA API
@app.route("/live_data")
def live_data():
    return jsonify({
        "attacks": attack_count,
        "normal": normal_count,
        "logs": packet_logs
    })


# ✅ PDF REPORT ROUTE
@app.route("/report")
def generate_report():

    file_path = "security_report.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("AI-Based Intrusion Detection Report", styles['Title']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"Total Attacks Detected: {attack_count}", styles['Heading2']))
    elements.append(Paragraph(f"Total Normal Traffic: {normal_count}", styles['Heading2']))

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Recent Packet Activity:", styles['Heading2']))
    elements.append(Spacer(1, 10))

    for log in packet_logs:
        elements.append(
            Paragraph(
                f"{log['src']} → {log['dst']} | {log['proto']} | {log['result']}",
                styles['BodyText']
            )
        )

    doc.build(elements)

    return send_file(file_path, as_attachment=True)


# ✅ RUN APP
if __name__ == "__main__":
    app.run(debug=True)