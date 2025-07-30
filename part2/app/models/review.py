from app.models.basemodel import BaseModel
from app.models.user import User
import uuid

class Review(BaseModel):
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
