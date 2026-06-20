from django.contrib import admin
from domains.crm.models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "status", "tenant", "project", "created_at"]
    list_filter = ["status", "tenant", "project"]
    search_fields = ["name", "email"]
    readonly_fields = ["id", "created_at"]
