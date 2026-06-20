# tests/test_content_factory_api.py
import json
import uuid

import pytest

# Apply django_db to all tests in this module — every test hits the test DB
pytestmark = pytest.mark.django_db

from domains.content_factory.models import ContentMaster, ContentVariant, PromptTemplate
from tests.factories import (
    TenantFactory,
    ProjectFactory,
    PromptTemplateFactory,
    ContentMasterFactory,
    ContentVariantFactory,
)

# ===========================================================================
# PromptTemplate endpoints
# ===========================================================================


class TestPromptTemplateList:
    def test_list_empty(self, client):
        response = client.get("/api/content-factory/prompt-templates/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_all(self, client, tenant):
        PromptTemplateFactory.create_batch(3, tenant=tenant)
        response = client.get("/api/content-factory/prompt-templates/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    def test_list_filtered_by_tenant(self, client, tenant):
        PromptTemplateFactory.create_batch(2, tenant=tenant)
        other = TenantFactory()
        PromptTemplateFactory.create_batch(1, tenant=other)

        response = client.get(
            f"/api/content-factory/prompt-templates/?tenant_id={tenant.id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_includes_null_tenant(self, client, tenant):
        """Templates without a tenant should appear in unfiltered lists."""
        PromptTemplateFactory(tenant=None)
        response = client.get("/api/content-factory/prompt-templates/")
        assert response.status_code == 200
        assert len(response.json()) == 1


class TestPromptTemplateCreate:
    CREATE_URL = "/api/content-factory/prompt-templates/"

    def test_create_basic(self, client):
        payload = {
            "name": "Generador de Reels",
            "version": "v2.0",
            "system_prompt": "Eres un experto en Reels de Instagram.",
            "variables": ["{{tema}}"],
            "task_type": "creative_writing",
        }
        response = client.post(
            self.CREATE_URL,
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Generador de Reels"
        assert data["version"] == "v2.0"
        assert data["task_type"] == "creative_writing"
        assert data["tenant_id"] is None
        assert "id" in data

    def test_create_with_defaults(self, client):
        """Only required fields — version and task_type should use defaults."""
        payload = {
            "name": "Simple Prompt",
            "system_prompt": "Responde de forma útil.",
        }
        response = client.post(
            self.CREATE_URL,
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 201
        data = response.json()
        assert data["version"] == "v1.0"
        assert data["task_type"] == "creative_writing"
        assert data["variables"] == []

    def test_create_with_tenant(self, client, tenant):
        payload = {
            "name": "Template with Tenant",
            "system_prompt": "Prompt personalizado.",
            "tenant_id": str(tenant.id),
        }
        response = client.post(
            self.CREATE_URL,
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 201
        assert response.json()["tenant_id"] == str(tenant.id)

    def test_create_with_invalid_tenant_returns_404(self, client):
        payload = {
            "name": "Bad Tenant",
            "system_prompt": "Test",
            "tenant_id": str(uuid.uuid4()),
        }
        response = client.post(
            self.CREATE_URL,
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 404


class TestPromptTemplateGet:
    def test_get(self, client, prompt_template):
        response = client.get(
            f"/api/content-factory/prompt-templates/{prompt_template.id}/"
        )
        assert response.status_code == 200
        assert response.json()["name"] == prompt_template.name

    def test_get_404(self, client):
        response = client.get(
            f"/api/content-factory/prompt-templates/{uuid.uuid4()}/"
        )
        assert response.status_code == 404


class TestPromptTemplateUpdate:
    def test_partial_update(self, client, prompt_template):
        response = client.patch(
            f"/api/content-factory/prompt-templates/{prompt_template.id}/",
            data=json.dumps({"name": "Nombre Actualizado"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Nombre Actualizado"
        # Ensure other fields unchanged
        assert response.json()["version"] == prompt_template.version

    def test_update_system_prompt(self, client, prompt_template):
        response = client.patch(
            f"/api/content-factory/prompt-templates/{prompt_template.id}/",
            data=json.dumps({"system_prompt": "Nuevo system prompt."}),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response.json()["system_prompt"] == "Nuevo system prompt."

    def test_update_404(self, client):
        response = client.patch(
            f"/api/content-factory/prompt-templates/{uuid.uuid4()}/",
            data=json.dumps({"name": "Nope"}),
            content_type="application/json",
        )
        assert response.status_code == 404


class TestPromptTemplateDelete:
    def test_delete(self, client, prompt_template):
        response = client.delete(
            f"/api/content-factory/prompt-templates/{prompt_template.id}/"
        )
        assert response.status_code == 204
        # Verify it's actually gone
        assert PromptTemplate.objects.filter(id=prompt_template.id).count() == 0

    def test_delete_404(self, client):
        response = client.delete(
            f"/api/content-factory/prompt-templates/{uuid.uuid4()}/"
        )
        assert response.status_code == 404


# ===========================================================================
# ContentMaster endpoints
# ===========================================================================


class TestContentMasterList:
    def test_list_empty(self, client):
        response = client.get("/api/content-factory/masters/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_all(self, client, content_master):
        ContentMasterFactory.create_batch(2)
        response = client.get("/api/content-factory/masters/")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_list_filtered_by_tenant(self, client, tenant):
        ContentMasterFactory.create_batch(2, tenant=tenant)
        other = TenantFactory()
        ContentMasterFactory.create_batch(1, tenant=other)
        response = client.get(
            f"/api/content-factory/masters/?tenant_id={tenant.id}"
        )
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_list_filtered_by_project(self, client, tenant, project):
        ContentMasterFactory.create_batch(2, tenant=tenant, project=project)
        other = ProjectFactory(tenant=tenant)
        ContentMasterFactory.create_batch(1, tenant=tenant, project=other)
        response = client.get(
            f"/api/content-factory/masters/?project_id={project.id}"
        )
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_list_filtered_by_status(self, client, tenant, project):
        ContentMasterFactory(tenant=tenant, project=project, status="draft")
        ContentMasterFactory(tenant=tenant, project=project, status="approved")
        response = client.get(
            "/api/content-factory/masters/?status=approved"
        )
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["status"] == "approved"


class TestContentMasterCreate:
    CREATE_URL = "/api/content-factory/masters/"

    def test_create(self, client, tenant, project):
        payload = {
            "title": "10 Tips de Marketing Digital",
            "content": "El marketing digital ha evolucionado...",
            "tenant_id": str(tenant.id),
            "project_id": str(project.id),
        }
        response = client.post(
            self.CREATE_URL,
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "10 Tips de Marketing Digital"
        assert data["status"] == "draft"
        assert data["tenant_id"] == str(tenant.id)
        assert data["project_id"] == str(project.id)
        assert "id" in data

    def test_create_with_custom_status(self, client, tenant, project):
        payload = {
            "title": "Guía Completa",
            "content": "Contenido completo.",
            "tenant_id": str(tenant.id),
            "project_id": str(project.id),
            "status": "approved",
        }
        response = client.post(
            self.CREATE_URL,
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 201
        assert response.json()["status"] == "approved"

    def test_create_with_invalid_tenant_returns_404(self, client, project):
        payload = {
            "title": "Test",
            "content": "Test content",
            "tenant_id": str(uuid.uuid4()),
            "project_id": str(project.id),
        }
        response = client.post(
            self.CREATE_URL,
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_create_publishes_event(self, client, tenant, project, mock_publish_event):
        """Verify the service calls publish_event via the mocked publisher."""
        payload = {
            "title": "Test Event",
            "content": "Testing event publication.",
            "tenant_id": str(tenant.id),
            "project_id": str(project.id),
        }
        client.post(
            self.CREATE_URL,
            data=json.dumps(payload),
            content_type="application/json",
        )
        # publish_event should have been called once for master.created
        mock_publish_event.assert_called_once()


class TestContentMasterGet:
    def test_get(self, client, content_master):
        response = client.get(
            f"/api/content-factory/masters/{content_master.id}/"
        )
        assert response.status_code == 200
        assert response.json()["title"] == content_master.title

    def test_get_404(self, client):
        response = client.get(
            f"/api/content-factory/masters/{uuid.uuid4()}/"
        )
        assert response.status_code == 404


class TestContentMasterUpdate:
    def test_partial_update(self, client, content_master):
        response = client.patch(
            f"/api/content-factory/masters/{content_master.id}/",
            data=json.dumps({"title": "Título Actualizado"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Título Actualizado"

    def test_update_status(self, client, content_master):
        response = client.patch(
            f"/api/content-factory/masters/{content_master.id}/",
            data=json.dumps({"status": "approved"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response.json()["status"] == "approved"

    def test_update_404(self, client):
        response = client.patch(
            f"/api/content-factory/masters/{uuid.uuid4()}/",
            data=json.dumps({"title": "Nope"}),
            content_type="application/json",
        )
        assert response.status_code == 404


class TestContentMasterDelete:
    def test_delete(self, client, content_master):
        response = client.delete(
            f"/api/content-factory/masters/{content_master.id}/"
        )
        assert response.status_code == 204
        assert ContentMaster.objects.filter(id=content_master.id).count() == 0

    def test_delete_cascades_to_variants(self, client, content_master):
        """Deleting a master should delete all its variants."""
        ContentVariantFactory.create_batch(3, master=content_master)
        assert ContentVariant.objects.filter(master=content_master).count() == 3

        client.delete(f"/api/content-factory/masters/{content_master.id}/")
        assert ContentVariant.objects.filter(master=content_master).count() == 0

    def test_delete_404(self, client):
        response = client.delete(
            f"/api/content-factory/masters/{uuid.uuid4()}/"
        )
        assert response.status_code == 404


# ===========================================================================
# ContentVariant endpoints
# ===========================================================================


class TestContentVariantList:
    def test_list_empty(self, client, content_master):
        response = client.get(
            f"/api/content-factory/masters/{content_master.id}/variants/"
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_list_for_master(self, client, content_master):
        ContentVariantFactory.create_batch(2, master=content_master)
        response = client.get(
            f"/api/content-factory/masters/{content_master.id}/variants/"
        )
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_list_isolated_per_master(self, client):
        """Variants from one master should not leak into another master's list."""
        m1 = ContentMasterFactory()
        m2 = ContentMasterFactory()
        ContentVariantFactory(master=m1)
        ContentVariantFactory.create_batch(2, master=m2)

        response = client.get(
            f"/api/content-factory/masters/{m1.id}/variants/"
        )
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_list_master_404(self, client):
        response = client.get(
            f"/api/content-factory/masters/{uuid.uuid4()}/variants/"
        )
        assert response.status_code == 404


class TestContentVariantGenerate:
    GENERATE_URL = lambda self, master_id: f"/api/content-factory/masters/{master_id}/variants/generate/"  # noqa: E731

    def test_generate_variant(self, client, content_master, mock_ai_provider):
        """Generate a variant — AI provider should be called and a variant created."""
        response = client.post(
            self.GENERATE_URL(content_master.id),
            data=json.dumps({"platform": "instagram"}),
            content_type="application/json",
        )
        assert response.status_code == 201, response.json()
        data = response.json()
        assert data["platform"] == "instagram"
        assert data["generated_content"] == "Contenido generado por IA mockeada para pruebas."
        assert data["master_id"] == str(content_master.id)
        assert "id" in data

        # Verify the mock was called
        mock_ai_provider.assert_called_once()

        # Verify the variant is persisted
        assert ContentVariant.objects.filter(id=data["id"]).count() == 1

    def test_generate_variant_notifies_publisher(
        self, client, content_master, mock_publish_event
    ):
        """Verify the generate service calls publish_event."""
        client.post(
            self.GENERATE_URL(content_master.id),
            data=json.dumps({"platform": "linkedin"}),
            content_type="application/json",
        )
        # Should have at least one publish_event call (content.variant.generated)
        assert mock_publish_event.call_count >= 1

    def test_generate_with_prompt_template(
        self, client, content_master, prompt_template, mock_ai_provider
    ):
        """Generate a variant with a specific prompt template reference."""
        response = client.post(
            self.GENERATE_URL(content_master.id),
            data=json.dumps({
                "platform": "tiktok",
                "prompt_template_id": str(prompt_template.id),
            }),
            content_type="application/json",
        )
        assert response.status_code == 201
        assert response.json()["platform"] == "tiktok"

    def test_generate_with_invalid_prompt_template(self, client, content_master):
        """Referencing a non-existent prompt template should return 404."""
        response = client.post(
            self.GENERATE_URL(content_master.id),
            data=json.dumps({
                "platform": "instagram",
                "prompt_template_id": str(uuid.uuid4()),
            }),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_generate_invalid_platform(self, client, content_master):
        """An invalid platform value should return 422."""
        response = client.post(
            self.GENERATE_URL(content_master.id),
            data=json.dumps({"platform": "myspace"}),
            content_type="application/json",
        )
        assert response.status_code == 422

    def test_generate_master_404(self, client):
        response = client.post(
            self.GENERATE_URL(uuid.uuid4()),
            data=json.dumps({"platform": "instagram"}),
            content_type="application/json",
        )
        assert response.status_code == 404


class TestContentVariantGet:
    def test_get_variant(self, client, content_variant):
        response = client.get(
            f"/api/content-factory/variants/{content_variant.id}/"
        )
        assert response.status_code == 200
        assert response.json()["id"] == str(content_variant.id)

    def test_get_variant_404(self, client):
        response = client.get(
            f"/api/content-factory/variants/{uuid.uuid4()}/"
        )
        assert response.status_code == 404
