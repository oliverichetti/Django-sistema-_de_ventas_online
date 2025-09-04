from django.shortcuts import render, get_object_or_404
from .models import Categoria, Producto

def home(request):
    """Vista para la página principal que muestra categorías y productos destacados"""
    categorias = Categoria.objects.all()
    productos_destacados = Producto.objects.filter(destacado=True)[:8]
    
    context = {
        'categorias': categorias,
        'productos_destacados': productos_destacados,
        'title': 'Inicio - Tienda Online'
    }
    return render(request, 'catalog/home.html', context)

def categoria_detalle(request, categoria_id):
    """Vista para mostrar los productos de una categoría específica"""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)

    context = {
        'categoria': categoria,
        'productos': productos,
        'title': f'Categoría: {categoria.nombre}'
    }
    return render(request, 'catalog/categoria_detalle.html', context)

def producto_detalle(request, producto_id):
    """Vista para mostrar los detalles de un producto específico"""
    producto = get_object_or_404(Producto, id=producto_id)
    variantes = producto.variantes.all()
    imagenes = producto.imagenes.all()
    
    context = {
        'producto': producto,
        'variantes': variantes,
        'imagenes': imagenes,
        'title': producto.nombre
    }
    return render(request, 'catalog/producto_detalle.html', context)

# Vista para productos destacados
def productos_destacados(request):
    productos = Producto.objects.filter(destacado=True)
    context = {
        'productos': productos,
        'title': 'Productos Destacados'
    }
    return render(request, 'catalog/productos_destacados.html', context)
