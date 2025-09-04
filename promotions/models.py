from django.db import models

class Cupon(models.Model):
    def es_valido(self):
        from django.utils import timezone
        if not self.activo:
            return False
        if self.valido_hasta and timezone.now() > self.valido_hasta:
            return False
        if self.valido_desde and timezone.now() < self.valido_desde:
            return False
        return True
    TIPO_CHOICES = (
        ('porcentaje', 'Descuento por porcentaje'),
        ('fijo', 'Descuento fijo'),
    )
    
    codigo = models.CharField(max_length=50, unique=True)
    tipo_descuento = models.CharField(max_length=20, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)  # Porcentaje o monto fijo
    activo = models.BooleanField(default=True)
    valido_desde = models.DateTimeField()
    valido_hasta = models.DateTimeField()
    total_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return self.codigo
    
    def calcular_descuento(self, total):
        if total < self.total_minimo:
            return 0
        
        if self.tipo_descuento == 'porcentaje':
            return total * (self.monto / 100)
        else:  # fijo
            return min(self.monto, total)  # El descuento no puede ser mayor que el total
