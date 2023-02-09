from fastapi.testclient import TestClient

from main import app

import unittest


class TestStringMethods(unittest.TestCase):
    client = TestClient(app)

    def test_upper(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/').json(), 200)

    def test_upper1(self):
        self.assertEqual(self.client.get('/').status_code, 200)
