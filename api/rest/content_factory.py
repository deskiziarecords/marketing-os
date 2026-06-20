# api/rest/content_factory.py
from datetime import datetime
from enum import Enum
from uuid import UUID
from typing import List, Optional

from django.shortcuts import get_object_or_404
from ninja import Router, Schema

from apps.tenants.models import Tenant, Project
from domains.content_factory.models import ContentMaster, ContentVariant, PromptTemplate
from domains.content_factory.services import create_content_master, generate_variant

router = Router()


class PlatformEnum(str, Enum):
    instagram = "instagram"
    linkedin = "linkedin"
    tiktok = "tiktok"
    twitter = "twitter"
    facebook = "facebook"
    blog = "blog"
    email = "email"

# ---------------------------------------------------------------------------
# Schemas — PromptTemplate
# ---------------------------------------------------------------------------

class PromptTemplateCreate(Schema):
    name: str
    version: Optional[str] = "v1.0"
    system_prompt: str
    variables: Optional[list] = None
    task_type: Optional[str] = "creative_writing"
    tenant_id: Optional[UUID] = None


class PromptTemplateUpdate(Schema):
    name: Optional[str] = None
    version: Optional[str] = None
    system_prompt: Optional[str] = None
    variables: Optional[list] = None
    task_type: Optional[str] = None


class PromptTemplateOut(Schema):
    id: UUID
    name: str
    version: str
    system_prompt: str
    variables: list
    task_type: str
    tenant_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

# ---------------------------------------------------------------------------
# Schemas — ContentMaster
# ---------------------------------------------------------------------------

class ContentMasterCreate(Schema):
    title: str
    content: str
    tenant_id: UUID
    project_id: UUID
    status: Optional[str] = "draft"


class ContentMasterUpdate(Schema):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None


class ContentMasterOut(Schema):
    id: UUID
    title: str
    content: str
    status: str
    tenant_id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime

# ---------------------------------------------------------------------------
# Schemas — ContentVariant
# ---------------------------------------------------------------------------

class ContentVariantOut(Schema):
    id: UUID
    master_id: UUID
    platform: str
    generated_content: str
    created_at: datetime


class ContentVariantGenerateIn(Schema):
    platform: PlatformEnum
    prompt_template_id: Optional[UUID] = None

# ---------------------------------------------------------------------------
# Schemas — Shared
# ---------------------------------------------------------------------------

class ErrorOut(Schema):
    detail: str

# ===========================================================================
# Endpoints — PromptTemplates
# ===========================================================================

@router.get("/prompt-templates/", response=List[PromptTemplateOut])
def list_prompt_templates(request, tenant_id: Optional[UUID] = None):
    """List prompt templates, optionally filtered by tenant."""
    qs = PromptTemplate.objects.all()
    if tenant_id:
        qs = qs.filter(tenant_id=tenant_id)
    return list(qs)


@router.post("/prompt-templates/", response={201: PromptTemplateOut, 400: ErrorOut})
def create_prompt_template(request, payload: PromptTemplateCreate):
    """Create a new prompt template."""
    data = payload.dict(exclude_unset=True)
    # Resolve tenant FK if provided
    tenant = None
    if data.get("tenant_id"):
        tenant = get_object_or_404(Tenant, id=data.pop("tenant_id"))
    if data.get("variables") is None:
        data["variables"] = []
    template = PromptTemplate.objects.create(tenant=tenant, **data)
    return 201, template


@router.get("/prompt-templates/{template_id}/", response=PromptTemplateOut)
def get_prompt_template(request, template_id: UUID):
    """Get a single prompt template by ID."""
    return get_object_or_404(PromptTemplate, id=template_id)


@router.patch(
    "/prompt-templates/{template_id}/",
    response={200: PromptTemplateOut, 404: ErrorOut},
)
def update_prompt_template(request, template_id: UUID, payload: PromptTemplateUpdate):
    """Update a prompt template's fields (partial update)."""
    template = get_object_or_404(PromptTemplate, id=template_id)
    update_data = payload.dict(exclude_unset=True)
    for attr, value in update_data.items():
        setattr(template, attr, value)
    template.save()
    return template


