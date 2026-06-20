# domains/content_factory/models.py
import uuid

from django.db import models

from apps.tenants.models import Tenant, Project


class ContentMaster(models.Model):
    """A piece of "source of truth" content from which platform variants are generated."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="content_masters")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="content_masters")
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Base / source-of-truth content")
    status = models.CharField(
        max_length=50,
        choices=[
            ("draft", "Borrador"),
            ("approved", "Aprobado"),
            ("archived", "Archivado"),
        ],
        default="draft",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "project", "title"],
                name="unique_master_per_project",
            ),
        ]

    def __str__(self):
        return self.title


class PromptTemplate(models.Model):
    """Reusable prompt templates for AI content generation."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="prompt_templates", null=True, blank=True
    )
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=10, default="v1.0")
    system_prompt = models.TextField()
    variables = models.JSONField(default=list, help_text='e.g. ["{{topic}}", "{{tone}}"]')
    task_type = models.CharField(max_length=100, default="creative_writing")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "-version"]

    def __str__(self):
        return f"{self.name} ({self.version})"


class ContentVariant(models.Model):
    """A platform-specific variant generated from a ContentMaster."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    master = models.ForeignKey(
        ContentMaster, on_delete=models.CASCADE, related_name="variants"
    )
    platform = models.CharField(
        max_length=50,
        choices=[
            ("instagram", "Instagram"),
            ("linkedin", "LinkedIn"),
            ("tiktok", "TikTok"),
            ("twitter", "Twitter / X"),
            ("facebook", "Facebook"),
            ("blog", "Blog"),
            ("email", "Email"),
        ],
    )
    generated_content = models.TextField()
    prompt_used = models.ForeignKey(
        PromptTemplate, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.platform} variant of {self.master.title}"
