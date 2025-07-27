from flask import jsonify, Blueprint
from models import db, Publisher

# Create a Blueprint for publisher routes
publishers_bp = Blueprint('publishers', __name__)

@publishers_bp.route('/api/publishers', methods=['GET'])
def get_publishers():
    """Get all publishers with their id and name."""
    publishers = db.session.query(Publisher).all()
    publishers_list = [{"id": p.id, "name": p.name} for p in publishers]
    return jsonify(publishers_list)
