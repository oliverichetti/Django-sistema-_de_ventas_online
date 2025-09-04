from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Carrito, ItemCarrito

def mini_carrito_api(request):
    carrito = Carrito.objects.filter(clave_session=request.session.get('carrito_id')).first()
    if not carrito:
        return JsonResponse({'items': [], 'total': 0})
    items = []
    for item in carrito.items.all():
        items.append({
            'id': item.id,
            'nombre': item.producto.nombre,
            'cantidad': item.cantidad,
            'precio': float(item.precio_unitario),
            'imagen': getattr(item.producto, 'imagen', '') or (item.producto.imagenproducto_set.first().imagen if item.producto.imagenproducto_set.first() else ''),
        })
    return JsonResponse({'items': items, 'total': float(carrito.total)})

@csrf_exempt
def eliminar_item_api(request, item_id):
    if request.method == 'POST':
        item = ItemCarrito.objects.filter(id=item_id).first()
        if item:
            item.delete()
    return JsonResponse({'ok': True})
