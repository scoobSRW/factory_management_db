from flask import Blueprint, jsonify, request
from app.models.models import Order, Product, db
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address)

orders_bp = Blueprint('orders', __name__)


# create an order (5 requests per minute)
@orders_bp.route('', methods=['POST'])
@limiter.limit("5 per minute")
def create_order():
    data = request.get_json()
    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    total_price = product.price * data['quantity']
    new_order = Order(customer_id=data['customer_id'], product_id=data['product_id'], quantity=data['quantity'],
                      total_price=total_price)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201


# get all orders (10 requests per minute)
@orders_bp.route('', methods=['GET'])
@limiter.limit("10 per minute")
def get_orders():
    orders = Order.query.all()
    return jsonify([
        {'id': order.id, 'customer_id': order.customer_id, 'product_id': order.product_id, 'quantity': order.quantity,
         'total_price': order.total_price}
        for order in orders
    ]), 200
