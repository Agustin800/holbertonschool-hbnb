from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

from app.models.user import User  # asegúrate de que el path sea correcto
from app.models.amenity import Amenity

def create_admin_user():
    admin_id = "36c9050e-ddd3-4c3b-9731-9f487208bbc1"
    admin_email = "admin@hbnb.io"
    admin_password = "admin1234"

    existing_admin = User.query.filter_by(email=admin_email).first()
    if not existing_admin:
        admin = User(
            id=admin_id,
            first_name="Admin",
            last_name="HBnB",
            email=admin_email,
            password=admin_password,
            is_admin=True
        )
        admin.hash_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        print("Usuario admin creado.")
    else:
        print("Usuario admin ya existe.")


    amenity_names = ["WiFi", "Swimming Pool", "Air Conditioning"]
    for name in amenity_names:
        existing_amenity = Amenity.query.filter_by(name=name).first()
        if not existing_amenity:
            amenity = Amenity(name=name)
            db.session.add(amenity)
            db.session.commit()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)

    # Configuraciones
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prueba.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(config_class)
    app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"]

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # API setup
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.ameninties import api as amenity_ns
    from app.api.v1.places import api as place_ns
    from app.api.v1.reviews import api as review_ns
    from app.api.v1.auth import api as auth_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenity_ns, path='/api/v1/amenity')
    api.add_namespace(place_ns, path='/api/v1/places')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path="/api/v1/auth")

    with app.app_context():
        db.create_all()
        create_admin_user()

    jwt.init_app(app)
    return app