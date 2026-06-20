# apps/tenants/models.py
import uuid
from django.db import models


class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.tenant.name})"


class ProjectTemplate(models.Model):
    """
    Master template for rapidly bootstrapping a project.
    Stores industry-specific config: pipelines, AI prompts, automation rules.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text="e.g. 'Despacho Laboral'")
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, default="")
    config = models.JSONField(
        default=dict,
        help_text=(
            "JSON estructura: {"
            '"pipelines": [...], '
            '"prompts": [{"name", "version", "system_prompt", "variables", "task_type"}], '
            '"automations": [{"name", "trigger_event", "actions"}]'
            "}"
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
