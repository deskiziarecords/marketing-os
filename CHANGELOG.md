# Changelog

All notable changes to Marketing OS are documented here.

## [Unreleased]

### Added
- **Django Admin** — registered all models across every app (Tenant, Project,
  ProjectTemplate, Lead, ContentMaster, ContentVariant, PromptTemplate,
  DomainEvent, AIAuditLog) so the admin panel is usable out of the box
- **Tenants API router** (`/api/tenants/`) — two new endpoints:
  - `GET /api/tenants/templates/` — list all ProjectTemplates
  - `POST /api/tenants/projects/{id}/apply-template/{slug}/` — clone a
    template's prompts into a project's tenant
- **CRM test suite** (`tests/test_crm_api.py`) — 16 tests covering list
  (with tenant/project filters), create, get, partial update, and delete
  for the Lead endpoints
- **`config/settings/test.py`** — dedicated test settings that exclude
  `djstripe` to avoid importing the Stripe SDK during the test run
- **Root `conftest.py`** — early `ssl` import for Windows OpenSSL DLL
  load-order compatibility

### Fixed
- **`events/tasks.py`** — `select_for_update()` was called outside an
  `atomic()` block; on PostgreSQL this raises `TransactionManagementError`.
  The lock now wraps the queryset correctly. Added a `HANDLERS` dispatch
  table, structured logging, and `update_fields` on status saves
- **`ai/providers/service.py`** — moved `litellm` import inside the
  function body (lazy import). `aiohttp`, a `litellm` dependency, bundles
  OpenSSL C extensions that crash Python on Windows with
  `OPENSSL_Uplink: no OPENSSL_Applink` when loaded at module import time.
  With the lazy import, `litellm` is only loaded when an actual AI call is
  made — the test suite mocks the function, so it never crashes
- **`events/dispatcher.py`** — removed dead `create_lead()` function that
  referenced `Lead` without importing it (would `NameError` if called);
  kept only the Django Signal definitions

### Removed
- **`events/services.py`** — deleted; it was an exact duplicate of
  `events/publishers.py` and was never imported anywhere

### Infrastructure
- `pyproject.toml` — `DJANGO_SETTINGS_MODULE` switched to
  `config.settings.test` for pytest; `langsmith` pytest plugin disabled
  (not relevant to this test suite)
- `conftest.py` (root) — `import ssl` runs before any pytest plugin or
  conftest to set up Windows OpenSSL APPLINK pointers

---

## Earlier commits (pre-changelog)

| Commit | Summary |
|--------|---------|
| `904709d` | Add seed_templates.py with industry-specific ProjectTemplates |
| `0c1766f` | Add apps/tenants/services.py — apply_template_to_project |
| `8bf6b1b` | Update events/tasks.py — Celery Beat outbox worker |
| `af34020` | Update events/consumers.py — lead.created and ai.generation.completed handlers |
| `8541719` | Add create_lead service with Outbox event publishing |
| `5d52625` | Add Lead model to CRM domain |
| `083b348` | Refactor AI content generation and audit logging |
| `f5a0e99` | Add events/publishers.py — Outbox pattern publish_event |
| `28dd466` | Add ContentMaster, ContentVariant, PromptTemplate models |
| `8766952` | Add status field and choices to DomainEvent |
| `3f9b5e2` | Add DomainEvent model |
| `0c80f4a` | Add ai/providers/service.py — LiteLLM wrapper |
| `a67e777` | Add ai/audits/models.py — AIAuditLog |
| `b72a9a1` | Add DomainEvent model for event tracking |
| `4ed930b` | Add Makefile for project management |
| `b22c9ef` | Add pyproject.toml |
| `4cb5fdd` | Initial commit |
