import requests
import pytest
import xml.etree.ElementTree as ET

BASE_URL = "http://localhost:4567"

# Emmy Song - 261049871 - emmy.song@mail.mcgill.ca

def test_can_call_endpoint():
    response = requests.get(BASE_URL)
    assert response.status_code == 200           

# ----------------- Testing http://localhost:4567/projects -----------------

# Test 1: GET /projects - Retrieve all projects
def test_get_projects():
    response = requests.get(BASE_URL + "/projects")
    assert response.status_code == 200 
    assert "projects" in response.json()  

# Test 2: HEAD /projects - Retrieve headers
def test_head_projects():
    response = requests.head(BASE_URL + "/projects")
    assert response.status_code == 200 
    assert not response.text  
    assert 'Content-Type' in response.headers  
    assert response.headers['Content-Type'] == 'application/json'  

# Test 3: POST /projects - Create a new project
def test_post_projects_full_payload():
    payload = {
        "title": "Test Project",
        "completed": False,
        "active": True,
        "description": "This is a test project"
    }
    response = requests.post(BASE_URL + "/projects", json=payload)
    assert response.status_code == 201  # The request succeeded, and a new resource was created.
    json_response = response.json()
    assert "id" in json_response  # Ensure the project has an auto-generated ID.
    assert json_response["title"] == payload["title"]
    assert json_response["completed"] == "false"  # The API stores booleans as strings.
    assert json_response["active"] == "true"  # The API stores booleans as strings.
    assert json_response["description"] == payload["description"]

# ----------------- Testing http://localhost:4567/projects/:id -----------------

# Test 4: GET /projects/:id - Return a specific instance of a project using an ID
def test_get_project_by_id():
    response = requests.get(BASE_URL + "/projects/1")
    assert response.status_code == 200  # Success: Project exists
    json_data = response.json()
    assert "projects" in json_data
    assert json_data["projects"][0]["id"] == "1"

# Test 5: HEAD /projects/:id - Return headers for a specific instance of a project using an ID
def test_head_project_by_id():
    response = requests.head(BASE_URL + "/projects/1")
    assert response.status_code == 200  # Success: Project exists
    assert not response.text  # Ensures response body is empty
    assert "Content-Type" in response.headers
    assert response.headers["Content-Type"] == "application/json"

# Test 6: POST /projects/:id - Amend a specific instance of a project using an ID
def test_post_project_by_id():
    payload = {
        "title": "Updated Project Title"
    }
    response = requests.post(BASE_URL + "/projects/1", json=payload)
    assert response.status_code == 200  # Project should be updated
    json_data = response.json()
    assert json_data["id"] == "1"
    assert json_data["title"] == payload["title"]

# Test 7: PUT /projects/:id - Fully update a specific instance of a project using an ID
def test_put_project_by_id():
    payload = {
        "title": "Updated Project",
        "completed": True,
        "active": False,
        "description": "Updated details"
    }
    response = requests.put(BASE_URL + "/projects/1", json=payload)
    assert response.status_code == 200  # Success: Project is updated
    json_data = response.json()
    assert json_data["id"] == "1"
    assert json_data["title"] == payload["title"]
    assert json_data["completed"] == "true"  # API returns boolean as string
    assert json_data["active"] == "false"  # API returns boolean as string
    assert json_data["description"] == payload["description"]

# Test 8: DELETE /projects/:id - Delete a specific instance of a project by ID
def test_delete_project_by_id():
    response = requests.delete(BASE_URL + "/projects/2")
    assert response.status_code in [200]  

# Test 9 (UNDOCUMENTED): GET /projects/id: - Should return 404 Not Found for a non-existent project
def test_get_non_existent_project():
    response = requests.get(BASE_URL + "/projects/101")
    
    assert response.status_code == 404  # Expect 404 Not Found
    json_data = response.json()

    assert "errorMessages" in json_data  # Ensure error message is present
    assert "Could not find an instance with projects/101" in json_data["errorMessages"]

# ----------------- Testing http://localhost:4567/projects/:id/tasks -----------------                                                               

# Test 10: GET /projects/1/tasks - Return all todo items related to project 1
def test_get_project_tasks():
    response = requests.get(BASE_URL + "/projects/1/tasks")  
    assert response.status_code == 200  
    json_data = response.json()
    assert "todos" in json_data  # Ensure "todos" is present in response
    assert isinstance(json_data["todos"], list)  # Ensure it's a list
    assert json_data["todos"] == []

# Test 11: HEAD /projects/1/tasks -- Return headers for todo items related to project 1
def test_head_project_tasks():
    response = requests.head(BASE_URL + "/projects/1/tasks")
    assert response.status_code == 200  
    assert not response.text  
    assert "Content-Type" in response.headers  
    assert response.headers["Content-Type"] == "application/json"

