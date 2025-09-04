// Animación y notificación toast para agregar al carrito
function showCartToast(productName) {
    let toast = document.createElement('div');
    toast.className = 'cart-toast';
    toast.innerHTML = `<i class='fas fa-check-circle text-success'></i> <strong>${productName}</strong> añadido al carrito!`;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 500);
    }, 2500);

    // Animar el icono del carrito
    let cartIcon = document.querySelector('.fa-shopping-cart');
    if(cartIcon) {
        cartIcon.classList.add('cart-bounce');
        setTimeout(() => cartIcon.classList.remove('cart-bounce'), 800);
    }
}

// Interceptar formularios de agregar al carrito
window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form[action*="agregar_al_carrito"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            let productName = this.closest('.card')?.querySelector('.card-title')?.textContent || 'Producto';
            setTimeout(() => {
                showCartToast(productName);
                // Mostrar mini-carrito flotante
                if (typeof toggleMiniCarrito === 'function') {
                    toggleMiniCarrito(true);
                    actualizarMiniCarrito();
                }
            }, 500);
        });
    });
});
