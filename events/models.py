# events/models.py
import uuid
from django.db import models
from django.utils import timezone


class DomainEvent(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("processing", "Procesando"),
        ("completed", "Completado"),
        ("failed", "Fallido"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_type = models.CharField(
        max_length=100, db_index=True
    )  # ej: 'lead.created', 'ai.generation.completed'

    # Contexto (Crucial para multi-tenant)
    tenant_id = models.UUIDField(null=True, blank=True, db_index=True)
    project_id = models.UUIDField(null=True, blank=True, db_index=True)

    payload = models.JSONField()  # El estado del objeto o datos relevantes

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", db_index=True
    )
    attempts = models.IntegerField(default=0)
    error_message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(
                fields=["status", "created_at"]
            ),  # Optimiza la consulta del worker
        ]

    def __str__(self):
        return f"{self.event_type} ({self.status})"
