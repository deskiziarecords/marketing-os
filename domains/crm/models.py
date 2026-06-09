# domains/crm/models.py
from django.db import models
from apps.tenants.models import Tenant, Project

class Lead(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='leads')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='leads')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    status = models.CharField(max_length=50, default='nuevo')
    created_at = models.DateTimeField(auto_now_add=True)
