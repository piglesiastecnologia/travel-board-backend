from app.extensions import db

class Destination(db.Model):
    __tablename__ = "destinations"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    planned_date = db.Column(db.Date, nullable=True)
    estimated_budget = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    is_favorite = db.Column(db.Boolean, nullable=False, default=False)
    
    created_at = db.Column(db.DateTime, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "city": self.city,
            "category": self.category,
            "planned_date": self.planned_date.isoformat() if self.planned_date else None,
            "estimated_budget": self.estimated_budget,
            "status": self.status,
            "notes": self.notes,
            "is_favorite": self.is_favorite,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }    