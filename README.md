# marketing-os


``` plain
marketing_os/
│
├── .python-version              # "3.12" (uv lee esto para gestionar la versión)
├── pyproject.toml               # Dependencias y configuración (uv sync)
├── uv.lock                      # Lockfile de versiones exactas
├── Makefile                     # Comandos nativos: make run, make migrate, make worker
├── .env.example                 # Plantilla de variables de entorno
├── README.md                    # Guía de inicio rápido
│
├── config/                      #  Configuración Global de Django
│   ├── __init__.py
│   ├── settings/
│   │   ├── base.py              # Settings comunes (DB, Apps instaladas, Middlewares)
│   │   ├── local.py             # Settings de desarrollo (Debug=True, SQLite/Postgres local)
│   │   └── production.py        # Settings de prod (AWS, Seguridad, Redis, PGVector)
│   ├── urls.py                  # Enrutador principal (incluye api/urls.py)
│   ├── celery.py                # Configuración del worker de Celery
│   ├── asgi.py                  # WebSockets (opcional, para notificaciones en tiempo real)
│   └── wsgi.py                  # Entry point para Gunicorn
│
├── apps/                        #  Cimientos Transversales del SaaS
│   ├── core/                    # Excepciones custom, mixins, utilidades globales
│   ├── users/                   # Modelo User custom, Roles, Permisos, Auth
│   ├── tenants/                 # Multi-tenancy, White Label, Project Templates
│   └── billing/                 # Plan, Subscription, Invoice, Usage (Metered Billing)
│
├── domains/                     #  Lógica de Negocio Pura (Domain-Driven Design)
│   ├── business/                # Empresa, Oferta, Público Objetivo
│   ├── content/                 # Ideas, Content Master, Variantes, Calendario
│   ├── campaigns/               # Campaña, Presupuesto, KPIs, Canales (Agrupador de contenido)
│   ├── crm/                     # Leads, Pipeline, Touchpoints, Atribución de Ventas
│   ├── automation/              # Reglas, Secuencias, Marketplace de flujos
│   ├── publishing/              # Scheduler, Colas de publicación en redes
│   ├── analytics/               # Agregación de métricas, Dashboards, ROI
│   ├── knowledge/               # RAG: sources, chunks, embeddings, collections, retrieval
│   └── media_library/           # Asset, AssetVersion, Collection, Tag (S3/Cloudinary)
│
├── ai/                          #  Motor de Inteligencia Artificial (Aislado)
│   ├── providers/               # Wrappers unificados (LiteLLM, OpenAI, Anthropic)
│   ├── routing/                 # Lógica para elegir el modelo según la tarea (GPT-4o vs Claude)
│   ├── prompts/                 # Archivos YAML/JSON versionados (v1, v2, v3)
│   ├── agents/                  # Lógica de agentes autónomos (LangChain/LlamaIndex)
│   ├── memory/                  # Gestión de contexto e historial de conversaciones
│   ├── embeddings/              # Generación y gestión de vectores
│   ├── vectorstores/            # Interfaz con pgvector / Qdrant / Chroma
│   ├── evaluations/             # Evaluación de calidad de respuestas (LLM-as-a-judge)
│   └── audits/                  # Modelos: AIAuditLog (tokens, costo, latency, success)
│
├── integrations/                #  Adaptadores de Servicios Externos (Puertos)
│   ├── meta/                    # Graph API (Facebook, Instagram, WhatsApp)
│   ├── linkedin/                # LinkedIn API
│   ├── tiktok/                  # TikTok API
│   ├── google/                  # Google Business, YouTube, Analytics
│   ├── stripe/                  # Webhooks y gestión de pagos
│   └── twilio/                  # SMS / WhatsApp fallback
│
├── events/                      #  Sistema Nervioso (Event Bus + Outbox Pattern)
│   ├── models.py                # DomainEvent (Outbox: pending, processing, completed, failed)
│   ├── schemas.py               # Definición de payloads de eventos (Pydantic models)
│   ├── publishers.py            # Función: publish_event() (guarda en Outbox)
│   ├── consumers.py             # Handlers que escuchan y reaccionan (ej: handle_ai_generation_completed)
│   └── tasks.py                 # Tarea Celery Beat: process_pending_events() (con select_for_update)
│
├── api/                         #  Capa de Exposición de Datos
│   ├── rest/                    # Endpoints Django Ninja (CRUD de dominios)
│   └── webhooks/                # Endpoints públicos para recibir eventos de Meta, Stripe, etc.
│
├── tests/                       #  Tests Globales
│   ├── factories.py             # Factory Boy para generar datos de prueba
│   └── conftest.py              # Fixtures de pytest
│
├── scripts/                     #  Utilidades de Mantenimiento
│   ├── seed_templates.py        # Carga inicial de Plantillas de Proyecto (Clínica, Legal, etc.)
│   └── retry_failed_events.py   # Comando para reprocesar eventos fallidos del Outbox
│
└── docs/                        #  Documentación
    ├── architecture.md          # Este mismo árbol y decisiones de diseño
    └── api.md                   # Documentación de endpoints
