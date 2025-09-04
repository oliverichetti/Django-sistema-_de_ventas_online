from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Orden, ItemOrden
from cart.models import Carrito
from cart.views import _get_or_create_carrito
from promotions.models import Cupon

def checkout(request):
    """Vista para el proceso de checkout"""
    carrito = _get_or_create_carrito(request)
    items = carrito.items.all()
    
    if not items:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('cart:carrito_detalle')
    
    context = {
        'carrito': carrito,
        'items': items,
        'title': 'Checkout'
    }
    return render(request, 'orders/checkout.html', context)

def confirmar_orden(request):
    """Vista para confirmar y crear una orden"""
    if request.method == 'POST':
        carrito = _get_or_create_carrito(request)
        items = carrito.items.all()
        
        if not items:
            messages.warning(request, 'Tu carrito está vacío')
            return redirect('cart:carrito_detalle')
        
        # Crear la orden
        orden = Orden.objects.create(
            clave_session=carrito.clave_session,
            nombre_envio=request.POST.get('nombre_envio'),
            direccion_envio=request.POST.get('direccion_envio'),
            telefono=request.POST.get('telefono'),
            total=carrito.total,
            cupon=carrito.cupon
        )
        
        # Crear los items de la orden
        for item in items:
            ItemOrden.objects.create(
                orden=orden,
                producto=item.producto,
                variante=item.variante,
                cantidad=item.cantidad,
                precio_unitario=item.precio,
                total_linea=item.subtotal
            )
        
        # Limpiar el carrito
        items.delete()
        carrito.cupon = None
        carrito.save()
        # Actualizar el contador de productos en la sesión
        request.session['carrito_items'] = 0
        
        messages.success(request, f'Orden #{orden.id} creada exitosamente')
        return redirect('orders:orden_detalle', orden_id=orden.id)
    
    return redirect('orders:checkout')

def orden_detalle(request, orden_id):
    """Vista para mostrar los detalles de una orden"""
    orden = get_object_or_404(Orden, id=orden_id, clave_session=request.session.get('carrito_id', ''))
    items = orden.items.all()
    
    context = {
        'orden': orden,
        'items': items,
        'title': f'Orden #{orden.id}'
    }
    return render(request, 'orders/orden_detalle.html', context)

@login_required
def historial_ordenes(request):
    """Vista para mostrar el historial de órdenes del usuario"""
    # En una implementación real, filtrarías por usuario
    ordenes = Orden.objects.filter(clave_session=request.session.get('carrito_id', '')).order_by('-fecha_creacion')
    
    context = {
        'ordenes': ordenes,
        'title': 'Historial de Órdenes'
    }
    return render(request, 'orders/historial_ordenes.html', context)
