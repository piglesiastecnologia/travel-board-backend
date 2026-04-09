from flask import Blueprint, jsonify, request
from app.services.destination_service import (
    create_destination,
    get_all_destinations,
    get_destination_by_id,
    update_destination,
    update_destination_favorite,
    delete_destination,
)

# Creating the blueprint for the destination routes
destination_bp = Blueprint("destinations", __name__)

@destination_bp.route('/health', methods=['GET'])
def index():
    """
    Health check endpoint
    ---
    tags:
      - Health
    responses:
      200:
        description: API is running
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
    """
    return jsonify({"status": "ok"}), 200

@destination_bp.route('/destinations', methods=["POST"])
def create_destination_route():
    """
Create a new destination
---
tags:
  - Destinations
consumes:
  - application/json
parameters:
  - in: body
    name: body
    required: true
    schema:
      type: object
      required:
        - name
        - country
        - city
        - category
        - status
      properties:
        name:
          type: string
          example: Montreal
        country:
          type: string
          example: Canada
        city:
          type: string
          example: Montreal
        category:
          type: string
          example: cultural
        status:
          type: string
          example: planned
        planned_date:
          type: string
          example: 2026-09-20
        estimated_budget:
          type: number
          example: 3000
        notes:
          type: string
          example: Visit museums and old port
        is_favorite:
          type: boolean
          example: true
responses:
  201:
    description: Destination successfully created
  400:
    description: Invalid request
"""
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
    """
List all destinations
---
tags:
  - Destinations
parameters:
  - name: page
    in: query
    type: integer
    required: false
    example: 1
  - name: per_page
    in: query
    type: integer
    required: false
    example: 10
  - name: status
    in: query
    type: string
    required: false
    example: planned
  - name: category
    in: query
    type: string
    required: false
    example: cultural
  - name: search
    in: query
    type: string
    required: false
    example: montreal
responses:
  200:
    description: Paginated and filtered list of destinations
"""
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    status = request.args.get("status", default="", type=str)
    category = request.args.get("category", default="", type=str)
    search = request.args.get("search", default="", type=str)

    results = get_all_destinations(
        page=page,
        per_page=per_page,
        status=status,
        category=category,
        search=search,
    )

    return jsonify(results), 200

@destination_bp.route('/destinations/<int:destination_id>', methods=["GET"])
def get_destination_route(destination_id):
    """
Get destination by ID
---
tags:
  - Destinations
parameters:
  - name: destination_id
    in: path
    type: integer
    required: true
    example: 1
responses:
  200:
    description: Paginated and filtered list of destinations
    schema:
      type: object
      properties:
        items:
          type: array
          items:
            type: object
        total:
          type: integer
          example: 10
        pages:
          type: integer
          example: 2
        current_page:
          type: integer
          example: 1
  404:
    description: Destination not found
"""
    try:
        destination = get_destination_by_id(destination_id)
        return jsonify(destination.to_dict()), 200
    except ValueError as error:
        return jsonify({"error": str(error)}), 404
    
@destination_bp.route('/destinations/<int:destination_id>', methods=["PUT"])
def update_destination_route(destination_id):
    """
Update a destination
---
tags:
  - Destinations
consumes:
  - application/json
parameters:
  - name: destination_id
    in: path
    type: integer
    required: true
    example: 1
  - in: body
    name: body
    required: true
    schema:
      type: object
      properties:
        name:
          type: string
        country:
          type: string
        city:
          type: string
        category:
          type: string
        status:
          type: string
        planned_date:
          type: string
        estimated_budget:
          type: number
        notes:
          type: string
        is_favorite:
          type: boolean
responses:
  200:
    description: Destination updated successfully
  400:
    description: Invalid request
  404:
    description: Destination not found
"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    try:
        data = request.get_json(silent=True)
        
        if not data:
            return jsonify({"error": "Request body must be a valid JSON"}), 400
        
        destination = update_destination(destination_id, data)
        return jsonify(destination.to_dict()), 200
    
    except ValueError as error:
        message = str(error)
        status_code = 404 if "not found" in message.lower() else 400
        return jsonify({"error": message}), status_code
      
@destination_bp.route('/destinations/<int:destination_id>/favorite', methods=["PUT"])
def update_destination_favorite_route(destination_id):
    """
Update destination favorite status
---
tags:
  - Destinations
consumes:
  - application/json
parameters:
  - name: destination_id
    in: path
    type: integer
    required: true
    example: 1
  - in: body
    name: body
    required: true
    schema:
      type: object
      required:
        - is_favorite
      properties:
        is_favorite:
          type: boolean
          example: true
responses:
  200:
    description: Destination favorite status updated successfully
  400:
    description: Invalid request
  404:
    description: Destination not found
"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json(silent=True)

    if not data or "is_favorite" not in data:
        return jsonify({"error": "Field 'is_favorite' is required."}), 400

    try:
        destination = update_destination_favorite(destination_id, data["is_favorite"])
        return jsonify(destination.to_dict()), 200

    except ValueError as error:
        message = str(error)
        status_code = 404 if "not found" in message.lower() else 400
        return jsonify({"error": message}), status_code
    
@destination_bp.route('/destinations/<int:destination_id>', methods=["DELETE"])
def delete_destination_route(destination_id):
    """
Delete a destination
---
tags:
  - Destinations
parameters:
  - name: destination_id
    in: path
    type: integer
    required: true
    example: 1
responses:
  204:
    description: Destination deleted successfully
  404:
    description: Destination not found
"""
    try:
        delete_destination(destination_id)
        return '', 204
    except ValueError as error:
        return jsonify({"error": str(error)}), 404