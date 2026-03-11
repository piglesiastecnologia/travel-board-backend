from app.extensions import db
from app.models.destination import Destination

def create_destination(destination):
    # put the object destination to be persisted in the session of SQLAlchemy
    db.session.add(destination)
    # confirm commit transaction
    db.session.commit()
    return destination
    
def get_all_destinations():
    # search all destinations persisted in the DB
    return Destination.query.order_by(Destination.id.desc()).all()
    
