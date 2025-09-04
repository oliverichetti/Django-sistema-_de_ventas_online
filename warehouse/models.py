from django.db import models
from catalog.models import Producto, Variante
from orders.models import Orden

class MovimientoInventario(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    )
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variante = models.ForeignKey(Variante, null=True, blank=True, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    motivo = models.CharField(max_length=200)
    orden_relacionada = models.ForeignKey(Orden, null=True, blank=True, on_delete=models.SET_NULL)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_tipo_display()} de {self.cantidad} unidades de {self.producto.nombre}"

class Despacho(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE, related_name='despacho')
    fecha_despacho = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Despacho de orden #{self.orden.id}"
