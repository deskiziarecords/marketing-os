# tests/conftest.py
import ssl  # must be imported before cryptography on Windows to set up OpenSSL APPLINK
import uuid
from unittest.mock import patch

import pytest
from django.test import Client

from tests.factories import (
    TenantFactory,
    ProjectFactory,
    PromptTemplateFactory,
    ContentMasterFactory,
    ContentVariantFactory,
)


# ---------------------------------------------------------------------------
# Global mocks — applied to every test
#
# NOTE: We patch the *consumer* references, not the definition module.
# The services do `from events.publishers import publish_event` and
# `from ai.providers.service import generate_ai_content`, which creates
# local references. Patching the definition module alone won't affect
# those already-imported local references.
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def mock_ai_provider():
    """Mock the AI content generation provider so no real API calls are made."""
    with patch("domains.content_factory.services.generate_ai_content") as mock:
        mock.return_value = "Contenido generado por IA mockeada para pruebas."
        yield mock


@pytest.fixture(autouse=True)
def mock_publish_event():
    """
    Mock event publishing so no DomainEvent records are created in tests.

    The AI provider is already mocked by `mock_ai_provider`, so we only
    need to patch the consumer reference in the content factory service.
    """
    with patch("domains.content_factory.services.publish_event") as mock:
        yield mock


# ---------------------------------------------------------------------------
# Django test client
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    """Return a Django test client configured to hit the API."""
    return Client()


# ---------------------------------------------------------------------------
# Multi-tenant fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tenant():
    return TenantFactory()


@pytest.fixture
def project(tenant):
    return ProjectFactory(tenant=tenant)


# ---------------------------------------------------------------------------
# Content Factory fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def prompt_template(tenant):
    return PromptTemplateFactory(tenant=tenant)


@pytest.fixture
def prompt_template_no_tenant():
    return PromptTemplateFactory(tenant=None)


@pytest.fixture
def content_master(tenant, project):
    return ContentMasterFactory(tenant=tenant, project=project)


@pytest.fixture
def content_variant(content_master):
    return ContentVariantFactory(master=content_master)
