import unittest
from app import create_app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Sudoku', response.data)

    def test_game(self):
        response = self.client.get('/game')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sudoku Game', response.data)

    def test_invalid_route(self):
        response = self.client.get('/invalid')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()