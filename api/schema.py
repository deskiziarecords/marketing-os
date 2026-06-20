# api/schema.py
from ninja import NinjaAPI

api = NinjaAPI(
    title="Marketing OS API",
    version="0.1.0",
    description="Marketing Operating System SaaS — CRM and Content Factory APIs",
    docs_url="/docs/",
)

# Register routers
from api.rest.crm import router as crm_router  # noqa: E402
from api.rest.content_factory import router as content_factory_router  # noqa: E402
from api.rest.tenants import router as tenants_router  # noqa: E402

api.add_router("/crm", crm_router, tags=["CRM"])
api.add_router("/content-factory", content_factory_router, tags=["Content Factory"])
api.add_router("/tenants", tenants_router, tags=["Tenants"])
