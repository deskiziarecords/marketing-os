from django.contrib import admin
from domains.content_factory.models import ContentMaster, ContentVariant, PromptTemplate


@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "version", "task_type", "tenant", "created_at"]
    list_filter = ["task_type", "tenant"]
    search_fields = ["name", "system_prompt"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(ContentMaster)
class ContentMasterAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "tenant", "project", "created_at"]
    list_filter = ["status", "tenant", "project"]
    search_fields = ["title", "content"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(ContentVariant)
class ContentVariantAdmin(admin.ModelAdmin):
    list_display = ["__str__", "platform", "master", "created_at"]
    list_filter = ["platform"]
    search_fields = ["generated_content", "master__title"]
    readonly_fields = ["id", "created_at"]
