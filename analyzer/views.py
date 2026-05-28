from django.shortcuts import render, redirect
from .models import Alert
import random

def dashboard_view(request):
    all_alerts = Alert.objects.all().order_by('-id')[:25] 
    total_logs = Alert.objects.count()
    total_anomalies = Alert.objects.filter(is_anomaly=True).count()
    total_mitigations = Alert.objects.filter(is_anomaly=True).exclude(action_taken="Monitored Only").count()
    
    # NEW: Specific counts for Chart representation
    total_ddos = Alert.objects.filter(attack_type="DDoS Attack").count()
    total_brute_force = Alert.objects.filter(attack_type="Brute Force").count()

    context = {
        'alerts': all_alerts,
        'total_logs': total_logs,
        'total_anomalies': total_anomalies,
        'total_mitigations': total_mitigations,
        'total_ddos': total_ddos,
        'total_brute_force': total_brute_force
    }
    return render(request, 'analyzer/dashboard.html', context)

def trigger_attack_simulation(request, attack_type):
    if attack_type == 'ddos':
        ip = f"172.16.{random.randint(10,250)}.{random.randint(10,250)}"
        packet_size = random.randint(55000, 65000)
        request_rate = random.randint(1200, 2500)
        failed_logins = 0
        detected_attack = "DDoS Attack"
        action = f"🚨 AUTONOMOUS PLAYBOOK: Injected NULL Route to drop traffic from malicious IP {ip}"
    elif attack_type == 'brute_force':
        ip = f"192.168.1.{random.randint(200,254)}"
        packet_size = random.randint(64, 128)
        request_rate = random.randint(45, 95)
        failed_logins = random.randint(25, 60)
        detected_attack = "Brute Force"
        action = f"🚨 AUTONOMOUS PLAYBOOK: Revoked Auth Token & Isolated Host {ip} from network"
    else:
        ip = f"192.168.1.{random.randint(10,150)}"
        packet_size = random.randint(100, 1200)
        request_rate = random.randint(2, 8)
        failed_logins = random.choice([0, 0, 0, 1])
        detected_attack = "Normal Traffic"
        action = "Monitored Only"

    Alert.objects.create(
        source_ip=ip,
        packet_size=packet_size,
        request_rate=request_rate,
        failed_logins=failed_logins,
        attack_type=detected_attack,
        is_anomaly=(attack_type != 'normal'),
        action_taken=action,
        is_resolved=(attack_type != 'normal')
    )
    return redirect('dashboard')