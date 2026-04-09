from datetime import datetime
from app.models.destination import Destination
from app.repositories.destination_repository import (
    create_destination as create_destination_repository,
    get_all_destinations as get_all_destinations_repository,
    get_destination_by_id as get_destination_by_id_repository,
    update_destination as update_destination_repository,
    delete_destination as delete_destination_repository,
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

def get_all_destinations(page, per_page, status="", category="", search=""):
    normalized_status = status.strip().lower() if status else ""
    normalized_category = category.strip().lower() if category else ""
    normalized_search = search.strip() if search else ""

    if normalized_status:
        validate_status(normalized_status)

    if normalized_category:
        validate_category(normalized_category)

    pagination = get_all_destinations_repository(
        page=page,
        per_page=per_page,
        status=normalized_status,
        category=normalized_category,
        search=normalized_search,
    )

    return {
        "items": [destination.to_dict() for destination in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }

def get_destination_by_id(destination_id):
    destination = get_destination_by_id_repository(destination_id=destination_id)
    if not destination: 
        raise ValueError(f"Destination with id {destination_id} not found.")
    
    return destination

def update_destination(destination_id, data):
    destination = get_destination_by_id_repository(destination_id)
    
    if not destination:
        raise ValueError(f"Destination with id {destination_id} not found.")
    
    if "name" in data and data["name"] not in (None, ""):
        destination.name = data["name"]
        
    if "country" in data and data["country"] not in (None, ""):
        destination.country = data["country"]
        
    if "city" in data and data["city"] not in (None, ""):
        destination.city = data["city"]
        
    if "category" in data and data["category"] not in (None, ""):
        category = data["category"].strip().lower()
        validate_category(category)
        destination.category = category
        
    if "status" in data and data["status"] not in (None, ""):
        status = data["status"].strip().lower()
        validate_status(status)
        destination.status = status
        
    if "planned_date" in data:
        destination.planned_date = parse_planned_date(data.get("planned_date"))
        
    if "estimated_budget" in data:
        destination.estimated_budget = parse_estimated_budget(data.get("estimated_budget"))
        
    if "notes" in data:
        destination.notes = data.get("notes")
        
    if "is_favorite" in data:
        destination.is_favorite = bool(data.get("is_favorite"))
        
    return update_destination_repository(destination)

def update_destination_favorite(destination_id, is_favorite):
    destination = get_destination_by_id_repository(destination_id)

    if not destination:
        raise ValueError(f"Destination with id {destination_id} not found.")

    destination.is_favorite = bool(is_favorite)

    return update_destination_repository(destination)

def delete_destination(destination_id):
    # here we'll apply reusable function to get the destination id
    destination = get_destination_by_id(destination_id)
    delete_destination_repository(destination)
    
        