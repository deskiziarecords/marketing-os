from django.contrib import admin
from ai.audits.models import AIAuditLog


@admin.register(AIAuditLog)
class AIAuditLogAdmin(admin.ModelAdmin):
    list_display = ["purpose", "model", "tenant", "success", "cost_usd", "latency_ms", "created_at"]
    list_filter = ["success", "model", "tenant"]
    search_fields = ["purpose", "error_detail"]
    readonly_fields = ["id", "created_at", "prompt_hash"]
