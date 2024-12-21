from flask import Blueprint, jsonify, request
from app.models.models import Product, db
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address)

products_bp = Blueprint('products', __name__)

# create a product (5 requests per minute)
@products_bp.route('', methods=['POST'])
@limiter.limit("5 per minute")
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

# get all products (10 requests per minute)
@products_bp.route('', methods=['GET'])
@limiter.limit("10 per minute")
def get_products():
    products = Product.query.all()
    return jsonify([{'id': prod.id, 'name': prod.name, 'price': prod.price} for prod in products]), 200
