from django.db import models
from django.utils.text import slugify

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategorias')
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    destacado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.URLField(max_length=500, blank=True)
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.URLField(max_length=500, blank=True)
    texto_alternativo = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

class Variante(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='variantes')
    nombre = models.CharField(max_length=100)  # Ej: "Talla M", "Color Rojo"
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.nombre}"

class ItemStock(models.Model):
    producto = models.ForeignKey(Producto, null=True, blank=True, on_delete=models.CASCADE)
    variante = models.ForeignKey(Variante, null=True, blank=True, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        if self.variante:
            return f"Stock: {self.variante} - {self.cantidad} unidades"
        return f"Stock: {self.producto.nombre} - {self.cantidad} unidades"
