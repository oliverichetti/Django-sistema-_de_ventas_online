from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Carrito, ItemCarrito
from catalog.models import Producto, Variante
import uuid

def _get_or_create_carrito(request):
    """Función auxiliar para obtener o crear un carrito para el usuario"""
    if 'carrito_id' not in request.session:
        # Crear un nuevo carrito con un ID de sesión único
        request.session['carrito_id'] = str(uuid.uuid4())
    
    carrito, created = Carrito.objects.get_or_create(
        clave_session=request.session['carrito_id']
    )
    return carrito

def carrito_detalle(request):
    """Vista para mostrar el contenido del carrito"""
    carrito = _get_or_create_carrito(request)
    items = carrito.items.all()
    
    context = {
        'carrito': carrito,
        'items': items,
        'title': 'Tu Carrito'
    }
    return render(request, 'cart/carrito_detalle.html', context)

def agregar_al_carrito(request, producto_id):
    """Vista para agregar un producto al carrito"""
    if request.method == 'POST':
        carrito = _get_or_create_carrito(request)
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = int(request.POST.get('cantidad', 1))
        variante_id = request.POST.get('variante_id')
        
        variante = None
        if variante_id:
            variante = get_object_or_404(Variante, id=variante_id)
        
        # Verificar si el producto ya está en el carrito
        item_existente = ItemCarrito.objects.filter(
            carrito=carrito,
            producto=producto,
            variante=variante
        ).first()
        
        if item_existente:
            # Actualizar cantidad si ya existe
            item_existente.cantidad += cantidad
            item_existente.save()
            messages.success(request, 'Cantidad actualizada en el carrito')
        else:
            # Crear nuevo item en el carrito
            ItemCarrito.objects.create(
                carrito=carrito,
                producto=producto,
                variante=variante,
                cantidad=cantidad,
                precio_unitario=producto.precio,
                precio=producto.precio * cantidad
            )
            messages.success(request, 'Producto agregado al carrito')
    
    # Actualizar el contador de productos en la sesión
    request.session['carrito_items'] = ItemCarrito.objects.filter(carrito=carrito).count()
    # Si la petición viene de compra rápida, redirigir a la página anterior
    referer = request.META.get('HTTP_REFERER')
    if referer and 'producto_detalle' not in referer:
        return redirect(referer)
    return redirect('catalog:producto_detalle', producto_id=producto_id)

def actualizar_carrito(request, item_id):
    """Vista para actualizar la cantidad de un item en el carrito"""
    if request.method == 'POST':
        item = get_object_or_404(ItemCarrito, id=item_id)
        cantidad = int(request.POST.get('cantidad', 1))
        
        if cantidad > 0:
            item.cantidad = cantidad
            item.save()
            messages.success(request, 'Carrito actualizado')
        else:
            item.delete()
            messages.success(request, 'Producto eliminado del carrito')
    
    # Actualizar el contador de productos en la sesión
    carrito = item.carrito
    request.session['carrito_items'] = ItemCarrito.objects.filter(carrito=carrito).count()
    return redirect('cart:carrito_detalle')

def eliminar_del_carrito(request, item_id):
    """Vista para eliminar un item del carrito"""
    if request.method in ['GET', 'POST']:
        item = get_object_or_404(ItemCarrito, id=item_id)
        carrito = item.carrito
        item.delete()
        # Actualizar el contador de productos en la sesión
        request.session['carrito_items'] = ItemCarrito.objects.filter(carrito=carrito).count()
        messages.success(request, 'Producto eliminado del carrito')
        return redirect('cart:carrito_detalle')
    else:
        return redirect('cart:carrito_detalle')
