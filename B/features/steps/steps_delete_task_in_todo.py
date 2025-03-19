from behave import given, when, then
import requests

BASE_URL = "http://localhost:4567/todos"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# --------------------- Normal Flow ---------------------
@given('a todo exists with title "{task_title}", description "{task_description}" and done status "{task_doneStatus}"')
def step_impl(context, task_title, task_description, task_doneStatus):
    """
    Ensure the todo exists with a specified title, description, and doneStatus.
    First, we query to get the ID based on the title.
    """
    task_data = {
        "title": task_title,
        "description": task_description,
        "doneStatus": task_doneStatus == "True"
    }
    response = requests.post(BASE_URL, headers=HEADERS, json=task_data)
    assert response.status_code == 201, f"Failed to create task: {response.status_code}"

    # Save the created task's ID for later use
    context.task_id = response.json()["id"]


@when('I delete the todo with title "{task_title}"')
def step_impl(context, task_title):
    response = requests.delete(f"{BASE_URL}/{context.task_id}", headers=HEADERS)
    context.reponse = response
    assert response.status_code == 200


@then('the todo should be deleted from the system')
def step_impl(context):
    response = requests.get(f"{BASE_URL}/{context.project_id}", headers=HEADERS)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}. Response: {response.text}"

# --------------------- Alternative Flow ---------------------
@given('there is no existing todo item with title "{task_title}", description "{task_description}" and done status "{task_doneStatus}"')
def step_impl(context, task_title, task_description, task_doneStatus):
    response = requests.get(BASE_URL)
    todos = response.json().get("todos", [])
    for todo in todos:
        assert not (todo["title"] == task_title and todo.get("description", "") == task_description and
                    todo["doneStatus"].lower() == task_doneStatus.lower()), f"Todo already exists: {todo}"


@when('I add a todo with title "{task_title}" and description "{task_description}"')
def step_impl(context, task_title, task_description):
    payload = {
        "title": task_title,
        "description": task_description
    }
    context.response = requests.post(BASE_URL, json=payload)
    assert context.response.status_code in [200, 201], f"Failed to create todo: {context.response.text}"


@then('the todo should be saved with doneStatus "False"')
def step_impl(context):
    created_todo = context.response.json()
    assert "title" in created_todo, f"Title missing in response: {context.response.text}"
    assert created_todo["doneStatus"].lower() == "false", f"Incorrect doneStatus: {created_todo}"

# --------------------- Error Flow ---------------------

@when('I send a DELETE request to "/todos/1111"')
def step_impl(context):
    context.response = requests.delete(f"{BASE_URL}/999999", headers=HEADERS)
    print(f"Response: {context.response.status_code}, {context.response.text}")

@then("I should receive an 404 error when deleting a project")
def step_impl(context):
    assert context.response.status_code == 404, f"Expected 404, got {context.response_status_code}. Response: {context.response.text}"
