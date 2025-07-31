from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload

        if 'password' not in user_data or not user_data['password']:
            return {'error': 'Password is required'}, 400

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'message': 'User registered successfully'
            }, 201
        except ValueError as e:
            return {'error': 'Invalid input data', 'message': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        users = facade.get_all_users()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        user_data = api.payload
        try:
            updated_user = facade.update_user(user_id, user_data)
            return {
                'message': 'User updated successfully',
                'user': {
                    'id': updated_user.id,
                    'first_name': updated_user.first_name,
                    'last_name': updated_user.last_name,
                    'email': updated_user.email
                }
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400