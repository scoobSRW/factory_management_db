from flask import Blueprint, jsonify, request
from app.models.models import Customer, db
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.utils.decorator import role_required


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
