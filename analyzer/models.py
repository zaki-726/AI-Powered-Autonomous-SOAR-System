from django.db import models

class Alert(models.Model):
    # Incident Details
    timestamp = models.DateTimeField(auto_now_add=True)
    source_ip = models.GenericIPAddressField(default="192.168.1.100")
    packet_size = models.IntegerField()
    request_rate = models.IntegerField()
    failed_logins = models.IntegerField()
    
    # AI Assessment Results
    attack_type = models.CharField(max_length=50, default="Unknown")
    is_anomaly = models.BooleanField(default=False)
    
    # SOAR Autonomous Action Status
    action_taken = models.CharField(max_length=100, default="Monitored Only")
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        status = "🚨 ANOMALY" if self.is_anomaly else "🟢 NORMAL"
        return f"{status} - {self.attack_type} from {self.source_ip}"