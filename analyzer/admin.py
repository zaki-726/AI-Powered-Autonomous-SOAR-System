from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'source_ip', 'attack_type', 'is_anomaly', 'action_taken')
    list_filter = ('is_anomaly', 'attack_type')