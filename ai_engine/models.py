# ai_engine/models.py
class AIAuditLog(models.Model):
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    # Detalles de la ejecución
    modelo = models.CharField(max_length=100) # "gpt-4o", "claude-3-5-sonnet"
    proposito = models.CharField(max_length=255) # "Generar variante instagram"
    
    # Auditoría
    prompt_enviado = models.TextField()
    respuesta_recibida = models.TextField()
    accion_tomada = models.CharField(max_length=255, blank=True) # "Guardado en ContentVariant"
    
    # Costos (Crítico para SaaS)
    input_tokens = models.IntegerField()
    output_tokens = models.IntegerField()
    costo_estimado_usd = models.DecimalField(max_digits=10, decimal_places=6)
    
    fecha = models.DateTimeField(auto_now_add=True)
