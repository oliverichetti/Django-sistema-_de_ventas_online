// Mini-carrito flotante: lógica JS
function toggleMiniCarrito(show) {
    const miniCarrito = document.getElementById('miniCarrito');
    const toggleBtn = document.getElementById('miniCarritoAbrir');
    if (show) {
        miniCarrito.style.display = 'flex';
        toggleBtn.style.display = 'none';
    } else {
        miniCarrito.style.display = 'none';
        toggleBtn.style.display = 'flex';
    }
}

function actualizarMiniCarrito() {
    fetch('/cart/api/mini/')
        .then(res => res.json())
        .then(data => {
            let itemsHtml = '';
            const miniCarrito = document.getElementById('miniCarrito');
            const toggleBtn = document.getElementById('miniCarritoAbrir');
            if (data.items.length === 0) {
                itemsHtml = '<div class="text-center text-muted">El carrito está vacío</div>';
                miniCarrito.style.display = 'none';
                toggleBtn.style.display = 'none';
            } else {
                data.items.forEach(item => {
                    itemsHtml += `<div class="d-flex align-items-center mb-2">
                        <img src="${item.imagen}" alt="${item.nombre}" style="width:40px;height:40px;border-radius:8px;margin-right:10px;object-fit:cover;">
                        <div class="flex-grow-1">
                            <div class="fw-bold">${item.nombre}</div>
                            <div class="small text-muted">x${item.cantidad} - ${item.precio} $</div>
                        </div>
                        <button class="btn btn-sm btn-outline-danger ms-2" onclick="eliminarMiniCarrito(${item.id})"><i class="fas fa-trash"></i></button>
                    </div>`;
                });
                toggleBtn.style.display = 'flex';
            }
            document.getElementById('miniCarritoItems').innerHTML = itemsHtml;
            document.getElementById('miniCarritoTotal').textContent = data.total + ' $';
            document.getElementById('miniCarritoBadge').textContent = data.items.length;
        });
}

function eliminarMiniCarrito(itemId) {
    fetch(`/cart/api/eliminar/${itemId}/`, {method: 'POST', headers: {'X-CSRFToken': getCSRFToken()}})
        .then(() => actualizarMiniCarrito());
}

function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === ('csrftoken=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('miniCarritoAbrir').onclick = () => toggleMiniCarrito(true);
    document.getElementById('miniCarritoCerrar').onclick = () => toggleMiniCarrito(false);
    actualizarMiniCarrito();
});
