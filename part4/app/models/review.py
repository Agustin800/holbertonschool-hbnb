from app import db
from app.models.basemodel import BaseModel
from app.models.user import User
import uuid
from sqlalchemy import UniqueConstraint

class Review(BaseModel):
    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'place_id', name='uq_user_place_review'),
    )

    # Relaciones
    place = db.relationship('Place', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

    def __init__(self, text, rating, place, user):
        from app.models.place import Place
        super().__init__()

        if not text or len(text) > 100:
            raise ValueError("El texto es obligatorio y debe tener máximo 100 caracteres")
        self.text = text

        if rating < 1 or rating > 5:
            raise ValueError("La calificacion debe ser un valor valido")
        self.rating = rating

        if not isinstance(place, Place):
            raise ValueError("Debe ser adjuntado a una propiedad")
        self.place = place

        if not isinstance(user, User):
            raise ValueError("Debe ser asociado un usuario")
        self.user = user
