from django.shortcuts import redirect
from django.contrib import messages
from .models import Cupon
from cart.views import _get_or_create_carrito

def aplicar_cupon(request):
    """Vista para aplicar un cupón al carrito"""
    if request.method == 'POST':
        codigo = request.POST.get('codigo_cupon')
        
        try:
            cupon = Cupon.objects.get(codigo=codigo, activo=True)
            carrito = _get_or_create_carrito(request)
            
            # Verificar si el carrito cumple con el mínimo requerido
            if carrito.total < cupon.total_minimo:
                messages.warning(request, f'El total del carrito debe ser al menos {cupon.total_minimo} para usar este cupón')
                return redirect('cart:carrito_detalle')
            
            carrito.cupon = cupon
            carrito.save()
            messages.success(request, f'Cupón {codigo} aplicado correctamente')
        except Cupon.DoesNotExist:
            messages.error(request, f'El cupón {codigo} no existe o no está activo')
    
    return redirect('cart:carrito_detalle')

def eliminar_cupon(request):
    """Vista para eliminar un cupón del carrito"""
    carrito = _get_or_create_carrito(request)
    if carrito.cupon:
        codigo = carrito.cupon.codigo
        carrito.cupon = None
        carrito.save()
        messages.success(request, f'Cupón {codigo} eliminado correctamente')
    
    return redirect('cart:carrito_detalle')
