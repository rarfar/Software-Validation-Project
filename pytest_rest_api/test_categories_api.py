import requests

# Brenden Trudeau - 260 941 695 - brenden.trudeau@mail.mcgill.ca

'''
    Categories json format:
    {
        "id": "21",                             # not mandatory
        "title": "iam, quis nostrud ex",        # mandatory
        "description": "e et dolore magna al"   # not mandatory
    }

    Categories XML format:
    <category>
        <description>e et dolore magna al</description> # not mandatory
        <id>21</id>                                     # not mandatory
        <title>iam, quis nostrud ex</title>             # mandatory
    </category>
'''


BASE_URL = "http://localhost:4567"


# TESTING https://localhost:4567/categories

""" Test 1: GET /categories - return all the instances of categories """
def test_get_categories():
    response = requests.get(BASE_URL + "/categories")
    assert response.status_code == 200                              # The request has succeeded.
    assert "categories" in response.json()                          # The response contains a key named "categories"


""" Test 2: POST /categories - create a new category """
def test_post_categories():
    payload = {
            "title": "test full payload",
            "description": "test 2 categories"
        }
    response = requests.post(BASE_URL + "/categories", json=payload)
    assert response.status_code == 201                              # The request has been fulfilled and has resulted in new resources being created.
    assert response.json()['title'] == payload['title']             # The response contains the title of the new category

""" Test 3: POST /categories - create a new category with no title """
def test_post_categories_no_title():
    payload = {
            "description": "test 3 categories no title"
        }
    response = requests.post(BASE_URL + "/categories", json=payload)
    assert response.status_code == 400                              # The server could not understand the request due to invalid syntax.

""" Test 4: HEAD /categories - return the headers of the response """
def test_head_categories():
    response = requests.head(BASE_URL + "/categories")
    assert response.status_code == 200                              # The request has succeeded.
    assert not response.text                                        # The response body is empty as should be for a HEAD request
    assert "Content-Type" in response.headers                       # The response contains a key named "Content-Type"
    assert response.headers['Content-Type'] == 'application/json'   # The response Content-Type is application/json


# TESTING https://localhost:4567/categories/:id

""" Test 5: GET /categories/:id - return a specific category """
def test_get_categories_id():
    payload = {
        "title": "title test 5 categories"
    }
    cat_response = requests.post(BASE_URL + "/categories", json=payload)    # Create a new category to get the id and then get it
    assert cat_response.status_code == 201                                  # The request has been fulfilled and has resulted in new resources being created.
    cat_id = cat_response.json()['id']
    response = requests.get(BASE_URL + f"/categories/{cat_id}")
    assert response.status_code == 200                                      # The request has succeeded.
    assert response.json()['categories'][0]['id'] == f"{cat_id}"             # The response contains the id of the category

""" Test 6: GET /categories/:id - return a specific category that does not exist """
def test_get_categories_id_invalid_id():
    invalid_id = 99999
    response = requests.get(BASE_URL + f"/categories/{invalid_id}")
    assert response.status_code == 404                                                                          # The server has not found a resource matching the request URI.
    assert response.json()['errorMessages'] == [f"Could not find an instance with categories/{invalid_id}"]     # The response contains an error message

""" Test 7: PUT /categories/:id - update a specific category """
def test_put_categories_id():
    payload = {
            "title": "title test 7 categories",
            "description": "description test 7 categories"
        }
    updated_payload = {
        "title": "title test 7 categories updated"
    }
    cat_response = requests.post(BASE_URL + "/categories", json=payload)    # Create a new category to be updated
    assert cat_response.status_code == 201                                  # The request has been fulfilled and has resulted in new resources being created.
    cat_id = cat_response.json()['id']
    response = requests.put(BASE_URL + f"/categories/{cat_id}", json=updated_payload)
    assert response.status_code == 200                              # The request has succeeded.            
    assert response.json()['title'] == updated_payload['title']             # The response contains the title of the updated category

