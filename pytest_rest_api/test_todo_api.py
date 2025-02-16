import requests
import pytest
import xml.etree.ElementTree as ET

BASE_URL = "http://localhost:4567"

"""Test 1: to ensure we can call endpoint/base URL successfully """
def test_can_call_endpoint():
    response = requests.get(BASE_URL)
    assert response.status_code == 200                           # HTTP Success code

#TESTING http://localhost:4567/todos
"""Test 2:  GET /todos -- return all the instances of todo"""
def test_get_todos():
    response = requests.get(BASE_URL + "/todos")
    assert response.status_code == 200                            # Success: The resource has been fetched and transmitted in the message body.
    assert "todos" in response.json()                             # is checking whether the JSON response from the API contains a key named "todos"

"""Test 3: HEAD /todos -- returns headers for all the instances of todo """
def test_head_todos():
    response = requests.head(BASE_URL + "/todos")
    assert response.status_code == 200                            # Success: The resource has been fetched and transmitted in the message body.
    assert not response.text                                      # Ensures the response body is empty (as expected for HEAD requests).
    assert 'Content-Type' in response.headers                     # This ensures the API is returning properly formatted HTTP headers.
    assert response.headers['Content-Type'] == 'application/json' # Verifies that the API correctly sets the Content-Type to JSON.
                                                                  # Even though the HEAD response has no body, it still needs to indicate the expected format.

"""Test 4: POST /todos -- we should be able to create todo without a ID using the field values in the body of the message"""
def test_post_todos_full_payload():
    payload = {
            "title": "test full payload",
            "doneStatus": False,
            "description": "test description4",
        }
    response = requests.post(BASE_URL + "/todos", json=payload)
    assert response.status_code == 201                            # The request succeeded, and a new resource was created as a result. This is typically the response sent after POST requests, or some PUT requests.
    assert response.json()['title'] == payload['title']

"""Test 5: POST /todos -- only supply title """
def test_post_todos_only_title():
    payload = {
        "title": "test only title",
    }
    response = requests.post(BASE_URL + "/todos", json=payload)
    assert response.status_code == 201                            # The request succeeded, and a new resource was created as a result. This is typically the response sent after POST requests, or some PUT requests.
    assert response.json()['title'] == payload['title']

"""Test 6: POST /todos -- only supply description which is missing mandatory title"""
def test_post_todos_invalid_field():
    payload = {
        "description": "test description",
    }
    response = requests.post(BASE_URL + "/todos", json=payload)
    assert response.status_code == 400                             # The server cannot or will not process the request due to something that is perceived to be a client error.

"""Test 7: POST /todos -- supply title but invlaid type of done status (should be bool)"""
def test_post_todos_invalid_type():
    payload = {
        "title": "test title with invalid done status",
        "doneStatus": "false",
    }
    response = requests.post(BASE_URL + "/todos", json=payload)
    assert response.status_code == 400                             # The server cannot or will not process the request due to something that is perceived to be a client error.

"""Test 8: UNDOCUMENTED PUT /todos -- use PUT instead of POST -- should be not allowed"""
def test_put_todos():
    payload = {
        "title": "test put",
        "doneStatus": False,
        "description": "test description8",
    }
    response = requests.put(BASE_URL + "/todos", json=payload)
    assert response.status_code == 405                              # Method Not Allowed - The request method is known by the server but is not supported by the target resource.

#TESTING http://localhost:4567/todos/:id

"""Test 9: GET /todos/:id -- return a specific instances of todo using a id """
def test_get_todos_id():
    response = requests.get(BASE_URL + "/todos/1")
    assert response.status_code == 200                # Success: The resource has been fetched and transmitted in the message body.
    assert response.json()['todos'][0]["id"] == "1"   # assert the returned todos has id 1
    assert len(response.json()["todos"]) == 1         # assert the response only returns one todos

"""Test 10: GET /todos/:id -- using id 9999 which we know does not exist"""
def test_get_todos_id_invalid():
    response = requests.get(BASE_URL + "/todos/9999")
    assert response.status_code == 404                # 404 Not Found: The server cannot find the requested resource.

