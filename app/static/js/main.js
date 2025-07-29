document.addEventListener('DOMContentLoaded', () => {
  // Handle quantity updates
  document.querySelectorAll('.cart-quantity-input').forEach(input => {
    input.addEventListener('change', async (e) => {
      const cartItemId = e.target.dataset.cartItemId;
      const newQuantity = e.target.value;

      if (newQuantity < 1) {
        alert('Quantity must be at least 1');
        e.target.value = 1;
        return;
      }

      try {
        const response = await fetch(`/cart/update/${cartItemId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: `quantity=${newQuantity}`
        });
        const data = await response.json();
        if (data.success) {
          // Optionally update UI or show message
          location.reload(); // simplest way to reflect changes
        } else {
          alert('Error updating cart');
        }
      } catch (err) {
        alert('Network error');
      }
    });
  });

  // Handle remove buttons
  document.querySelectorAll('.remove-cart-item-btn').forEach(button => {
    button.addEventListener('click', async (e) => {
      e.preventDefault();
      const form = e.target.closest('form');
      if (confirm('Remove this item from cart?')) {
        form.submit(); // submit the POST form to remove item
      }
    });
  });
});
