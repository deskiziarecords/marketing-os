# ai/audits/models.py
from django.db import models
from django.conf import settings

class AIAuditLog(models.Model):
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.SET_NULL, null=True, related_name='ai_audits')
    project = models.ForeignKey('tenants.Project', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Detalles de la ejecución
    provider = models.CharField(max_length=50) # 'openai', 'anthropic', 'local'
    model = models.CharField(max_length=100)   # 'gpt-4o', 'claude-3-5-sonnet'
    purpose = models.CharField(max_length=255) # 'content_generation', 'rag_retrieval'
    prompt_hash = models.CharField(max_length=64, db_index=True) # Para detectar duplicados y cachear
    
    # Métricas
    input_tokens = models.IntegerField()
    output_tokens = models.IntegerField()
    cost_usd = models.DecimalField(max_digits=10, decimal_places=6)
    latency_ms = models.IntegerField()
    
    success = models.BooleanField(default=True)
    error_detail = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
