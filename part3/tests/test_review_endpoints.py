import unittest
from app import create_app
import uuid

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Crear usuario con email único usando uuid y place
        unique_email = f"eva_{uuid.uuid4()}@example.com"
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Eva",
            "last_name": "Mendez",
            "email": unique_email
        })
        self.assertEqual(user_resp.status_code, 201, msg=user_resp.get_data(as_text=True))
        user = user_resp.get_json()
        self.user_id = user['id']

        place_resp = self.client.post('/api/v1/places/', json={
            "title": "Loft moderno",
            "description": "Céntrico",
            "price": 90.0,
            "latitude": -34.9,
            "longitude": -56.2,
            "owner_id": self.user_id,
            "amenities": [],
            "reviews": []
        })
        self.assertEqual(place_resp.status_code, 201, msg=place_resp.get_data(as_text=True))
        place = place_resp.get_json()
        self.place_id = place['place_id']

    def test_create_review_valid(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Muy cómodo",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 10,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_get_review_valid(self):
        # Crear review
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Excelente estadía",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = response.get_json()['id']

        # Obtener
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['rating'], 5)

    def test_update_review_valid(self):
        # Crear
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Requiere mejoras",
            "rating": 2,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = response.get_json()['id']

        # Actualizar
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Mucho mejor esta vez",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['review']['rating'], 4)

    def test_delete_review_valid(self):
        # Crear
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Para borrar",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = response.get_json()['id']

        # Borrar
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)

if __name__ == '__main__':
    unittest.main()