""" Test 8: DELETE /categories/:id - delete a specific category """
def test_delete_categories_id():
    payload = {
            "title": "title test 8 categories DELETE",
            "description": "description test 8 categories"
        }
    put_response = requests.post(BASE_URL + "/categories", json=payload)    # Create a new category to be deleted
    assert put_response.status_code == 201                                  # The request has been fulfilled and has resulted in new resources being created.
    cat_id = put_response.json()['id']
    response = requests.delete(BASE_URL + "/categories/" + cat_id)
    assert response.status_code == 200                                      # The request has succesfully been deleted.

""" Test 9: POST /categories/:id - update a specific category """
def test_post_categories_id():
    payload = {
            "title": "title test 9 categories",
            "description": "description test 9 categories"
        }
    updated_payload = {
        "title": "title test 9 categories updated",
        "description": "description test 9 categories"
    }
    cat_response = requests.post(BASE_URL + "/categories", json=payload)    # Create a new category to be updated
    assert cat_response.status_code == 201                                  # The request has been fulfilled and has resulted in new resources being created.
    cat_id = cat_response.json()['id']

    response = requests.post(BASE_URL + f"/categories/{cat_id}", json=updated_payload)
    assert response.status_code == 200                                      # The request has succeeded.                  
    assert response.json()['title'] == updated_payload['title']                     # The response contains the title of the updated category
    assert response.json()['description'] == updated_payload['description']         # The response contains the description of the updated category

""" Test 10: HEAD /categories/:id - return the headers of the response """
def test_head_categories_id():
    payload = {
            "title": "title test 10 categories",
            "description": "description test 10 categories"
    }
    cat_response = requests.post(BASE_URL + "/categories", json=payload)    # Create a new category to get the id and then check its headers
    assert cat_response.status_code == 201                                  # The request has been fulfilled and has resulted in new resources being created.
    cat_id = cat_response.json()['id']

    response = requests.head(BASE_URL + f"/categories/{cat_id}")
    assert response.status_code == 200                                      # The request has succeeded.
    assert not response.text                                                # The response body is empty as should be for a HEAD request
    assert "Content-Type" in response.headers                               # The response contains a key named "Content-Type"
    assert response.headers['Content-Type'] == 'application/json'           # The response Content-Type is application/json


# TESTING https://localhost:4567/categories/:id/projects

""" Test 11: GET /categories/:id/projects - return all the project items related to category, with given id, by the relationship named projects """
def test_get_categories_id_projects():
    payload = {
            "title": "title test 11 categories"
    }
    cat_response = requests.post(BASE_URL + "/categories", json=payload)    # Create a new category to get the id and then get the projects related to it
    assert cat_response.status_code == 201                                  # The request has been fulfilled and has resulted in new resources being created.
    cat_id = cat_response.json()['id']

    response = requests.get(BASE_URL + f"/categories/{cat_id}/projects")
    assert response.status_code == 200                                      # The request has succeeded.
    assert "projects" in response.json()                                    # The response contains a key named "projects"

""" Test 12: GET /categories/:id/projects - with invalid id, this is a known bug should output 404 but outputs 200 instead """
def test_get_categories_id_projects_invalid_id():
    invalid_id = 99999
    response = requests.get(BASE_URL + f"/categories/{invalid_id}/projects")                                    
    assert response.status_code == 404, (f"BUG! Expected a 404 status code, but got {response.status_code}")    # The server has not found a resource matching the request URI.

""" Test 13: HEAD /categories/:id/projects - headers for the project items related to category, with given id, by the relationship named projects """
def test_head_categories_id_projects():
    category_payload = {
            "title": "title test 13 categories",
            "description": "description test 13 categories"
        }
    category_response = requests.post(BASE_URL + "/categories", json=category_payload)
    assert category_response.status_code == 201                                         # Succesfully posted a category to get the id and then check its headers
    category_id = category_response.json()['id']

    response = requests.head(BASE_URL + f"/categories/{category_id}/projects")
    assert response.status_code == 200                                                  # The request has succeeded.
    assert not response.text                                                            # The response body is empty as should be for a HEAD request
    assert "Content-Type" in response.headers                                           # The response contains a key named "Content-Type"
    assert response.headers['Content-Type'] == 'application/json'                       # The response Content-Type is application/json

""" Test 14: POST /categories/:id/projects - create a new project item related to category, with given id, by the relationship named projects """
def test_post_categories_id_projects():
    category_payload = {
            "title": "title test 14 categories",
            "description": "description test 11 categories"
        }
    project_payload = {
            "title": "title test 14 projects",
        }
    category_response = requests.post(BASE_URL + "/categories", json=category_payload)
    assert category_response.status_code == 201                                                     # Succesfully posted a category to get the id and then create a relationship with a project
    category_id = category_response.json()['id']

    response = requests.post(BASE_URL + f"/categories/{category_id}/projects", json=project_payload)
    assert response.status_code == 201                                                              # Succesfully created a project related to the category
    assert response.json()['title'] == project_payload['title']


# TESTING https://localhost:4567/categories/:id/projects/:id

""" Test 15: DELETE /categories/:id/projects/:id - delete a specific project item related to category, with given id, by the relationship named projects """
def test_delete_categories_id_projects_id():
    category_payload = {
            "title": "title test 15 categories",
            "description": "description test 15 categories"
        }
    project_payload = {
            "title": "title test 15 projects",
        }
    category_response = requests.post(BASE_URL + "/categories", json=category_payload)
    assert category_response.status_code == 201                                             # Succesfully created a category to get the id and then create a relationship with a project and then delete
    category_id = category_response.json()['id']

    project_response = requests.post(BASE_URL + "/projects", json=project_payload)
    assert project_response.status_code == 201                                              # Succesfully created a project to get the id and then create a relationship with a category and then delete
    project_id = project_response.json()['id']

    relationship_payload = {"id": project_id}
    relationship_response = requests.post(BASE_URL + f"/categories/{category_id}/projects",json=relationship_payload)   # Succesfully created a relationship between the category and project
    assert relationship_response.status_code == 201

    response = requests.delete(BASE_URL + f"/categories/{category_id}/projects/{project_id}")
    assert response.status_code == 200                                                      # Succesfully deleted the relationship between the category and project

# TESTING https://localhost:4567/categories/:id/todos

""" Test 16: GET /categories/:id/todos - return all the todo items related to category, with given id, by the relationship named todos """
def test_get_categories_id_todos():
    category_payload = {
            "title": "title test 16 categories",
            "description": "description test 16 categories"
        }
    category_response = requests.post(BASE_URL + "/categories", json=category_payload)
    assert category_response.status_code == 201                                             # Succesfully created a category to get the id and then get the todos related to it
    category_id = category_response.json()['id']

    response = requests.get(BASE_URL + f"/categories/{category_id}/todos")
    assert response.status_code == 200                                                      # The request has succeeded.              
    assert "todos" in response.json()

""" Test 17: GET /categories/:id/todos - with invalid id, this is a known bug should output 404 but outputs 200 instead """
def test_get_categories_id_todos_invalid_id():
    invalid_id = 99999
    response = requests.get(BASE_URL + f"/categories/{invalid_id}/todos")
    assert response.status_code == 404, (f"BUG! Expected a 404 status code, but got {response.status_code}")    # The server has not found a resource matching the request URI.

""" Test 18: HEAD /categories/:id/todos - headers for the todo items related to category, with given id, by the relationship named todos """
def test_head_categories_id_todos():
    category_payload = {
            "title": "title test 18 categories",
            "description": "description test 18 categories"
        }
    category_response = requests.post(BASE_URL + "/categories", json=category_payload)
    assert category_response.status_code == 201                                           # Succesfully created a category to get the id and then check its headers
    category_id = category_response.json()['id']

    response = requests.head(BASE_URL + f"/categories/{category_id}/todos")
    assert response.status_code == 200                                                    # The request has succeeded.                  
    assert not response.text                                                              # The response body is empty as should be for a HEAD request              
    assert "Content-Type" in response.headers                                             # The response contains a key named "Content-Type"       
    assert response.headers['Content-Type'] == 'application/json'                         # The response Content-Type is application/json 

