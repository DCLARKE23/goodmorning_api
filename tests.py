import unittest, json
from flask import Flask
from app import app

class Tests(unittest.TestCase):
    def client(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    # Weather - Good Requests
    def test_weather_get_no_id(self):
        response = self.app.get('/weather')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, list)
    
    def test_weather_get_id(self):
        response = self.app.get("/weather/1")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response), 0)
        self.assertIsInstance(response, list)
        self.assertEqual(response.json["id"], 1)

    def test_weather_post(self):
        response = self.app.post("/weather", json={"name": "toronto"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.data)) # not sure if this works or is necessary
        
    def test_weather_put(self):
        response = self.app.put("/weather/1", json={"name": "vancouver"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Location with ID:1 updated.')

    def test_weather_delete(self):
        response = self.app.delete("/weather/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Location with ID:1 removed.')
    
    # Tasks - Good Requests
    def test_task_get(self):
        response = self.app.get("/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, list)

    def test_task_post(self):
        response = self.app.post("/tasks", json={"task": "wash car", "time": 20})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.data)) 

    def test_task_put(self):
        response = self.app.put("/tasks/1", json={"task": "brush teeth", "time": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Task with ID:1 updated.')

    def test_task_delete(self):
        response = self.app.delete("/tasks/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Task with ID:1 removed.')
    
    # Links - Good Requests    
    def test_link_get(self):
        response = self.app.get('/links')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, list)

    def test_link_post(self):
        response = self.app.post('/links', json={"url": "www.youtube.com", "name": "YouTube"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.data))

    def test_link_put(self):
        response = self.app.post('/links/1', json={"url": "www.google.com", "name": "Google"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Link with ID:1 updated.')

    def test_link_delete(self):
        response = self.app.delete("/tasks/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Link with ID:1 removed.')