from sqlalchemy import or_
from app.extensions import db
from app.models.destination import Destination

def create_destination(destination):
    # put the object destination to be persisted in the session of SQLAlchemy
    db.session.add(destination)
    # confirm commit transaction
    db.session.commit()
    return destination
    
def get_all_destinations(page, per_page, status="", category="", search=""):
    query = Destination.query

    if status:
        query = query.filter(Destination.status == status)

    if category:
        query = query.filter(Destination.category == category)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Destination.name.ilike(search_term),
                Destination.city.ilike(search_term),
            )
        )

    return query.order_by(Destination.id.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
def get_destination_by_id(destination_id):
    # search destination by id
    return db.session.get(Destination, destination_id)

def update_destination(destination):
    # persist changes from the object in memory
    db.session.commit()
    return destination

def delete_destination(destination):
    db.session.delete(destination)
    db.session.commit()