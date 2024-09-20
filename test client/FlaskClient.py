import unittest
from server.server import app  # Import the Flask app from your main server.py
from keys.key_manager import generate_rsa_keypair, keys

class FlaskTestClient(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        self.client = app.test_client()
        self.client.testing = True

        # Generate a new key pair before each test
        keys.clear()  # Clear any existing keys
        keys.append(generate_rsa_keypair())  # Append a new key pair

    def test_jwks_endpoint(self):
        # Test GET request to /jwks
        response = self.client.get('/jwks')
        self.assertEqual(response.status_code, 200)  # Check for a 200 OK status
        data = response.get_json()
        print("JWKS Response:", data)  # Print the response for verification
        self.assertIn('keys', data)  # Check if 'keys' is in the response

    def test_auth_endpoint(self):
        # Test POST request to /auth
        response = self.client.post('/auth')
        self.assertEqual(response.status_code, 200)  # Check for a 200 OK status
        data = response.get_json()
        print("Auth Response:", data)  # Print the response for verification
        self.assertIn('token', data)  # Check if 'token' is in the response

    def test_auth_expired_endpoint(self):
        # Test POST request to /auth with expired key
        response = self.client.post('/auth?expired=true')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        print("Expired Auth Response:", data)  # Print the response for verification
        self.assertIn('token', data)

if __name__ == '__main__':
    unittest.main()
