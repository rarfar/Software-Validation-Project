from behave import given, when, then
import requests

BASE_URL = "http://localhost:4567"

@given('there are existing projects in the system')
def step_impl(context):
    """Ensure that at least one project exists in the system"""
    response = requests.get(f"{BASE_URL}/projects")
    projects = response.json().get("projects", [])

    if not projects:
        # Create a default project
        payload = {"title": "Sample Project", "description": "Default project"}
        response = requests.post(f"{BASE_URL}/projects", json=payload)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

@given('there are no projects in the system')
def step_impl(context):
    """Ensure that no projects exist in the system"""
    response = requests.get(f"{BASE_URL}/projects")
    projects = response.json().get("projects", [])

    # Delete all existing projects
    for project in projects:
        requests.delete(f"{BASE_URL}/projects/{project['id']}")

    # Verify deletion
    response = requests.get(f"{BASE_URL}/projects")
    projects = response.json().get("projects", [])
    assert len(projects) == 0, "Projects still exist in the system"

@when('I request a list of all projects')
def step_impl(context):
    """Send a GET request to retrieve all projects"""
    context.response = requests.get(f"{BASE_URL}/projects")

@when('I send a GET request to an invalid endpoint "/invalid_projects"')
def step_impl(context):
    """Send a GET request to an invalid endpoint"""
    context.response = requests.get(f"{BASE_URL}/invalid_projects")

@then('I should receive a response containing all projects')
def step_impl(context):
    """Ensure that the response contains a list of projects"""
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"
    projects = context.response.json().get("projects", [])
    assert isinstance(projects, list) and len(projects) > 0, "No projects found in the response"

@then('I should receive an empty list of projects')
def step_impl(context):
    """Ensure that the response contains an empty list"""
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"
    projects = context.response.json().get("projects", [])
    assert projects == [], "Expected an empty list of projects"