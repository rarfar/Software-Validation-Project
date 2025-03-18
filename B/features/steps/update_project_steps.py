import requests
from behave import given, when, then

BASE_URL = "http://localhost:4567/projects"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

@given("a project with title \"{project_title}\" exists")
def step_impl(context, project_title):
    payload = {"title": project_title, "completed": False, "active": True}
    response = requests.post(BASE_URL, headers=HEADERS, json=payload)
    assert response.status_code == 201, f"Failed to create project {project_title}, Status: {response.status_code}"
    
    if not hasattr(context, "project_ids"):
        context.project_ids = {}
    context.project_ids[project_title] = response.json()["id"]
    print(f"✅ Created project '{project_title}' with ID {context.project_ids[project_title]}")

@when("I update the project title from \"{old_title}\" to \"{new_title}\"")
def step_impl(context, old_title, new_title):
    project_id = context.project_ids.get(old_title)
    payload = {"title": new_title}
    response = requests.put(f"{BASE_URL}/{project_id}", headers=HEADERS, json=payload)
    context.response = response
    context.project_ids[new_title] = project_id
    print(f"Request Payload: {payload}")
    print(f"Response: {response.status_code}, {response.text}")

@when("I attempt to update a non-existent project")
def step_impl(context):
    payload = {"title": "Non-existent Project"}
    context.response = requests.put(f"{BASE_URL}/999999", headers=HEADERS, json=payload)
    print(f"Request Payload: {payload}")
    print(f"Response: {context.response.status_code}, {context.response.text}")

@then("the project title should be updated to \"{new_title}\"")
def step_impl(context, new_title):
    project_id = context.project_ids.get(new_title)
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}. Response: {context.response.text}"
    response_json = requests.get(f"{BASE_URL}/{project_id}", headers=HEADERS).json()
    if "projects" in response_json:
        project_data = response_json["projects"][0]
    else:
        project_data = response_json
    assert project_data.get("title") == new_title, f"Expected title '{new_title}', got '{project_data.get('title')}'"

@then("I should receive an error: status code {status_code}")
def step_impl(context, status_code):
    expected_status_code = int(status_code)
    assert context.response.status_code == expected_status_code, (
        f"Expected {expected_status_code}, got {context.response.status_code}. Response: {context.response.text}"
    )
