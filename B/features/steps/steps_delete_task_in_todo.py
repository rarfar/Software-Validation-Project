from behave import given, when, then
import requests

BASE_URL = "http://localhost:4567/todos"



# --------------------- Normal Flow ---------------------
@given('a todo exists with title "{task_title}", description "{task_description}" and done status "{task_doneStatus}"')
def step_impl(context, task_title, task_description, task_doneStatus):
    payload = {
        "title": task_title,
        "description": task_description,
        "doneStatus": task_doneStatus
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code in [200, 201], f"Todo creation failed: {response.text}"
    context.todo_id = response.json()["id"]


@when('I delete the todo with title "{task_title}"')
def step_impl(context, task_title):
    # Get all todos and find the one with the matching title
    response = requests.get(BASE_URL)
    todos = response.json().get("todos", [])

    todo_id = None
    for todo in todos:
        if todo["title"] == task_title:
            todo_id = todo["id"]
            break

    assert todo_id, f"No todo found with title: {task_title}"

    # Delete the found todo
    context.response = requests.delete(f"{BASE_URL}/{todo_id}")


@then("the todo should be deleted from the system")
def step_impl(context):
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"
    deleted_todo_id = context.response.url.split("/")[-1]

    # Verify it no longer exists
    response = requests.get(f"{BASE_URL}/{deleted_todo_id}")
    assert response.status_code == 404, "Todo was not deleted successfully"


# --------------------- Alternative Flow ---------------------
@given(
    'there is no existing todo item with title "{task_title}", description "{task_description}" and done status "{task_doneStatus}"')
def step_impl(context, task_title, task_description, task_doneStatus):
    response = requests.get(BASE_URL)
    todos = response.json().get("todos", [])

    for todo in todos:
        assert not (todo["title"] == task_title and todo.get("description", "") == task_description and todo[
            "doneStatus"] == task_doneStatus), \
            f"Todo with title '{task_title}' already exists!"


@when('I add a todo with title "{task_title}" and description "{task_description}"')
def step_impl(context, task_title, task_description):
    payload = {
        "title": task_title,
        "description": task_description
    }
    context.response = requests.post(BASE_URL, json=payload)
    assert context.response.status_code in [200, 201], f"Expected 200/201, got {context.response.status_code}"
    context.todo_id = context.response.json()["id"]


@then('the todo should be saved with doneStatus "False"')
def step_impl(context):
    assert context.response.status_code in [200, 201]
    created_todo = context.response.json()
    assert created_todo["title"]
    assert created_todo["doneStatus"] == "false"


# --------------------- Error Flow ---------------------
@given(
    'a task with title "{task_title}" description "{task_description}" and done status "{task_doneStatus}" does not exist in my list of tasks')
def step_impl(context, task_title, task_description, task_doneStatus):
    response = requests.get(BASE_URL)
    todos = response.json().get("todos", [])

    for todo in todos:
        assert not (todo["title"] == task_title and todo.get("description", "") == task_description and todo[
            "doneStatus"] == task_doneStatus), \
            f"Todo '{task_title}' unexpectedly found!"


@when('I try to delete a todo with title "{task_title}"')
def step_impl(context, task_title):
    # Try to find the todo ID
    response = requests.get(BASE_URL)
    todos = response.json().get("todos", [])

    todo_id = None
    for todo in todos:
        if todo["title"] == task_title:
            todo_id = todo["id"]
            break

    # If not found, use a random ID to trigger 404
    todo_id = todo_id or "999999"

    context.response = requests.delete(f"{BASE_URL}/{todo_id}")


