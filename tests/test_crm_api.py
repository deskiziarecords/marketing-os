# tests/test_crm_api.py
import json
import uuid

import pytest
from unittest.mock import patch

pytestmark = pytest.mark.django_db

from domains.crm.models import Lead
from tests.factories import TenantFactory, ProjectFactory


@pytest.fixture(autouse=True)
def mock_crm_publish_event():
    with patch("domains.crm.services.publish_event") as mock:
        yield mock


# ===========================================================================
# Lead list
# ===========================================================================

class TestLeadList:
    def test_list_empty(self, client):
        response = client.get("/api/crm/leads/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_all(self, client, tenant, project):
        Lead.objects.create(tenant=tenant, project=project, name="A", email="a@x.com")
        Lead.objects.create(tenant=tenant, project=project, name="B", email="b@x.com")
        response = client.get("/api/crm/leads/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_list_filtered_by_tenant(self, client, tenant, project):
        Lead.objects.create(tenant=tenant, project=project, name="Mine", email="mine@x.com")
        other = TenantFactory()
        other_project = ProjectFactory(tenant=other)
        Lead.objects.create(tenant=other, project=other_project, name="Theirs", email="theirs@x.com")

        response = client.get(f"/api/crm/leads/?tenant_id={tenant.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Mine"

    def test_list_filtered_by_project(self, client, tenant, project):
        Lead.objects.create(tenant=tenant, project=project, name="P1", email="p1@x.com")
        other_project = ProjectFactory(tenant=tenant)
        Lead.objects.create(tenant=tenant, project=other_project, name="P2", email="p2@x.com")

        response = client.get(f"/api/crm/leads/?project_id={project.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "P1"


# ===========================================================================
# Lead create
# ===========================================================================

class TestLeadCreate:
    CREATE_URL = "/api/crm/leads/"

    def test_create(self, client, tenant, project):
        payload = {
            "name": "Juan Pérez",
            "email": "juan@example.com",
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
        assert data["name"] == "Juan Pérez"
        assert data["email"] == "juan@example.com"
        assert data["status"] == "nuevo"
        assert data["tenant_id"] == str(tenant.id)
        assert data["project_id"] == str(project.id)
        assert "id" in data

    def test_create_persists_to_db(self, client, tenant, project):
        payload = {
            "name": "María López",
            "email": "maria@example.com",
            "tenant_id": str(tenant.id),
            "project_id": str(project.id),
        }
        client.post(
            self.CREATE_URL,
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert Lead.objects.filter(email="maria@example.com").count() == 1

    def test_create_publishes_event(self, client, tenant, project, mock_crm_publish_event):
        payload = {
            "name": "Event Lead",
            "email": "event@example.com",
            "tenant_id": str(tenant.id),
            "project_id": str(project.id),
        }
        client.post(
            self.CREATE_URL,
            data=json.dumps(payload),
            content_type="application/json",
        )
        mock_crm_publish_event.assert_called_once()
        call_kwargs = mock_crm_publish_event.call_args
        assert call_kwargs.kwargs["event_type"] == "lead.created"

    def test_create_invalid_tenant_returns_404(self, client, project):
        payload = {
            "name": "Ghost",
            "email": "ghost@example.com",
            "tenant_id": str(uuid.uuid4()),
            "project_id": str(project.id),
        }
        response = client.post(
            self.CREATE_URL,
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_create_invalid_project_returns_404(self, client, tenant):
        payload = {
            "name": "Ghost",
            "email": "ghost@example.com",
            "tenant_id": str(tenant.id),
            "project_id": str(uuid.uuid4()),
        }
        response = client.post(
            self.CREATE_URL,
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == 404


# ===========================================================================
# Lead get
# ===========================================================================

class TestLeadGet:
    def test_get(self, client, tenant, project):
        lead = Lead.objects.create(
            tenant=tenant, project=project, name="Test", email="t@x.com"
        )
        response = client.get(f"/api/crm/leads/{lead.id}/")
        assert response.status_code == 200
        assert response.json()["name"] == "Test"

    def test_get_404(self, client):
        response = client.get(f"/api/crm/leads/{uuid.uuid4()}/")
        assert response.status_code == 404


# ===========================================================================
# Lead update
# ===========================================================================

class TestLeadUpdate:
    def test_partial_update_status(self, client, tenant, project):
        lead = Lead.objects.create(
            tenant=tenant, project=project, name="Test", email="t@x.com"
        )
        response = client.patch(
            f"/api/crm/leads/{lead.id}/",
            data=json.dumps({"status": "contactado"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response.json()["status"] == "contactado"

    def test_partial_update_name(self, client, tenant, project):
        lead = Lead.objects.create(
            tenant=tenant, project=project, name="Old Name", email="t@x.com"
        )
        response = client.patch(
            f"/api/crm/leads/{lead.id}/",
            data=json.dumps({"name": "New Name"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response.json()["name"] == "New Name"
        assert response.json()["email"] == "t@x.com"

    def test_update_404(self, client):
        response = client.patch(
            f"/api/crm/leads/{uuid.uuid4()}/",
            data=json.dumps({"status": "contactado"}),
            content_type="application/json",
        )
        assert response.status_code == 404


# ===========================================================================
# Lead delete
# ===========================================================================

class TestLeadDelete:
    def test_delete(self, client, tenant, project):
        lead = Lead.objects.create(
            tenant=tenant, project=project, name="Del", email="del@x.com"
        )
        response = client.delete(f"/api/crm/leads/{lead.id}/")
        assert response.status_code == 204
        assert Lead.objects.filter(id=lead.id).count() == 0

    def test_delete_404(self, client):
        response = client.delete(f"/api/crm/leads/{uuid.uuid4()}/")
        assert response.status_code == 404
