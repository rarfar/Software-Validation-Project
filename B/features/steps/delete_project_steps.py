import requests
from behave import given, when, then

BASE_URL = "http://localhost:4567/projects"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# --------------------- Background ---------------------
# Reusing existing step definition from create_project_steps.py
# @given("the /projects system is running")
def step_impl(context):
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"API is not running. Status: {response.status_code}, Response: {response.text}"

# --------------------- Normal Flow ---------------------
@given("a project exists with title \"{project_title}\"")
def step_impl(context, project_title):
    payload = {"title": project_title, "completed": False, "active": True}
    response = requests.post(BASE_URL, headers=HEADERS, json=payload)
    assert response.status_code == 201, f"Failed to create project {project_title}, Status: {response.status_code}"
    context.project_id = response.json()["id"]

@when("I delete the project with title \"{project_title}\"")
def step_impl(context, project_title):
    response = requests.delete(f"{BASE_URL}/{context.project_id}", headers=HEADERS)
    context.response = response
    print(f"Response: {context.response.status_code}, {context.response.text}")

@then("the project should no longer exist")
def step_impl(context):
    response = requests.get(f"{BASE_URL}/{context.project_id}", headers=HEADERS)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}. Response: {response.text}"

# --------------------- Alternative Flow ---------------------
@when("I attempt to delete the same project again")
def step_impl(context):
    response = requests.delete(f"{BASE_URL}/{context.project_id}", headers=HEADERS)
    context.response = response
    print(f"Response: {context.response.status_code}, {context.response.text}")

# --------------------- Error Flow ---------------------
@when("I attempt to delete a non-existent project")
def step_impl(context):
    context.response = requests.delete(f"{BASE_URL}/999999", headers=HEADERS)
    print(f"Response: {context.response.status_code}, {context.response.text}")

@then("I should receive a 404 error when deleting a project")
def step_impl(context):
    assert context.response.status_code == 404, f"Expected 404, got {context.response_status_code}. Response: {context.response.text}"
