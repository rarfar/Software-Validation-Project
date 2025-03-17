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
    assert response.status_code == 201  #
    json_response = response.json()
    assert "id" in json_response  # Ensure the project has an auto-generated ID.
    assert json_response["title"] == payload["title"]
    assert json_response["completed"] == "false"  # The API stores booleans as strings.
    assert json_response["active"] == "true"  # The API stores booleans as strings.
    assert json_response["description"] == payload["description"]


# ----------------- Testing http://localhost:4567/projects/:id -----------------

# Test 4: GET /projects/:id - Return a specific instance of a project using an ID
def test_get_project_by_id():
    create_response = requests.post(BASE_URL + "/projects", json={"title": "Test Project"})
    assert create_response.status_code == 201
    project_id = create_response.json()["id"]

    response = requests.get(BASE_URL + f"/projects/{project_id}")
    assert response.status_code == 200
    json_data = response.json()
    assert "projects" in json_data
    assert json_data["projects"][0]["id"] == project_id


# Test 5: HEAD /projects/:id - Return headers for a specific instance of a project using an ID
def test_head_project_by_id():
    project_response = requests.post(BASE_URL + "/projects", json={"title": "Test Project Header"})
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    response = requests.head(BASE_URL + f"/projects/{project_id}")
    assert response.status_code == 200
    assert not response.text
    assert "Content-Type" in response.headers
    assert response.headers["Content-Type"] == "application/json"


# Test 6: POST /projects/:id - Amend a specific instance of a project using an ID
def test_post_project_by_id():
    project_response = requests.post(BASE_URL + "/projects", json={"title": "Original Project Title"})
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    updated_payload = {"title": "Updated Project Title"}
    amend_response = requests.post(BASE_URL + f"/projects/{project_id}", json=updated_payload)
    assert amend_response.status_code == 200

    updated_project = amend_response.json()
    assert updated_project["id"] == project_id
    assert updated_project["title"] == updated_payload["title"]


# Test 7: PUT /projects/:id - Fully update a specific instance of a project using an ID
def test_put_project_by_id():
    create_payload = {
        "title": "Original Project",
        "completed": False,
        "active": True,
        "description": "Initial description"
    }
    create_response = requests.post(BASE_URL + "/projects", json=create_payload)
    assert create_response.status_code == 201
    project_id = create_response.json()["id"]

    update_payload = {
        "title": "Updated Project",
        "completed": True,
        "active": False,
        "description": "Updated details"
    }
    update_response = requests.put(f"{BASE_URL}/projects/{project_id}", json=update_payload)
    assert update_response.status_code == 200

    json_data = update_response.json()
    assert json_data["id"] == project_id
    assert json_data["title"] == update_payload["title"]
    assert json_data["completed"] == "true" 
    assert json_data["active"] == "false"   
    assert json_data["description"] == update_payload["description"]


# Test 8: DELETE /projects/:id - Delete a specific instance of a project by ID
def test_delete_project_by_id():
    payload = {"title": "Project Delete"}
    create_response = requests.post(BASE_URL + "/projects", json=payload)
    assert create_response.status_code == 201
    project_id = create_response.json()["id"]

    response = requests.delete(f"{BASE_URL}/projects/{project_id}")
    assert response.status_code == 200
     

# Test 9 (UNDOCUMENTED): GET /projects/id: - Should return 404 Not Found for a non-existent project
def test_get_non_existent_project():
    project_response = requests.post(BASE_URL + "/projects", json={"title": "Temp Project"})
    assert project_response.status_code == 201
    existing_id = int(project_response.json()["id"])

    non_existent_id = existing_id + 1000
    response = requests.get(BASE_URL + f"/projects/{non_existent_id}")

    assert response.status_code == 404
    json_data = response.json()
    assert "errorMessages" in json_data
    assert f"Could not find an instance with projects/{non_existent_id}" in json_data["errorMessages"]


# ----------------- Testing http://localhost:4567/projects/:id/tasks -----------------                                                               

# Test 10: GET /projects/:id/tasks - Return all todo items related to project id
def test_get_project_tasks():
    project_response = requests.post(BASE_URL + "/projects", json={"title": "Project Task"})
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    response = requests.get(BASE_URL + f"/projects/{project_id}/tasks")
    assert response.status_code == 200
    json_data = response.json()

    assert "todos" in json_data
    assert isinstance(json_data["todos"], list)


# Test 11: HEAD /projects/:id/tasks -- Return headers for todo items related to project id
def test_head_project_tasks():
    project_response = requests.post(BASE_URL + "/projects", json={"title": "Project Task Header"})
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    response = requests.head(BASE_URL + f"/projects/{project_id}/tasks")
    assert response.status_code == 200
    assert not response.text 
    assert "Content-Type" in response.headers
    assert response.headers["Content-Type"] == "application/json"