""" Test 19: POST /categories/:id/todos - create a new todo item related to category, with given id, by the relationship named todos """
def test_post_categories_id_todos():
    category_payload = {
            "title": "title test 19 categories",
            "description": "description test 19 categories"
        }
    todo_payload = {
            "title": "title test 19 todos",
            "doneStatus": False
        }
    category_response = requests.post(BASE_URL + "/categories", json=category_payload)
    assert category_response.status_code == 201                                             # Succesfully created a category to get the id and then create a todo related to it
    category_id = category_response.json()['id']

    response = requests.post(BASE_URL + f"/categories/{category_id}/todos", json=todo_payload)
    assert response.status_code == 201                                                      # Succesfully created a todo related to the category             
    assert response.json()['title'] == todo_payload['title']                                # The response contains the title of the new todo
    assert response.json()['doneStatus'] == "false"                                         # The response contains the doneStatus of the new todo

# TESTING https://localhost:4567/categories/:id/todos/:id

""" Test 20: DELETE /categories/:id/todos/:id - delete a specific todo item related to category, with given id, by the relationship named todos """
def test_delete_categories_id_todos_id():
    category_payload = {
            "title": "title test 20 categories",
            "description": "description test 20 categories"
        }
    todo_payload = {
            "title": "title test 20 todos",
            "doneStatus": False
        }
    category_response = requests.post(BASE_URL + "/categories", json=category_payload)
    assert category_response.status_code == 201                                             # Succesfully created a category to get the id and then create a relationship with a todo and then delete
    category_id = category_response.json()['id']

    todo_response = requests.post(BASE_URL + "/todos", json=todo_payload)
    assert todo_response.status_code == 201                                                 # Succesfully created a todo to get the id and then create a relationship with a category and then delete     
    todo_id = todo_response.json()['id']

    relationship_payload = {"id": todo_id}
    relationship_response = requests.post(BASE_URL + f"/categories/{category_id}/todos",json=relationship_payload)
    assert relationship_response.status_code == 201                                         # Succesfully created a relationship between the category and todo

    response = requests.delete(BASE_URL + f"/categories/{category_id}/todos/{todo_id}")
    assert response.status_code                                                             # Succesfully deleted the relationship between the category and todo

# TESTING https://localhost:4567/categories/ with xml

""" Test 21: POST /categories - create a new category with xml format """
def test_post_categories_xml():
    payload = """
        <category>
            <title>test xml</title>
            <description>test 21 categories xml</description>
        </category>
    """
    headers = {'Content-Type': 'application/xml'}
    response = requests.post(BASE_URL + "/categories", data=payload, headers=headers)
    assert response.status_code == 201                                                      # The request has been fulfilled and has resulted in new resources being created.
    assert response.json()['title'] == "test xml"

""" Test 22: GET /categories - return all the instances of categories with xml format """
def test_get_categories_xml():
    headers = {'Accept': 'application/xml'}
    response = requests.get(BASE_URL + "/categories", headers=headers)
    assert response.status_code == 200                                                      # The request has succeeded.
    assert "categories" in response.text                                                    # The response contains a key named "categories"

""" Test 23: HEAD /categories - return the headers of the response with xml format """
def test_head_categories_xml():
    headers = {'Accept': 'application/xml'}
    response = requests.head(BASE_URL + "/categories", headers=headers)
    assert response.status_code == 200                                                      # The request has succeeded.
    assert not response.text                                                                # The response body is empty as should be for a HEAD request
    assert "Content-Type" in response.headers                                               # The response contains a key named "Content-Type"
    assert response.headers['Content-Type'] == 'application/xml'                            # The response Content-Type is application/xml

""" Test 24: POST /cateoriees - no title, should cause error """
def test_post_categories_no_title_xml():
    payload = """
        <category>
            <description>test 24 categories xml</description>
        </category>
    """
    response = requests.post(BASE_URL + "/categories", json=payload)
    assert response.status_code == 400                                                      # The server could not understand the request due to invalid syntax.
