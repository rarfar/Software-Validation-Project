import requests
from behave import given, when, then

BASE_URL = "http://localhost:4567/todos"

# --------------------- Background ---------------------
@given("the /todo system is running")
def step_impl(context):
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"API is not running. Status: {response.status_code}, Response: {response.text}"

# --------------------- Normal Flow ---------------------
@given('there is no existing todo item with title "{task_title}", description "{task_description}" and doneStatus "{task_doneStatus}"')
def step_impl(context, task_title, task_description, task_doneStatus):
    response = requests.get(BASE_URL)
    todos = response.json().get("todos", [])
    for todo in todos:
        assert not (todo["title"] == task_title and todo.get("description", "") == task_description and
                    todo["doneStatus"].lower() == task_doneStatus.lower()), f"Todo already exists: {todo}"

@when('I create a todo with title "{task_title}" and description "{task_description}"')
def step_impl(context, task_title, task_description):
    payload = {
        "title": task_title,
        "description": task_description
    }
    context.response = requests.post(BASE_URL, json=payload)
    assert context.response.status_code in [200, 201], f"Failed to create todo: {context.response.text}"

@then('the todo should be saved in the system with doneStatus "False"')
def step_impl(context):
    created_todo = context.response.json()
    assert "title" in created_todo, f"Title missing in response: {context.response.text}"
    assert created_todo["doneStatus"].lower() == "false", f"Incorrect doneStatus: {created_todo}"

# --------------------- Alternative Flow ---------------------
@when('I create a todo with title "{task_title}", no description and no doneStatus')
def step_impl(context, task_title):
    payload = {
        "title": task_title
    }
    context.response = requests.post(BASE_URL, json=payload)
    assert context.response.status_code in [200, 201], f"Failed to create todo: {context.response.text}"

@then('the todo should be saved with an empty description and doneStatus "False"')
def step_impl(context):
    created_todo = context.response.json()
    assert "title" in created_todo, f"Title missing in response: {context.response.text}"
    assert created_todo.get("description", "") == "", f"Description is not empty: {created_todo}"
    assert created_todo["doneStatus"].lower() == "false", f"Incorrect doneStatus: {created_todo}"

# --------------------- Error Flow ---------------------
@when('I attempt to add a task without a title and only provide a description "{task_description}"')
def step_impl(context, task_description):
    payload = {
        "description": task_description
    }
    context.response = requests.post(BASE_URL, json=payload)

@then('I should receive an error response: status code 400')
def step_impl(context):
    assert context.response.status_code == 400, f"Expected 400, got {context.response.status_code}: {context.response.text}"
