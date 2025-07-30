from app.models.basemodel import BaseModel
import uuid

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

        if not name or len(name) > 50:
            raise ValueError("El nombre es obligatorio y debe tener 50 caracteres máximo")
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }