# api/rest/crm.py
from datetime import datetime
from uuid import UUID
from typing import List, Optional

from django.shortcuts import get_object_or_404
from ninja import Router, Schema

from domains.crm.models import Lead
from domains.crm.services import create_lead
from apps.tenants.models import Tenant, Project

router = Router()

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class LeadCreate(Schema):
    name: str
    email: str
    tenant_id: UUID
    project_id: UUID


class LeadUpdate(Schema):
    name: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None


class LeadOut(Schema):
    id: UUID
    name: str
    email: str
    status: str
    tenant_id: UUID
    project_id: UUID
    created_at: datetime


class ErrorOut(Schema):
    detail: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/leads/", response=List[LeadOut])
def list_leads(request, tenant_id: Optional[UUID] = None, project_id: Optional[UUID] = None):
    """List leads, optionally filtered by tenant and/or project."""
    queryset = Lead.objects.select_related("tenant", "project").all()
    if tenant_id:
        queryset = queryset.filter(tenant_id=tenant_id)
    if project_id:
        queryset = queryset.filter(project_id=project_id)
    return list(queryset)


@router.post("/leads/", response={201: LeadOut, 400: ErrorOut})
def create_lead_endpoint(request, payload: LeadCreate):
    """Create a new lead. Publishes a 'lead.created' event via the Outbox pattern."""
    tenant = get_object_or_404(Tenant, id=payload.tenant_id)
    project = get_object_or_404(Project, id=payload.project_id)

    lead = create_lead(
        name=payload.name,
        email=payload.email,
        tenant=tenant,
        project=project,
    )
    return 201, lead


@router.get("/leads/{lead_id}/", response=LeadOut)
def get_lead(request, lead_id: UUID):
    """Get a single lead by ID."""
    return get_object_or_404(Lead.objects.select_related("tenant", "project"), id=lead_id)


@router.patch("/leads/{lead_id}/", response={200: LeadOut, 404: ErrorOut})
def update_lead(request, lead_id: UUID, payload: LeadUpdate):
    """Update a lead's fields (partial update)."""
    lead = get_object_or_404(Lead, id=lead_id)
    update_data = payload.dict(exclude_unset=True)
    for attr, value in update_data.items():
        setattr(lead, attr, value)
    lead.save()
    return lead


@router.delete("/leads/{lead_id}/", response={204: None, 404: ErrorOut})
def delete_lead(request, lead_id: UUID):
    """Delete a lead."""
    lead = get_object_or_404(Lead, id=lead_id)
    lead.delete()
    return 204, None
