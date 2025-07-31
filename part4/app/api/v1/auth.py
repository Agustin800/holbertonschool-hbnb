from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace("auth", description="Authentication")

login_model = api.model("Login", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password")
})

@api.route("/login", methods=["POST", "OPTIONS"])
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        data = api.payload
        user = facade.get_user_by_email(data["email"])
        
        if not user or not user.verify_password(data["password"]):
            return {"error": "Invalid credentials"}, 401

        token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )
        return {"access_token": token}, 200

    def options(self):
        return {}, 200
