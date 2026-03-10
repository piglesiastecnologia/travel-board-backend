from flask import Blueprint, jsonify
from markupsafe import escape

# Creating the blueprint for the destination routes
destination_bp = Blueprint("destination", __name__)

@destination_bp.route('/health', methods=['GET'])
def index():
    return jsonify({"status": "ok"})