@router.delete(
    "/prompt-templates/{template_id}/",
    response={204: None, 404: ErrorOut},
)
def delete_prompt_template(request, template_id: UUID):
    """Delete a prompt template."""
    template = get_object_or_404(PromptTemplate, id=template_id)
    template.delete()
    return 204, None

# ===========================================================================
# Endpoints — ContentMasters
# ===========================================================================

@router.get("/masters/", response=List[ContentMasterOut])
def list_masters(
    request,
    tenant_id: Optional[UUID] = None,
    project_id: Optional[UUID] = None,
    status: Optional[str] = None,
):
    """List content masters, filterable by tenant, project, and status."""
    qs = ContentMaster.objects.all()
    if tenant_id:
        qs = qs.filter(tenant_id=tenant_id)
    if project_id:
        qs = qs.filter(project_id=project_id)
    if status:
        qs = qs.filter(status=status)
    return list(qs)


@router.post("/masters/", response={201: ContentMasterOut, 400: ErrorOut})
def create_master(request, payload: ContentMasterCreate):
    """Create a new content master. Publishes a 'content.master.created' event."""
    tenant = get_object_or_404(Tenant, id=payload.tenant_id)
    project = get_object_or_404(Project, id=payload.project_id)

    master = create_content_master(
        title=payload.title,
        content=payload.content,
        tenant=tenant,
        project=project,
        status=payload.status,
    )
    return 201, master


@router.get("/masters/{master_id}/", response=ContentMasterOut)
def get_master(request, master_id: UUID):
    """Get a single content master by ID."""
    return get_object_or_404(ContentMaster, id=master_id)


@router.patch("/masters/{master_id}/", response={200: ContentMasterOut, 404: ErrorOut})
def update_master(request, master_id: UUID, payload: ContentMasterUpdate):
    """Update a content master's fields (partial update)."""
    master = get_object_or_404(ContentMaster, id=master_id)
    update_data = payload.dict(exclude_unset=True)
    for attr, value in update_data.items():
        setattr(master, attr, value)
    master.save()
    return master


@router.delete("/masters/{master_id}/", response={204: None, 404: ErrorOut})
def delete_master(request, master_id: UUID):
    """Delete a content master and all its variants."""
    master = get_object_or_404(ContentMaster, id=master_id)
    master.delete()
    return 204, None

# ===========================================================================
# Endpoints — ContentVariants
# ===========================================================================

@router.get("/masters/{master_id}/variants/", response=List[ContentVariantOut])
def list_variants(request, master_id: UUID):
    """List all variants for a given content master."""
    master = get_object_or_404(ContentMaster, id=master_id)
    return list(master.variants.all())


@router.post(
    "/masters/{master_id}/variants/generate/",
    response={201: ContentVariantOut, 400: ErrorOut},
)
def generate_variant_endpoint(request, master_id: UUID, payload: ContentVariantGenerateIn):
    """Generate an AI-powered variant for a content master on a given platform.

    This calls the AI provider, logs the audit trail, publishes Outbox events
    for billing, and returns the generated variant.
    """
    master = get_object_or_404(ContentMaster, id=master_id)

    # Resolve optional prompt template
    prompt_template = None
    if payload.prompt_template_id:
        prompt_template = get_object_or_404(
            PromptTemplate, id=payload.prompt_template_id
        )

    variant = generate_variant(
        master=master,
        platform=payload.platform,
        tenant=master.tenant,
        project=master.project,
        prompt_template=prompt_template,
    )
    return 201, variant


@router.get("/variants/{variant_id}/", response=ContentVariantOut)
def get_variant(request, variant_id: UUID):
    """Get a single variant by ID."""
    return get_object_or_404(ContentVariant.objects.select_related("master"), id=variant_id)
