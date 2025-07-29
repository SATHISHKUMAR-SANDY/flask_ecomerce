from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from app.models import Cart, Product
from app import db

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/')
@login_required
def view_cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))

    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    db.session.commit()
    flash(f'Added {quantity} of {product.name} to your cart.', 'success')
    return redirect(url_for('product.product_list'))

@cart_bp.route('/remove/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    cart_item = Cart.query.get_or_404(cart_item_id)
    if cart_item.user_id != current_user.id:
        flash("You can't remove items from someone else's cart!", 'danger')
        return redirect(url_for('cart.view_cart'))
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/update/<int:cart_item_id>', methods=['POST'])
@login_required
def update_cart_item(cart_item_id):
    cart_item = Cart.query.get_or_404(cart_item_id)
    if cart_item.user_id != current_user.id:
        return jsonify({'error': "Unauthorized"}), 403

    new_quantity = int(request.form.get('quantity', 1))
    if new_quantity < 1:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = new_quantity
    db.session.commit()
    return jsonify({'success': True, 'new_quantity': new_quantity})
