# ai/audits/models.py
from django.db import models
from apps.tenants.models import Tenant, Project

class AIAuditLog(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, related_name='ai_audits')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    
    model = models.CharField(max_length=100)
    purpose = models.CharField(max_length=255)
    prompt_hash = models.CharField(max_length=64, db_index=True)
    
    input_tokens = models.IntegerField()
    output_tokens = models.IntegerField()
    cost_usd = models.DecimalField(max_digits=10, decimal_places=6)
    latency_ms = models.IntegerField()
    success = models.BooleanField(default=True)
    error_detail = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
