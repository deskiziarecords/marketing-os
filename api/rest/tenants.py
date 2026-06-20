# api/rest/tenants.py
from uuid import UUID
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Schema

from apps.tenants.models import Tenant, Project, ProjectTemplate
from apps.tenants.services import apply_template_to_project

router = Router()


class TenantOut(Schema):
    id: UUID
    name: str
    subdomain: str


class ProjectOut(Schema):
    id: UUID
    name: str
    tenant_id: UUID


class ProjectTemplateOut(Schema):
    id: UUID
    name: str
    slug: str
    description: str


class ErrorOut(Schema):
    detail: str


@router.get("/templates/", response=List[ProjectTemplateOut])
def list_project_templates(request):
    """List all available project templates."""
    return list(ProjectTemplate.objects.all())


@router.post(
    "/projects/{project_id}/apply-template/{template_slug}/",
    response={200: ProjectOut, 404: ErrorOut},
)
def apply_template(request, project_id: UUID, template_slug: str):
    """
    Apply a ProjectTemplate to a Project.
    Clones the template's PromptTemplates into the project's tenant.
    """
    project = get_object_or_404(Project, id=project_id)
    template = get_object_or_404(ProjectTemplate, slug=template_slug)
    apply_template_to_project(project=project, template=template)
    return project
