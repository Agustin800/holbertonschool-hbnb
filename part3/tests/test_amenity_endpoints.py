import unittest
from app import create_app
import uuid

class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity_valid(self):
        response = self.client.post('/api/v1/amenity/', json={
            "name": "WiFi"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], 'WiFi')

    def test_create_amenity_duplicate(self):
        self.client.post('/api/v1/amenity/', json={"name": "Piscina"})
        response = self.client.post('/api/v1/amenity/', json={"name": "Piscina"})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_amenity_valid(self):
        # Crear
        response = self.client.post('/api/v1/amenity/', json={"name": "TV"})
        amenity_id = response.get_json()['id']

        # Obtener
        response = self.client.get(f'/api/v1/amenity/{amenity_id}')
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], "TV")

    def test_update_amenity_valid(self):
        # Crear
        response = self.client.post('/api/v1/amenity/', json={"name": "Estufa"})
        amenity_id = response.get_json()['id']

        # Actualizar
        response = self.client.put(f'/api/v1/amenity/{amenity_id}', json={"name": "Estufa a leña"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['Amenity']['name'], "Estufa a leña")

if __name__ == '__main__':
    unittest.main()
