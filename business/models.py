# business/models.py
class Oferta(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='ofertas')
    TIPO_CHOICES = [('producto', 'Producto'), ('servicio', 'Servicio')]
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    nombre = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    promocion = models.TextField(blank=True, null=True)

class PublicoObjetivo(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='publicos')
    cliente_ideal = models.CharField(max_length=255)
    problemas = models.TextField()
    objetivos = models.TextField()
    miedos = models.TextField()
