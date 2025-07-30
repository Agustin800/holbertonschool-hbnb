from app import db, bcrypt
from app.models.basemodel import BaseModel
import uuid
from flask_bcrypt import Bcrypt

class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relaciones
    places = db.relationship('Place', back_populates='owner', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')
    
    def __init__(self, first_name, last_name, email, password, is_admin=False, id=None):
        super().__init__()
        if id:
            self.id = id

        if not first_name or len(first_name) > 50:
            raise ValueError("El nombre es obligatorio y debe tener 50 caracteres máximo")
        self.first_name = first_name

        if not last_name or len(last_name) > 50:
            raise ValueError("El apellido es obligatorio y debe tener 50 caracteres máximo")
        self.last_name = last_name

        if not email or not self.validador_email(email):
            raise ValueError("El email es obligatorio y debe tener un formato valido")
        self.email = email

        self.is_admin = is_admin

    def validador_email(self, email):
        return email.count("@") == 1 and "." in email
    
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password_hash, password)