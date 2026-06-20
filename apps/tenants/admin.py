from django.contrib import admin
from apps.tenants.models import Tenant, Project, ProjectTemplate


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ["name", "subdomain", "created_at"]
    search_fields = ["name", "subdomain"]
    readonly_fields = ["id", "created_at"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "tenant"]
    list_filter = ["tenant"]
    search_fields = ["name", "tenant__name"]
    readonly_fields = ["id"]


@admin.register(ProjectTemplate)
class ProjectTemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    search_fields = ["name", "slug"]
    readonly_fields = ["id", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
