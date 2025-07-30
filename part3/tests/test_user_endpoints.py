import unittest
from app import create_app
import uuid


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
#POST
    def test_create_user_valid(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)

    def test_create_user_invalid(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

#GET
    def test_get_user_valid(self):
        # Crear usuario primero
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@example.com"
        })
        user_id = response.get_json()['id']

        # Obtener usuario
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'Alice')

    def test_get_user_not_found(self):
        response = self.client.get('/api/v1/users/12345')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('error', data)

#PUT
    def test_update_user_valid(self):
        # Crear usuario
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Brown",
            "email": "bob.brown@example.com"
        })
        user_id = response.get_json()['id']

        # Actualizar
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Bobby",
            "last_name": "Brown",
            "email": "bobby.brown@example.com"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['user']['first_name'], 'Bobby')

    def test_update_user_not_found(self):
        response = self.client.put('/api/v1/users/999', json={
            "first_name": "Ghost",
            "last_name": "User",
            "email": "ghost@example.com"
        })
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('error', data)

    def test_update_user_invalid_data(self):
    # Crear usuario
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Carlos",
            "last_name": "Lopez",
            "email": "carlos.lopez@example.com"
        })
        user_id = response.get_json()['id']

        # Intentar actualizar con datos inválidos
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "",
            "last_name": "Lopez",
            "email": "not-an-email"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()

