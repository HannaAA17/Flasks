from sqlalchemy.orm.query import Query

from flask import Blueprint, render_template, redirect, url_for, flash, session, request

from ..models import Product, Order, OrderItem
from ..forms import AddProductForm, AddToCartForm, CheckoutForm


bp = Blueprint('main', __name__)


def __get_summary():
    cart = session.get('cart', [])
    products = []
    summary = {}
    for ndx, item in enumerate(cart):
        prod:Product = Product.query.get(item['id'])
        if prod:
            # products.append({'prod': prod, 'quantity': item['quantity']})
            products.append({
                'ndx': ndx,
                'id': prod.id,
                'image': prod.image,
                'name': prod.name,
                'price': prod.price/100,
                'quantity': item['quantity'],
                'stock': prod.stock,
                'total': prod.price*item['quantity']/100,
                '__product': prod,
            })
    
    summary['number_of_items'] =  len(products)
    summary['total'] = sum(x['total'] for x in products)
    summary['shipping'] = 10
    summary['tax'] =  0
    summary['grand_total'] = summary['total']+summary['shipping']+summary['tax']
    return products, summary


@bp.route('/')
def index():
    products: Query[Product] = Product.query.all()
    return render_template('main/index.html', products=products)


@bp.route('/product/<int:id>')
def product(id):
    prod = Product.query.get_or_404(id, description='product not found')
    form = AddToCartForm(prod)
    return render_template('main/view-product.html', form=form)


@bp.route('/cart')
def cart():
    products, summary = __get_summary()
    return render_template('main/cart.html', products=products, summary=summary)


@bp.route('/checkout', methods=['get', 'post'])
def checkout():
    form:CheckoutForm = CheckoutForm()
    products, summary = __get_summary()
    
    if len(products)==0:
        return '<h1>Can not order with empty cart</h1><a href="./"> return </a>' 

    if form.validate_on_submit():
        order = Order()
        form.populate_obj(order)
        order.random_reference()
        order.status = 'PENDING'
        for prod in products:
            order.order_items.append(OrderItem(
                product=prod['__product'],
                order=order,
                quantity= prod['quantity'],
            ))
        order.save()
        session['cart'] = []
        session.modified = True

        # update the stock
        for order_item in order.order_items:
            order_item.product.stock -= order_item.quantity
            order_item.product.save()

        return '<h1>Purchase Completed Successfully</h1><a href="./"> return </a>'
    
    return render_template('main/checkout.html', form=form, summary=summary)


@bp.route('/quick_add_to_cart/<int:id>', methods=['GET'])
def quick_add_to_cart(id):
    prod:Product = Product.query.get_or_404(id, description='product not found')
    cart:list = session.setdefault('cart', [])
    if prod.stock>=1:
        cart.append({'id': prod.id, 'quantity': 1})
        session.modified = True
        return redirect(url_for('.cart'))
    else:
        flash('product is out of stock', 'danger')
        return redirect(url_for('.product', id=id))


@bp.route('/add_to_cart/<int:id>', methods=['POST'])
def add_to_cart(id):
    prod:Product = Product.query.get_or_404(id, description='product not found')
    cart:list = session.setdefault('cart', [])
    form = AddToCartForm(prod)

    if form.validate():
        cart: list = session.setdefault('cart', [])
        cart.append({'id': prod.id, 'quantity': form.quantity.data})
        session.modified = True
        return redirect(url_for('.cart'))

    # handle the form errors
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'danger')

    return redirect(url_for('.product', id=id))


@bp.route('/remove_from_cart/<int:ndx>', methods=['GET'])
def remove_from_cart(ndx):
    cart:list = session.setdefault('cart', [])
    try:
        del cart[ndx]
        session.modified = True
    except IndexError:
        pass
    return redirect(url_for('.cart'))

