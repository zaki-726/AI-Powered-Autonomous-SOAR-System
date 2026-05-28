from django.contrib import admin
from django.urls import path
from analyzer.views import dashboard_view, trigger_attack_simulation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_view, name='dashboard'),
    
    # 🚀 Route path for triggering our autonomous security playbooks
    path('trigger/<str:attack_type>/', trigger_attack_simulation, name='trigger_attack'),
]