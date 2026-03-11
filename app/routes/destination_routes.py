from flask import Blueprint, jsonify, request
from app.services.destination_service import (
    create_destination,
    get_all_destinations
)

# Creating the blueprint for the destination routes
destination_bp = Blueprint("destinations", __name__)

@destination_bp.route('/health', methods=['GET'])
def health_index():
    return jsonify({"status": "ok"}), 200

@destination_bp.route('/destinations', methods=["POST"])
def create_destination_route():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Request body must be a valid JSON."}), 400
        
        destination = create_destination(data)
        return jsonify(destination.to_dict()), 201
        
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

@destination_bp.route('/destinations', methods=["GET"])
def get_all_destinations_route():
    destinations = get_all_destinations()
    return jsonify([destination.to_dict() for destination in destinations]), 200