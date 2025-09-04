
from django.db import models
from catalog.models import Producto, Variante
from promotions.models import Cupon

class Carrito(models.Model):
    @property
    def descuento(self):
        total = sum(item.subtotal for item in self.items.all())
        if self.cupon and self.cupon.es_valido():
            if self.cupon.tipo_descuento == 'porcentaje':
                return total * (self.cupon.monto / 100)
            elif self.cupon.tipo_descuento == 'fijo':
                return min(self.cupon.monto, total)
        return 0
    clave_session = models.CharField(max_length=255, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cupon = models.ForeignKey('promotions.Cupon', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"Carrito {self.id}"
    
    @property
    def total(self):
        total = sum(item.subtotal for item in self.items.all())
        if self.cupon and self.cupon.es_valido():
            if self.cupon.tipo_descuento == 'porcentaje':
                total = total * (1 - self.cupon.monto / 100)
            elif self.cupon.tipo_descuento == 'fijo':
                total = max(total - self.cupon.monto, 0)
        return total

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variante = models.ForeignKey(Variante, null=True, blank=True, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
