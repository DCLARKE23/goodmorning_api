import json, pytest
from app import app, City

# test for good input and bad input
# TODO actually read the documentation and fix this garbage

# Good Requests
def test_weather_get_no_id(client): # no request body, should return a list
    response = client.get("/weather")
    assert response is not None # no null reply
    assert isinstance(response,list)    # response is of type list

def test_weather_get_id(client):  # test that get method returns item of id 1
    response = client.get("/weather/1")
    assert response is not None # no null response
    assert len(response) != 0   # list not empty
    assert isinstance(response, list) # response is of type list
    assert response.json["id"] == 1 # response id is 1

def test_weather_post(client): # post unique city to weather table, post returns json with id and name
    response = client.post("/weather", json={"name": "toronto"})
    assert response is not None # no null response
    assert json.loads(response.data) # if response is not json, post failed
    
def test_weather_put(client):
    response = client.put("/weather/1", json={"name": "vancouver"})
    assert response.data == "Location with ID:1 updated."

def test_weather_delete(client):  # no request body
    response = client.delete("/weather/1")
    assert response is not None
    assert response.data == "Location with ID:1 updated."
# Bad requests
# TODO: determine how HTTP response codes are returned
def test_bad_weather_get_id(client):
    response = client.get("/weather/" + str(len(City) + 1))
    assert response.data == 404

def test_weather_post_invalid_city(client):
    pass

def test_weather_post_duplicate_city(client):
    pass

def test_bad_weather_put(client):
    pass

def test_bad_weather_delete(client):
    pass


# Good requests
def test_link_get(client):
    pass

def test_link_post(client):
    pass

def test_link_put(client):
    pass

def test_link_delete(client):
    pass
# Bad requests
def test_bad_link_get(client):
    pass

def test_bad_link_post(client):
    pass

def test_bad_link_put(client):
    pass

def test_bad_link_delete(client):
    pass

# Good requests
def test_task_get(client):
    response = client.get("/tasks")
    assert response is not None
    assert isinstance(response,list)

def test_task_post(client):
    response = client.post("/tasks", json={"task": "wash car", "time": 20})
    assert response is not None # no null response
    assert json.loads(response.data) # if response is not json, post failed

def test_task_put(client):
    response = client.put("/tasks/1", json={"task": "brush teeth", "time": 2})
    assert response.data == "Task with ID:1 updated."

def test_task_delete(client):
    pass
# Bad requests
def test_bad_task_get(client):
    pass

def test_bad_task_post(client):
    pass

def test_bad_task_put(client):
    pass

def test_bad_task_delete(client):
    pass