# Test 12: HEAD /projects/1/tasks -- Return headers for todo items related to project 1
def test_post_project_task():
    payload = {
        "id": "1"  #
    }
    response = requests.post(BASE_URL + "/projects/1/tasks", json=payload)
    assert response.status_code == 201

# Test 13: GET /projects/1/tasks - Retrieve tasks after linking todo to project
def test_get_project_tasks_after_post():
    response = requests.get(BASE_URL + "/projects/1/tasks")
    
    assert response.status_code == 200 
    json_data = response.json()

    assert "todos" in json_data  
    assert isinstance(json_data["todos"], list) 
    assert len(json_data["todos"]) > 0 

    # Validate the structure of the response
    todo = json_data["todos"][0]
    assert todo["id"] == "1"
    assert todo["title"] == "scan paperwork"
    assert todo["doneStatus"] == "false"
    assert todo["description"] == ""

    # Validate the task relationship
    assert "tasksof" in todo
    assert any(task["id"] == "1" for task in todo["tasksof"])  # Ensure linked project ID is present

    # Validate the categories structure exists (even if empty)
    assert "categories" in todo

# Test 14 (UNDOCUMENTED): PUT /projects/1/tasks with No Input - Should return 405 Method Not Allowed
def test_put_project_tasks_no_body():
    response = requests.put(BASE_URL + "/projects/1/tasks")
    assert response.status_code == 405  

# ----------------- Testing http://localhost:4567/projects/:id/tasks/:id -----------------

# Test 15: DELETE /projects/1/tasks/1 -- Remove task 1 from project 1
def test_delete_project_task():
    response = requests.delete(BASE_URL + "/projects/1/tasks/1")
    assert response.status_code == 200

# ----------------- Testing http://localhost:4567/projects/:id/categories -----------------

# Test 16: GET /projects/1/categories - Retrieve all categories related to project 1
def test_get_project_categories():
    response = requests.get(BASE_URL + "/projects/1/categories")

    assert response.status_code == 200  
    json_data = response.json()
    assert "categories" in json_data 
    assert isinstance(json_data["categories"], list)  
    assert json_data["categories"] == []  

# Test 17: HEAD /projects/1/categories - Retrieve headers for all category related to project 1
def test_head_project_categories():
    response = requests.head(BASE_URL + "/projects/1/categories")

    assert response.status_code == 200  
    assert not response.text 
    assert "Content-Type" in response.headers  
    assert response.headers["Content-Type"] == "application/json"

# Test 18: POST /projects/1/categories - Create a new category for project 1
def test_post_project_category():
    payload = {
        "id": "2"  # ID of the existing category
    }
    response = requests.post(BASE_URL + "/projects/1/categories", json=payload)
    
    assert response.status_code == 201  # Expect 201 Created

# Test 19: GET /projects/1/categories - Retrieve categories after creating a new category
def test_get_project_categories_after_post():
    response = requests.get(BASE_URL + "/projects/1/categories")

    assert response.status_code == 200  # Expect 200 OK
    json_data = response.json()

    assert "categories" in json_data 
    assert isinstance(json_data["categories"], list) 
    assert any(category["id"] == "2" for category in json_data["categories"])

    # Validate Category ID 2 details
    for category in json_data["categories"]:
        if category["id"] == "2":
            assert category["title"] == "Home"
            assert category["description"] == ""


# ----------------- Testing http://localhost:4567/projects/:id/cateogories/:id -----------------

# Test 20: DELETE /projects/1/categories/1 - Remove category 2 from project 1
def test_delete_project_category():
    response = requests.delete(BASE_URL + "/projects/1/categories/2")
    assert response.status_code in [200]

# ----------------- XML Payload Handling -----------------

# Test 21: XML - GET /projects - return all instances of projects
def test_xml_get_projects():
    response = requests.get(BASE_URL + "/projects", headers={'Accept': 'application/xml'})
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/xml'
    root = ET.fromstring(response.text)
    assert root.tag == "projects"

# Test 22: XML - HEAD /projects - return headers for all instances of projects
def test_xml_head_projects():
    response = requests.head(BASE_URL + "/projects", headers={'Accept': 'application/xml'})
    assert response.status_code == 200
    assert not response.text
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/xml'

# Test 23: XML - POST /projects - create a project without an ID using field values in body
def test_xml_post_projects():
    response = requests.post(BASE_URL + "/projects", data="""<project>
                    <completed>false</completed>
                    <title>XML Project Test</title>
                </project>""", headers={'Content-Type': 'application/xml'})
    assert response.status_code == 201
