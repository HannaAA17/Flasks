from sqlalchemy.orm.query import Query

from flask import Blueprint, render_template, redirect, url_for, flash, session, request

from ..models import Product, Order, OrderItem
from ..forms import AddProductForm, AddToCartForm, CheckoutForm
from ..forms import STATES, COUNTRIES, PAYMENTS


bp = Blueprint('admin', __name__, url_prefix='/admin')


STATES_DICT = {k:v for k, v in STATES}
COUNTRIES_DICT = {k:v for k, v in COUNTRIES}
PAYMENTS_DICT = {k:v for k, v in PAYMENTS}


@bp.route('/')
def admin():
    products: Query[Product] = Product.query.all()
    products_in_stock_count: int = Product.query.filter(Product.stock > 0).count()
    pending_orders: int = Order.query.filter(Order.status == 'PENDING').all()
    completed_orders_count = Order.query.count() - len(pending_orders)
    return render_template('admin/index.html', pending_orders=pending_orders, completed_orders_count=completed_orders_count, products=products, products_in_stock_count=products_in_stock_count, admin=True)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = AddProductForm()

    if form.validate_on_submit():
        new_product = Product()
        form.save_image()
        form.populate_obj(new_product)
        new_product.save()
        return redirect(url_for('.admin'))

    return render_template('admin/add-product.html', form=form, admin=True)


@bp.route('/order/<string:reference>')
def order(reference):
    order: Order = Order.query.filter_by(reference=reference).first_or_404(description='Order not found')
    
    ctx = {}
    ctx['reference'] = order.reference
    ctx['first_name'] = order.first_name
    ctx['last_name'] = order.last_name
    ctx['phone_number'] = order.phone_number
    ctx['email'] = order.email
    ctx['address'] = '{}, {}'.format(order.address, order.city)
    ctx['state'] = STATES_DICT[order.state]
    ctx['country'] = COUNTRIES_DICT[order.country]

    ctx['payment_type'] = PAYMENTS_DICT[order.payment_type]
    ctx['status'] = order.status
    ctx['products_count'] = order.order_items.count()
    ctx['total'] = order.total()

    ctx['order_items'] = []
    for ndx, item in enumerate(order.order_items, start=1):
        item_ctx = {}
        item_ctx['ndx'] = ndx
        item_ctx['name'] = item.product.name
        item_ctx['price'] = item.product.price
        item_ctx['qty'] = item.quantity
        item_ctx['tot_price'] = item.price
        ctx['order_items'].append(item_ctx)

    return render_template('admin/view-order.html', ctx=ctx, admin=True)

