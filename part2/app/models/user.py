from app.models.basemodel import BaseModel
import uuid

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

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
