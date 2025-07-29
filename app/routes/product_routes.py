from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.forms import ProductForm
from app.models import Product
from app import db

product_bp = Blueprint('product', __name__)

@product_bp.route('/')
def product_list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)

@product_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@product_bp.route('/product/add', methods=['GET', 'POST'])
@login_required
def product_add():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            quantity=form.quantity.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('product.product_list'))
    return render_template('product_form.html', form=form)

@product_bp.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def product_edit(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('product.product_detail', product_id=product.id))
    return render_template('product_form.html', form=form)

@product_bp.route('/product/<int:product_id>/delete', methods=['POST'])
@login_required
def product_delete(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted!', 'info')
    return redirect(url_for('product.product_list'))
