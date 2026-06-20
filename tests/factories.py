# tests/factories.py
import factory
from factory.django import DjangoModelFactory

from apps.tenants.models import Tenant, Project
from domains.content_factory.models import ContentMaster, ContentVariant, PromptTemplate


class TenantFactory(DjangoModelFactory):
    class Meta:
        model = Tenant

    name = factory.Faker("company")
    subdomain = factory.Sequence(lambda n: f"tenant-{n}")


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    tenant = factory.SubFactory(TenantFactory)
    name = factory.Faker("catch_phrase")


class PromptTemplateFactory(DjangoModelFactory):
    class Meta:
        model = PromptTemplate

    name = factory.Sequence(lambda n: f"Prompt Template {n}")
    version = "v1.0"
    system_prompt = factory.Faker("paragraph")
    variables = ["{{topic}}", "{{tone}}"]
    task_type = "creative_writing"
    tenant = None


class ContentMasterFactory(DjangoModelFactory):
    class Meta:
        model = ContentMaster

    tenant = factory.SubFactory(TenantFactory)
    project = factory.SubFactory(ProjectFactory)
    title = factory.Faker("catch_phrase")
    content = factory.Faker("paragraph")
    status = "draft"


class ContentVariantFactory(DjangoModelFactory):
    class Meta:
        model = ContentVariant

    master = factory.SubFactory(ContentMasterFactory)
    platform = factory.Iterator(["instagram", "linkedin", "tiktok", "twitter", "facebook", "blog", "email"])
    generated_content = factory.Faker("paragraph")
    prompt_used = None
