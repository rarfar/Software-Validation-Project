import requests
from behave import given, when, then

BASE_URL = "http://localhost:4567/projects"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# --------------------- Background ---------------------
@given("the /projects system is running")
def step_impl(context):
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"API is not running. Status: {response.status_code}, Response: {response.text}"

# --------------------- Normal Flow ---------------------
@given("there is no existing project with title \"{project_title}\" and with description \"{project_description}\"")
def step_impl(context, project_title, project_description):
    response = requests.get(BASE_URL)
    projects = response.json().get("projects", [])
    for project in projects:
        if project["title"] == project_title and project["description"] == project_description:
            requests.delete(f"{BASE_URL}/{project['id']}", headers=HEADERS)  # Delete existing project

@when("I create a project with title \"{project_title}\" and with description \"{project_description}\"")
def step_impl(context, project_title, project_description):
    payload = {"title": project_title, "description": project_description, "completed": False, "active": True}
    context.response = requests.post(BASE_URL, headers=HEADERS, json=payload)
    print(f"Request Payload: {payload}")
    print(f"Response: {context.response.status_code}, {context.response.text}")

@then("the project with title \"{project_title}\" and description \"{project_description}\" should be saved in the system")
def step_impl(context, project_title, project_description):
    assert context.response.status_code == 201, f"Expected 201, got {context.response.status_code}. Response: {context.response.text}"
    response_json = context.response.json()
    assert response_json.get("title") == project_title, "Project title mismatch"
    assert response_json.get("description") == project_description, "Project description mismatch"

# --------------------- Alternative Flow ---------------------
@given("there is no existing project with title \"{project_title}\"")
def step_impl(context, project_title):
    response = requests.get(BASE_URL)
    projects = response.json().get("projects", [])
    for project in projects:
        if project["title"] == project_title:
            requests.delete(f"{BASE_URL}/{project['id']}", headers=HEADERS)

@when("I create a project with title \"{project_title}\" but with no description")
def step_impl(context, project_title):
    payload = {"title": project_title, "completed": False, "active": True}
    context.response = requests.post(BASE_URL, headers=HEADERS, json=payload)
    print(f"Request Payload: {payload}")
    print(f"Response: {context.response.status_code}, {context.response.text}")

@then("the project with title \"{project_title}\" should still be created successfully")
def step_impl(context, project_title):
    assert context.response.status_code == 201, f"Expected 201, got {context.response.status_code}. Response: {context.response.text}"
    response_json = context.response.json()
    assert response_json.get("title") == project_title, "Project title mismatch"
    assert "id" in response_json, "Expected project ID in response"

# --------------------- Error Flow ---------------------
@when("I attempt to add a project without a title")
def step_impl(context):
    payload = {"description": "Project without a title", "completed": False, "active": True}
    context.response = requests.post(BASE_URL, headers=HEADERS, json=payload)
    print(f"Request Payload: {payload}")
    print(f"Response: {context.response.status_code}, {context.response.text}")

@then("the project should be created with an empty title")
def step_impl(context):
    assert context.response.status_code == 201, f"Expected 201, got {context.response.status_code}. Response: {context.response.text}"
    response_json = context.response.json()
    assert response_json.get("title", "") == "", f"Expected empty title, got {response_json.get('title')}"