import os
import unittest
import json
from app import app

class DuffelFlightsIntegrationTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.headers = {
            "Content-Type": "application/json",
            "Duffel-Version": "v2",
            "Authorization": f"Bearer {os.getenv('DUFFEL_API_KEY', 'your_default_api_key_here')}"
        }

    def test_duffel_flights_list_offers_success(self):
        # Example payload, replace with actual test data
        payload = {
            "data": {
                "slices": [
                    {
                        "origin": "LHR",
                        "destination": "JFK",
                        "departure_date": "2023-12-01"
                    }
                ],
                "passengers": [
                    {
                        "type": "adult"
                    }
                ]
            }
        }
        response = self.app.post('/duffel-flights-list-offers', headers=self.headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)

    def test_duffel_flights_list_offers_invalid_request(self):
        # Example of an invalid payload
        payload = {
            "data": {
                "slices": [],
                "passengers": []
            }
        }
        response = self.app.post('/duffel-flights-list-offers', headers=self.headers, data=json.dumps(payload))
        self.assertNotEqual(response.status_code, 200)
        self.assertIn('errors', response.json)

if __name__ == '__main__':
    unittest.main()