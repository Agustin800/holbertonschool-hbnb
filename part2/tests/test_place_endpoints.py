import unittest
from app import create_app
import uuid

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Crear usuario con mail unico usando uuid
        unique_email = f"lena_{uuid.uuid4()}@example.com"
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Lena",
            "last_name": "Jackson",
            "email": unique_email
        })
        self.assertEqual(response.status_code, 201, msg=response.get_data(as_text=True))
        user_data = response.get_json()
        self.assertIn('id', user_data)
        self.owner_id = user_data['id']


    def test_create_place_valid(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Casa en la playa",
            "description": "Hermosa casa frente al mar",
            "price": 150.0,
            "latitude": -34.9,
            "longitude": -56.2,
            "owner_id": self.owner_id,
            "amenities": [],
            "reviews": []
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('place_id', data)

    def test_create_place_invalid(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "price": -10,
            "latitude": 100,
            "longitude": -200,
            "owner_id": "nonexistent",
            "amenities": [],
            "reviews": []
        })
        self.assertIn(response.status_code, (400, 404))

    def test_get_place_valid(self):
        # Crear un nuevo place
        response = self.client.post('/api/v1/places/', json={
            "title": "Casa de campo",
            "description": "Con parrillero",
            "price": 100.0,
            "latitude": -34.0,
            "longitude": -56.0,
            "owner_id": self.owner_id,
            "amenities": [],
            "reviews": []
        })
        place_id = response.get_json()['place_id']

        # Obtener el place
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], "Casa de campo")

    def test_update_place_valid(self):
        # Crear place
        response = self.client.post('/api/v1/places/', json={
            "title": "Casa original",
            "description": "Algo simple",
            "price": 80.0,
            "latitude": -30.0,
            "longitude": -55.0,
            "owner_id": self.owner_id,
            "amenities": [],
            "reviews": []
        })
        place_id = response.get_json()['place_id']

        # Actualizar
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Casa actualizada",
            "description": "Con vista al mar",
            "price": 110.0,
            "latitude": -33.0,
            "longitude": -56.0,
            "amenities": [],
            "reviews": []
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['place']['title'], "Casa actualizada")

if __name__ == '__main__':
    unittest.main()
