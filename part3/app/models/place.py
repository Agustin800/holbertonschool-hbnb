from app import db
from app.models.basemodel import BaseModel
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity
import uuid

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', back_populates='places')

    place_amenity = db.Table(
        'place_amenity',
        db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
        db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
    )


    #Relaciones
    amenities = db.relationship('Amenity', secondary=place_amenity, back_populates='places')
    reviews = db.relationship('Review', back_populates='place', cascade='all, delete-orphan')

    def __init__(self, title, description, price, latitude, longitude, owner, amenities=None, reviews=None):
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError("El titulo es obligatorio y debe tener 100 caracteres máximo")
        self.title = title

        self.description = description

        if price is None or price < 0:
            raise ValueError("El precio es obligatorio y debe ser un valor valido")
        self.price = price

        if latitude < -90 or latitude > 90:
            raise ValueError("latitud debe ser mayor a -90 y menor a 90")
        self.latitude = latitude

        if longitude < -180 or longitude > 180:
            raise ValueError("longitud debe ser mayor a -180 y menor a 180")
        self.longitude = longitude

        if not isinstance(owner, User):
            raise ValueError("Debe asignarse un propietario")
        self.owner = owner

        self.reviews = reviews
        self.amenities = amenities

    def add_review(self, review):
        if not isinstance(review, Review):
            raise ValueError("Solo se pueden agregar objetos de tipo Review")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise ValueError("Solo se pueden agregar objetos de tipo Amenity")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
