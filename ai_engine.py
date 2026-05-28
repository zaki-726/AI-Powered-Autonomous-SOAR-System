import os
import sys
import django
import pandas as pd
import numpy as np
import random
import time
from sklearn.ensemble import IsolationForest

# =====================================================================
# DJANGO BACKEND INTEGRATION SETUP
# =====================================================================
# This allows our standalone AI script to talk directly to Django's database
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soar_core.settings")
django.setup()

# Import the Database Model from your analyzer app
from analyzer.models import Alert

# =====================================================================
# 1. GENERATE MOCK HISTORICAL TRAFFIC (For AI Training)
# =====================================================================
def generate_historical_logs(num_rows=1500):
    print(f"🔄 Generating {num_rows} historical network logs for AI training...")
    data = []
    for _ in range(num_rows):
        is_anomaly = random.choices([0, 1], weights=[0.95, 0.05])[0]
        if is_anomaly == 0:
            packet_size = random.randint(40, 1500)
            request_rate = random.randint(1, 10)
            failed_logins = random.randint(0, 1)
        else:
            attack_type = random.choice(['ddos', 'brute_force'])
            if attack_type == 'ddos':
                packet_size = random.randint(5000, 65000)
                request_rate = random.randint(500, 2000)
                failed_logins = 0
            else:
                packet_size = random.randint(40, 200)
                request_rate = random.randint(20, 100)
                failed_logins = random.randint(15, 50)
                
        data.append([packet_size, request_rate, failed_logins])
        
    return pd.DataFrame(data, columns=['packet_size', 'request_rate', 'failed_logins'])

# =====================================================================
# 2. TRAIN THE ANOMALY DETECTION MODEL
# =====================================================================
def train_ai_model(df):
    print("🧠 Training Isolation Forest Anomaly Detection model...")
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(df)
    print("✅ Model trained successfully!")
    return model

# =====================================================================
# 3. LIVE STREAM MONITORING & AUTONOMOUS DATABASE INJECTION
# =====================================================================
def start_live_soar_stream(model):
    print("\n🚀 AI-SOAR Engine is LIVE. Simulating network traffic stream...")
    print("📡 Watching for malicious activities and writing to Django DB...")
    print("-" * 80)
    
    # Simulated live incoming connection logs
    live_traffic_simulation = [
        {"ip": "192.168.1.15", "stats": [120, 4, 0]},       # Normal user
        {"ip": "10.0.0.45", "stats": [64000, 1850, 0]},    # Massive DDoS spike
        {"ip": "192.168.1.22", "stats": [450, 2, 1]},       # Normal user typo
        {"ip": "172.16.5.109", "stats": [85, 55, 42]},      # Brute Force credential stuffing
        {"ip": "192.168.1.99", "stats": [1100, 8, 0]},      # Normal streaming video
    ]
    
    for connection in live_traffic_simulation:
        time.sleep(2)  # Pause for 2 seconds to simulate real-world traffic gaps
        
        ip = connection["ip"]
        features = connection["stats"]
        
        # Format metrics for the AI prediction
        test_df = pd.DataFrame([features], columns=['packet_size', 'request_rate', 'failed_logins'])
        prediction = model.predict(test_df)[0]
        
        # Parse results and set autonomous playbook mitigation actions
        if prediction == 1:
            anomaly_status = False
            detected_attack = "Normal Traffic"
            action = "Monitored Only"
        else:
            anomaly_status = True
            # Determine the type of anomaly using simple logic rules for categorization
            if features[1] > 500:
                detected_attack = "DDoS Attack"
                action = f"🚨 AUTONOMOUS MITIGATION: Blocked Source IP {ip} via Firewall (UFW)"
            elif features[2] > 10:
                detected_attack = "Brute Force"
                action = f"🚨 AUTONOMOUS MITIGATION: Isolated Host Machine {ip}"
            else:
                detected_attack = "Suspicious Anomaly"
                action = "Flagged for Review"

        # 🚀 WRITE DIRECTLY TO THE DJANGO SQLITE DATABASE
        alert_record = Alert.objects.create(
            source_ip=ip,
            packet_size=features[0],
            request_rate=features[1],
            failed_logins=features[2],
            attack_type=detected_attack,
            is_anomaly=anomaly_status,
            action_taken=action,
            is_resolved=anomaly_status # Mark as automatically handled if it's an anomaly
        )
        
        print(f"📥 Saved Log from {ip} | AI Detection: {detected_attack} | SOAR Action: {action}")

if __name__ == "__main__":
    historical_data = generate_historical_logs(1000)
    ai_model = train_ai_model(historical_data)
    start_live_soar_stream(ai_model)
    print("\n🏁 Stream complete. Check your Django Admin page!")