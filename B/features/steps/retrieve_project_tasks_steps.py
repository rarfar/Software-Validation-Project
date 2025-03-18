from behave import given, when, then
import requests

BASE_URL = "http://localhost:4567"

@given('a project in the system exists with title "{project_title}"')
def step_impl(context, project_title):
    """Ensure a project with the given title exists"""
    response = requests.get(f"{BASE_URL}/projects")
    projects = response.json().get("projects", [])

    for project in projects:
        if project["title"] == project_title:
            context.project_id = project["id"]
            return

    # Create the project if it does not exist
    payload = {"title": project_title}
    response = requests.post(f"{BASE_URL}/projects", json=payload)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    context.project_id = response.json()["id"]

@given('the project has tasks "{task1}" and "{task2}"')
def step_impl(context, task1, task2):
    """Ensure the project has the specified tasks"""
    context.task1 = task1
    context.task2 = task2

    for task in [task1, task2]:
        payload = {"title": task}
        response = requests.post(f"{BASE_URL}/todos", json=payload)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        task_id = response.json()["id"]

        # Link the task to the project
        response = requests.post(f"{BASE_URL}/projects/{context.project_id}/tasks", json={"id": task_id})
        assert response.status_code in [200, 201], f"Failed to link task {task} to project"

@given('the project has no tasks')
def step_impl(context):
    """Ensure the project has no tasks"""
    response = requests.get(f"{BASE_URL}/projects/{context.project_id}/tasks")
    tasks = response.json().get("todos", [])

    # Remove any existing tasks
    for task in tasks:
        requests.delete(f"{BASE_URL}/projects/{context.project_id}/tasks/{task['id']}")

@when('I request all tasks for the project')
def step_impl(context):
    """Send a GET request to retrieve tasks for the project"""
    context.response = requests.get(f"{BASE_URL}/projects/{context.project_id}/tasks")

@when('I request tasks for a non-existent project')
def step_impl(context):
    """Send a GET request for a non-existent project"""
    context.response = requests.get(f"{BASE_URL}/projects/999999/tasks")

@then('I should receive a list containing the tasks "{task1}" and "{task2}"')
def step_impl(context, task1, task2):
    """Ensure that the response contains the specified tasks"""
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"
    tasks = context.response.json().get("todos", [])
    task_titles = {t["title"] for t in tasks}
    assert task1 in task_titles and task2 in task_titles, "Both tasks not found in response"

@then('I should receive an empty task list')
def step_impl(context):
    """Ensure that the response contains an empty list"""
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"
    tasks = context.response.json().get("todos", [])
    assert tasks == [], "Expected an empty list of tasks"

@then('I should receive a response (even if the project does not exist)')
def step_impl(context):
    """Ensure that the response contains tasks, even if the project is missing"""
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"
    tasks = context.response.json().get("todos", [])
    assert isinstance(tasks, list), f"Expected a list, but got {type(tasks)}"