"""Test 11: HEAD /todos/:id -- returns headers for a specific instance of todo using a id """
def test_head_todos_id():
    response = requests.head(BASE_URL + "/todos/1")
    assert response.status_code == 200                             # Success: The resource has been fetched and transmitted in the message body.
    assert not response.text                                       # Ensures the response body is empty (as expected for HEAD requests).
    assert 'Content-Type' in response.headers                      # This ensures the API is returning properly formatted HTTP headers.
    assert response.headers['Content-Type'] == 'application/json'  # Verifies that the API correctly sets the Content-Type to JSON.
                                                                   # Even though the HEAD response has no body, it still needs to indicate the expected format.

"""Test 12: POST /todos/:id -- amend a specific instances of todo using a id with a body containing the fields to amend"""
def test_post_todos_id():
    payload = {
        "doneStatus": True,
    }
    response = requests.post(BASE_URL + "/todos/1", json=payload)
    assert response.status_code == 200  # success
    assert 'doneStatus' in response.json()  # is checking whether the JSON response from the API contains a key named "doneStatus"
    assert response.json()['doneStatus'] == 'true'  # ensure doneStatus updated correctly

"""Test 13: PUT /todos/:id -- amend a specific instances of todo using a id with a body containing the fields to amend"""
def test_put_todos_id():
    payload = {
        "title": "new title test 12",
        "doneStatus": True,
        "description": "new desc 12",
    }
    response = requests.post(BASE_URL + "/todos/1", json=payload)
    assert response.status_code == 200                           # success
    assert 'title' in response.json()                            # is checking whether the JSON response from the API contains a key named "title"
    assert response.json()['title'] == 'new title test 12'       # ensure title updated correctly
    assert 'doneStatus' in response.json()                       # is checking whether the JSON response from the API contains a key named "doneStatus"
    assert response.json()['doneStatus'] == 'true'               # ensure doneStatus updated correctly

"""Test 14: PUT /todos/:id -- do not supply new title which is required for put"""
def test_put_todos_id_invalid():
    payload = {
        "doneStatus": True,
    }
    response = requests.put(BASE_URL + "/todos/1", json=payload)
    assert response.status_code == 400                           # The server cannot or will not process the request due to something that is perceived to be a client error.

"""Test 15: DELETE /todos/:id -- delete a specific instances of todo using a id"""
def test_delete_todos_id():
    todo2 = requests.get(BASE_URL + "/todos/2")
    response = requests.delete(BASE_URL + "/todos/2")
    todos = requests.get(BASE_URL + "/todos")
    assert response.status_code == 200                          # Success
    assert todo2 not in todos                                   # checking to see if todos with id 1 was actually deleted

"""Test 16: DELETE /todos/:id --  delete an instance of todo that does not exist"""
def test_delete_todos_id_invalid():
    response = requests.delete(BASE_URL + "/todos/9999")
    assert response.status_code == 404                          # 404 Not Found: The server cannot find the requested resource.

#TESTING http://localhost:4567/todos/:id/taskof

"""Test 17: GET /todos/:id/tasksof -- return all the project items related to todo, with given id, by the relationship named tasksof """
def test_get_todo_id_tasksof():
    response = requests.get(BASE_URL + '/todos/1/tasksof')
    assert response.status_code == 200
    assert "projects" in response.json()                           # Checks if "projects" exists as a top-level key in the JSON response

"""Test 18: HEAD /todos/:id/tasksof -- headers for the project items related to todo, with given id, by the relationship named tasksof """
def test_head_todo_id_tasksof():
    response = requests.head(BASE_URL + '/todos/2/tasksof')
    assert response.status_code == 200                             # Success: The resource has been fetched and transmitted in the message body.
    assert not response.text                                       # Ensures the response body is empty (as expected for HEAD requests).


"""Test 19: POST /todos/:id/tasksof -- create an instance of a relationship named tasksof between todo instance :id and the project instance represented by the id in the body of the message"""
def test_post_todo_id_tasksof():
    response = requests.post(BASE_URL + '/todos/1/tasksof', json={'title':'Class Work'})
    assert response.status_code == 201                             #  The request succeeded, and a new resource was created as a result. This is typically the response sent after POST requests, or some PUT requests.
    assert response.json()['title'] == 'Class Work'

