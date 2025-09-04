from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import MovimientoInventario, Despacho
from catalog.models import Producto, Variante, ItemStock
from orders.models import Orden

@login_required
def dashboard(request):
    """Vista para el dashboard del almacén"""
    ordenes_pendientes = Orden.objects.filter(estado='PAID').count()
    productos_bajos = ItemStock.objects.filter(cantidad__lt=10).count()
    movimientos_recientes = MovimientoInventario.objects.all().order_by('-fecha_creacion')[:5]
    
    context = {
        'ordenes_pendientes': ordenes_pendientes,
        'productos_bajos': productos_bajos,
        'movimientos_recientes': movimientos_recientes,
        'title': 'Dashboard de Almacén'
    }
    return render(request, 'warehouse/dashboard.html', context)

@login_required
def inventario(request):
    """Vista para gestionar el inventario"""
    productos = Producto.objects.all()
    
    context = {
        'productos': productos,
        'title': 'Inventario'
    }
    return render(request, 'warehouse/inventario.html', context)

@login_required
def movimientos(request):
    """Vista para ver los movimientos de inventario"""
    movimientos = MovimientoInventario.objects.all().order_by('-fecha_creacion')
    
    context = {
        'movimientos': movimientos,
        'title': 'Movimientos de Inventario'
    }
    return render(request, 'warehouse/movimientos.html', context)

@login_required
def despachos(request):
    """Vista para ver los despachos realizados"""
    despachos = Despacho.objects.all().order_by('-fecha_despacho')
    
    context = {
        'despachos': despachos,
        'title': 'Despachos'
    }
    return render(request, 'warehouse/despachos.html', context)

@login_required
def despachar_orden(request, orden_id):
    """Vista para despachar una orden"""
    orden = get_object_or_404(Orden, id=orden_id)
    
    if orden.estado != 'READY_TO_SHIP':
        messages.warning(request, f'La orden #{orden.id} no está lista para despachar')
        return redirect('warehouse:despachos')
    
    # Crear el despacho
    despacho = Despacho.objects.create(orden=orden)
    
    # Actualizar el estado de la orden
    orden.estado = 'DISPATCHED'
    orden.save()
    
    # Registrar los movimientos de inventario
    for item in orden.items.all():
        MovimientoInventario.objects.create(
            producto=item.producto,
            variante=item.variante,
            tipo='salida',
            cantidad=item.cantidad,
            motivo=f'Despacho de orden #{orden.id}',
            orden_relacionada=orden
        )
    
    messages.success(request, f'Orden #{orden.id} despachada correctamente')
    return redirect('warehouse:despachos')
