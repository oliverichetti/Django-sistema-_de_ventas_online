import json
from django.core.management.base import BaseCommand
from catalog.models import Producto, Categoria
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Importa productos desde productos.json a la base de datos'

    def handle(self, *args, **kwargs):
        with open('productos.json', 'r', encoding='utf-8') as f:
            productos = json.load(f)
        for prod in productos:
            categoria_nombre = prod.get('categoria', 'Sin categoría')
            categoria, _ = Categoria.objects.get_or_create(nombre=categoria_nombre, defaults={'slug': slugify(categoria_nombre)})
            producto, created = Producto.objects.get_or_create(
                nombre=prod['nombre'],
                defaults={
                    'slug': slugify(prod['nombre']),
                    'descripcion': prod.get('detalles', ''),
                    'precio': prod.get('precio_venta', 0),
                    'categoria': categoria,
                    'destacado': False,
                    'activo': True,
                    'imagen': prod.get('imagen', '')
                }
            )
            # Actualizar imagen principal si el producto ya existe y no tiene imagen
            imagen_url = prod.get('imagen')
            if imagen_url:
                if not producto.imagen:
                    producto.imagen = imagen_url
                    producto.save()
                from catalog.models import ImagenProducto
                # Crear ImagenProducto si no existe para este producto y url
                if not producto.imagenes.filter(imagen=imagen_url).exists():
                    ImagenProducto.objects.create(
                        producto=producto,
                        imagen=imagen_url,
                        texto_alternativo=prod.get('nombre', '')
                    )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Producto creado: {producto.nombre}"))
            else:
                self.stdout.write(self.style.WARNING(f"Producto ya existe: {producto.nombre}"))
        self.stdout.write(self.style.SUCCESS('Importación finalizada.'))