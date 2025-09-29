
import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_health(self):
        r = client.get("/health")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json().get("status"), "ok")

    def test_create_and_get_item(self):
        payload = {"id": 10, "name": "t", "value": 2.5}
        r = client.post("/items", json=payload)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json().get("created"))

        r2 = client.get("/items/10")
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r2.json().get("name"), "t")

    def test_compute(self):
        r = client.post("/compute", json={"x":3,"y":4})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json().get("sum"), 7)
