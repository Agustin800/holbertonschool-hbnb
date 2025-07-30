from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.review import Review

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        user = facade.get_user(user_id)
        data = api.payload

        if not current_user:
            return {'error': 'User not found'}, 404

        data.pop('user_id', None)
        data['user'] = user

        place_id = data.get('place_id')
        if not place_id: 
            return {'error': 'Place ID is required'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        data.pop('place_id', None) 
        data['place'] = place

        existing_review = Review.query.filter_by(user_id=user.id, place_id=place.id).first()
        if existing_review:
            return {'error': 'User has already reviewed this place.'}, 400
        try:
            new_review = facade.create_review(data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user':{
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'place':{
                    'id': place.id,
                    'title': place.title
                }
                }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        list_review = facade.get_all_reviews()
        return [{'id': review.id, 'text': review.text, 'rating': review.rating, 'user': review.user.first_name, 'place': review.place.title} for review in list_review], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'text': review.text,
            'rating': review.rating,
            'user': review.user.first_name,
            'place': review.place.title
            }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'review not found'}, 404

        if review.user_id != current_user["id"]:
            return {'error': 'Unauthorized action'}, 403

        review_data = api.payload
        try:
            updated_review = facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully', 'review': {
                'id': updated_review.id,
                'rating': updated_review.rating,
                'user': updated_review.user.first_name,
                'place': updated_review.place.title
            }}, 200

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        current_user_id = current_user["id"]
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404
        user_id = review.user_id

        if current_user_id != user_id:
            return {"error": "Unauthorized"}, 403

        else:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {'error': 'Reviews not found'}, 404
        return [{
            'text': review.text,
            'rating': review.rating,
            'user': review.user.first_name,
            'place': review.place.title
            }for review in reviews], 200