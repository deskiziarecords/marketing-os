from django.contrib import admin
from events.models import DomainEvent


@admin.register(DomainEvent)
class DomainEventAdmin(admin.ModelAdmin):
    list_display = ["event_type", "status", "attempts", "tenant_id", "created_at", "processed_at"]
    list_filter = ["status", "event_type"]
    search_fields = ["event_type", "error_message"]
    readonly_fields = ["id", "created_at", "processed_at"]
