from datetime import datetime
from app.models.destination import Destination
from app.repositories.destination_repository import (
    create_destination as create_destination_repository,
    get_all_destinations as get_all_destinations_repository,
    get_destination_by_id as get_destination_by_id_repository,
)

ALLOWED_STATUSES = {"idea", "planned", "booked", "visited"}
ALLOWED_CATEGORIES = {"beach", "city", "mountain", "cultural", "adventure"}

def validate_required_fields(data):
    required_fields = ["name", "country", "city", "category", "status"]
    
    for field in required_fields:
        if field not in data or data[field] in (None, ""):
            raise ValueError(f"Field '{field}' is required.")
    
def validate_status(status):
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"Invalid status. Allowed values are: {', '.join(sorted(ALLOWED_STATUSES))}.")

def validate_category(category):
    if category not in ALLOWED_CATEGORIES:
        raise ValueError(f"Invalid category. Allowed values are: {', '.join(sorted(ALLOWED_CATEGORIES))}.")

def parse_planned_date(planned_date):
    if not planned_date:
        return None
    
    try:
        return datetime.strptime(planned_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("planned_date must be in YYYY-MM-DD format.")

def parse_estimated_budget(value):
    if value in (None, ""):
        return None
    
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError("estimated_budget must be a valid number.")
    
def create_destination(data):
    category=data["category"].strip().lower()
    status=data["status"].strip().lower()

    validate_required_fields(data)
    validate_status(status)
    validate_category(category)
    
    estimated_budget = parse_estimated_budget(data.get("estimated_budget"))
    planned_date = parse_planned_date(data.get("planned_date"))
    
    destination = Destination(
        name=data["name"],
        country=data["country"],
        city=data["city"],
        category=category,
        planned_date=planned_date,
        estimated_budget=estimated_budget,
        status=status,
        notes=data.get("notes"),
        is_favorite=data.get("is_favorite", False),
        created_at=datetime.now(),
    )
    
    return create_destination_repository(destination)

def get_all_destinations():
    return get_all_destinations_repository()

def get_destination_by_id(destination_id):
    destination = get_destination_by_id_repository(destination_id=destination_id)
    if not destination: 
        raise ValueError(f"Destination with id {destination_id} not found.")
    
    return destination