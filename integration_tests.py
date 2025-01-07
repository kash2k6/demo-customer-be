import unittest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TestFlightAPIIntegration(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://localhost:5000"
        self.duffel_access_token = os.getenv('DUFFEL_ACCESS_TOKEN')
        self.headers = {
            "Accept-Encoding": "gzip",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Duffel-Version": "v1",
            "Authorization": f"Bearer {self.duffel_access_token}"
        }

    def test_fetch_flight_data(self):
        params = {
            "acid": "AA123",
            "outdate": "2023-10-01",
            "indate": "2023-10-10"
        }
        response = requests.get(f"{self.base_url}/fetch-flight-data", params=params)
        self.assertEqual(response.status_code, 200)
        self.assertIn("flights", response.json())

    def test_create_duffel_flight_order(self):
        url = f"{self.base_url}/duffel-flights-create-orders"
        data = {
            "data": {
                "type": "order",
                "slices": [
                    {
                        "origin": "JFK",
                        "destination": "LAX",
                        "departure_date": "2023-10-01"
                    }
                ],
                "passengers": [
                    {
                        "type": "adult",
                        "given_name": "John",
                        "family_name": "Doe"
                    }
                ],
                "payments": [
                    {
                        "type": "balance",
                        "currency": "USD",
                        "amount": "100.00"
                    }
                ]
            }
        }
        response = requests.post(url, headers=self.headers, json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("data", response.json())

if __name__ == '__main__':
    unittest.main()