""" Test 20: UNDOCUMENTED DELETE /todos/:id/tasksof"""
def test_delete_todo_id_taskof():
    response = requests.delete(BASE_URL + "/todos/2/tasksof")
    assert response.status_code == 405   # NOT ALLOWED


#TESTING http://localhost:4567/todos/:id/tasksof/:id

"""Test 21: DELETE /todos/:id/tasksof/:id -- delete the instance of the relationship named tasksof between todo and project using the :id"""
def test_delete_todo_taskof_id():
    task1 = requests.get(BASE_URL + "/todos/1/tasksof/1")
    response = requests.delete(BASE_URL + "/todos/1/tasksof/1")
    tasks = requests.get(BASE_URL + "/todos/1/tasksof")
    assert response.status_code == 200                            # Success
    assert task1 not in tasks                                     # Check that delete actually removes element

"""Test 22: DELETE /todos/:id --  delete an instance of todo taskof that does not exist"""
def test_delete_todo_taskof_id_invalid():
    response = requests.delete(BASE_URL + "/todos/1/taskof/9999")
    assert response.status_code == 404                           # 404 Not Found: The server cannot find the requested resource.

#TESTING http://localhost:4567/todos/:id/categories

"""Test 23:  GET /todos/:id/categories -- return all the category items related to todo, with given id, by the relationship named categories"""
def test_get_todo_id_categories():
    response = requests.get(BASE_URL + '/todos/1/categories')
    assert response.status_code == 200
    assert "categories" in response.json()  # Checks if "projects" exists as a top-level key in the JSON response


"""Test 24: HEAD /todos/:id/categories -- headers for the category items related to todo, with given id, by the relationship named categories"""
def test_head_todo_id_categories():
    response = requests.head(BASE_URL + "/todos/1/categories")
    assert response.status_code == 200
    assert not response.text                                      # Ensures the response body is empty (as expected for HEAD requests)

"""Test 25: POST /todos/:id/categories -- create an instance of a relationship named categories between todo instance :id and the category instance represented by the id in the body of the message"""
def test_post_todo_id_categories():
    response = requests.post(BASE_URL + "/todos/1/categories",json={'title':'Work'})
    assert response.status_code == 201                           # The request succeeded, and a new resource was created as a result. This is typically the response sent after POST requests, or some PUT requests.
    assert response.json()['title'] == 'Work'

#TESTING http://localhost:4567/todos/:id/categories/:id

"""Test 26: DELETE /todos/:id/categories/:id -- delete the instance of the relationship named categories between todo and category using the :id"""
def test_delete_todo_id_categories_id():
    category1 = requests.get(BASE_URL + "/todos/1/categories/1")
    response = requests.delete(BASE_URL + "/todos/1/categories/1")
    categories = requests.get(BASE_URL + "/todos/1/categories")
    assert response.status_code == 200  # Success
    assert category1 not in categories  # Check that delete actually removes element


"""Test 27: DELETE /todos/:id --  delete an instance of categories that does not exist"""
def test_delete_todos_id_categories_id_invalid():
    response = requests.delete(BASE_URL + "/todos/1/categories/9999")
    assert response.status_code == 404                          # 404 Not Found: The server cannot find the requested resource.


#TESTING http://localhost:4567/todos with XML

"""Test 28: XML - GET /todos -- return all the instances of todo"""
def test_xml_get_todos():
    response = requests.get(BASE_URL + "/todos", headers={'Accept': 'application/xml'})
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/xml'
    root = ET.fromstring(response.text)
    assert root.tag == "todos"

"""Test 29: XML - HEAD /todos -- returns headers for all the instances of todo"""
def test_xml_head_todos():
    response = requests.head(BASE_URL + "/todos", headers={'Accept': 'application/xml'})
    assert response.status_code == 200
    assert not response.text
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/xml'


"""Test 30: XML - POST /todos -- we should be able to create todo without a ID using the field values in the body of the message"""
def test_xml_post_todos():
    response = requests.post(BASE_URL + "/todos",data="""<todo>
                    <doneStatus>true</doneStatus>
                    <title>pi is 3.14</title>
                    <description>purple</description>
                </todo>""", headers={'Content-Type': 'application/xml'})
    assert response.status_code == 201














