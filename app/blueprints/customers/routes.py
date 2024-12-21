from flask import Blueprint, jsonify, request
from app.models.models import Customer, db
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address)

customers_bp = Blueprint('customers', __name__)

# create customer (5 requests per minute)
@customers_bp.route('', methods=['POST'])
@limiter.limit("5 per minute")
def create_customer():
    data = request.get_json()
    new_customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully'}), 201

# get all customers (10 requests per minute)
@customers_bp.route('', methods=['GET'])
@limiter.limit("10 per minute")
def get_customers():
    customers = Customer.query.all()
    return jsonify([{'id': cust.id, 'name': cust.name, 'email': cust.email, 'phone': cust.phone} for cust in customers]), 200
