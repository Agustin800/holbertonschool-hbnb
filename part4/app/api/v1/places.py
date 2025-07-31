from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    })

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        owner_id = get_jwt_identity()
        owner = facade.get_user(owner_id)
        data = api.payload
        existing_place = facade.get_place(data['title'])

        if not owner:
            return {'error': 'Owner not found'}, 404

        if not owner_id:
            return {'error': 'Unauthorized'}, 401

        if existing_place:
            return {'error': 'Place already exists'}, 400

        amenity_ids = data.get('amenities', [])
        amenities = []
        for amenity_id in amenity_ids:
            amenity = facade.get_amenity(amenity_id)
            if amenity:
                amenities.append(amenity)

        try:
            place = facade.create_place({
                'title': data['title'],
                'description': data.get('description'),
                'price': data['price'],
                'latitude': data['latitude'],
                'longitude': data['longitude'],
                'owner': owner,
                'amenities': amenities,
                'reviews': []
            })

            return {
                'place_id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                },
                'amenities': [a.to_dict() for a in place.amenities]
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        list_place = facade.get_all_places()
        return [{'id': place.id, 'title': place.title, 'price': place.price, 'owner': place.owner.first_name} for place in list_place], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'place not found'}, 404
        return {'title': place.title, 'description': place.description, 'price': place.price, 'latitude': place.latitude, 'longitude': place.longitude, 'owner_id': place.owner.id, 'amenities': place.amenities}, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')    
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        if place.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        place_data = api.payload
        try:
            updated_place = facade.update_place(place_id, place_data)
            return {
                'message': 'Place updated successfully',
                'place': {
                    'id': updated_place.id,
                    'title': updated_place.title,
                    'description': updated_place.description,
                    'price': updated_place.price,
                    'latitude': updated_place.latitude,
                    'longitude': updated_place.longitude,
                    'amenities': [a.to_dict() for a in updated_place.amenities]
                }
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400