# Test 12: POST /projects/:id/tasks -- Return headers for todo items related to project id
def test_post_project_task():
    project_response = requests.post(BASE_URL + "/projects", json={"title": "Project Task Posting"})
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    payload = {"title": "Task for Posting"}
    task_response = requests.post(BASE_URL + f"/projects/{project_id}/tasks", json=payload)
    assert task_response.status_code == 201
    assert "id" in task_response.json() 


# Test 13: GET /projects/:id/tasks - Retrieve tasks after linking todo to project
def test_get_project_tasks_after_post():
    project_response = requests.post(BASE_URL + "/projects", json={"title": "Project with Task"})
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    task_response = requests.post(BASE_URL + f"/projects/{project_id}/tasks", json={"title": "Test Task"})
    assert task_response.status_code == 201
    task_id = task_response.json()["id"]

    response = requests.get(f"{BASE_URL}/projects/{project_id}/tasks")
    assert response.status_code == 200
    json_data = response.json()

    assert "todos" in json_data
    assert any(task["id"] == task_id for task in json_data["todos"])


# Test 14 (UNDOCUMENTED): PUT /projects/:id/tasks with No Input - Should return 405 Method Not Allowed
def test_put_project_tasks_no_body():
    project_response = requests.post(BASE_URL + "/projects", json={"title": "Project for PUT Task Test"})
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    response = requests.put(BASE_URL + f"/projects/{project_id}/tasks")
    assert response.status_code == 405 


# ----------------- Testing http://localhost:4567/projects/:id/tasks/:id -----------------

# Test 15: DELETE /projects/:id/tasks/:id
def test_delete_project_task():
    project_response = requests.post(BASE_URL + "/projects", json={"title": "Project Delete Test Task"})
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    task_response = requests.post(BASE_URL + f"/projects/{project_id}/tasks", json={"title": "Test Task"})
    assert task_response.status_code == 201
    task_id = task_response.json()["id"]

    delete_response = requests.delete(f"{BASE_URL}/projects/{project_id}/tasks/{task_id}")
    assert delete_response.status_code  == 200


# ----------------- Testing http://localhost:4567/projects/:id/categories -----------------

# Test 16: GET /projects/id/categories - Retrieve all categories related to project id
def test_get_project_categories():
    project_response = requests.post(BASE_URL + "/projects", json={"title": "Project Categories"})
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    response = requests.get(f"{BASE_URL}/projects/{project_id}/categories")
    assert response.status_code == 200
    json_data = response.json()

    assert "categories" in json_data
    assert isinstance(json_data["categories"], list)

# Test 17: HEAD /projects/id/categories - Retrieve headers for all category related to project id
def test_head_project_categories():
    project_response = requests.post(BASE_URL + "/projects", json={"title": "Project Categories Header"})
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    response = requests.head(f"{BASE_URL}/projects/{project_id}/categories")
    assert response.status_code == 200

    assert not response.text
    assert response.headers.get("Content-Type") == "application/json"


# Test 18: POST /projects/id/categories - Create a new category for project id
def test_post_project_category():
    project_response = requests.post(BASE_URL + "/projects", json={"title": "Project Categories Posting"})
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    category_payload = {"title": "Test Category"}
    category_response = requests.post(BASE_URL + f"/projects/{project_id}/categories", json=category_payload)
    assert category_response.status_code == 201
    json_data = category_response.json()

    assert "id" in json_data
    assert json_data["title"] == category_payload["title"]

# Test 19: GET /projects/id/categories - Retrieve categories after creating a new category
def test_get_project_categories_after_post():
    project_response = requests.post(BASE_URL + "/projects", json={"title": "Project with Category"})
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    category_response = requests.post(BASE_URL + f"/projects/{project_id}/categories", json={"title": "Category 2"})
    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    response = requests.get(f"{BASE_URL}/projects/{project_id}/categories")
    assert response.status_code == 200
    json_data = response.json()
    assert "categories" in json_data
    assert any(category["id"] == category_id for category in json_data["categories"])


# ----------------- Testing http://localhost:4567/projects/:id/cateogories/:id -----------------

# Test 20: DELETE /projects/1/categories/1 - Remove category from project 
def test_delete_project_category():
    project_payload = {"title": "Project for Category Deletion"}
    project_response = requests.post(BASE_URL + "/projects", json=project_payload)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    category_payload = {"title": "Category to Delete"}
    category_response = requests.post(f"{BASE_URL}/projects/{project_id}/categories", json=category_payload)
    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    delete_response = requests.delete(f"{BASE_URL}/projects/{project_id}/categories/{category_id}")
    assert delete_response.status_code == 200


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
