from django.db import models
from catalog.models import Producto, Variante
from promotions.models import Cupon

class Orden(models.Model):
    ESTADO_CHOICES = (
        ('PENDING', 'Pendiente'),
        ('PAID', 'Pagada'),
        ('READY_TO_SHIP', 'Lista para despachar'),
        ('DISPATCHED', 'Despachada'),
    )
    
    clave_session = models.CharField(max_length=255)
    nombre_envio = models.CharField(max_length=200)
    direccion_envio = models.TextField()
    telefono = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDING')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cupon = models.ForeignKey(Cupon, null=True, blank=True, on_delete=models.SET_NULL)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Orden #{self.id}"

class ItemOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variante = models.ForeignKey(Variante, null=True, blank=True, on_delete=models.SET_NULL)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total_linea = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
