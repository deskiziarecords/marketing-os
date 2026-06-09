# content_factory/models.py
class PromptTemplate(models.Model):
    nombre = models.CharField(max_length=100) # ej: "Generador de Reels v2"
    version = models.CharField(max_length=10, default="v1.0")
    system_prompt = models.TextField()
    variables_requeridas = models.JSONField() # ["{{tema}}", "{{tono}}"]
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, null=True, blank=True)

class ContentMaster(models.Model):
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    tema_central = models.CharField(max_length=255)
    contenido_base = models.TextField() # El "Source of Truth"
    estado = models.CharField(max_length=50, default='borrador')

class ContentVariant(models.Model):
    master = models.ForeignKey(ContentMaster, on_delete=models.CASCADE, related_name='variantes')
    plataforma = models.CharField(max_length=50) # instagram, linkedin, etc.
    contenido_generado = models.TextField()
    prompt_usado = models.ForeignKey(PromptTemplate, on_delete=models.SET_NULL, null=True)
