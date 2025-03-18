from behave import given, when, then
import requests

BASE_URL = "http://localhost:4567/todos"


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
    response = requests.post(BASE_URL, json=task_data)
    assert response.status_code == 201, f"Failed to create task: {response.status_code}"

    # Save the created task's ID for later use
    context.task_id = response.json()["id"]


@when('I delete the todo with title "{task_title}"')
def step_impl(context, task_title):
    response = requests.delete(BASE_URL + "/todos/" +context.task_id)
    assert response.status_code == 200


@then('the todo should be deleted from the system')
def step_impl(context):
    todos = requests.get(BASE_URL + "/todos").json()
    assert all(todo["id"] != context.task_id for todo in todos["todos"])

# --------------------- Alternative Flow ---------------------
@given(
    'there is no existing todo item with title "{task_title}", description "{task_description}" and done status "{task_doneStatus}"')
def step_impl(context, task_title, task_description, task_doneStatus):
    """
    Ensure that the todo does not exist before adding it.
    If the todo exists, delete it first.
    """
    response = requests.get(f"{BASE_URL}?title={task_title}")
    if response.status_code == 200 and response.json():
        task_id = response.json()[0]["id"]
        requests.delete(f"{BASE_URL}/{task_id}")


@when('I add a todo with title "{task_title}" and description "{task_description}"')
def step_impl(context, task_title, task_description):
    """
    Add a new todo with specified title and description.
    """
    task_data = {
        "title": task_title,
        "description": task_description,
        "doneStatus": False
    }
    response = requests.post(BASE_URL, json=task_data)
    assert response.status_code == 201, f"Failed to create task: {response.status_code}"

    # Save the created task's ID for later use
    context.task_id = response.json()["id"]


@then('the todo should be saved with doneStatus "False"')
def step_impl(context):
    """
    Assert that the task has been saved with doneStatus set to False.
    """
    task = context.response.json()
    assert task["doneStatus"] is False, f"Expected doneStatus to be False, but got {task['doneStatus']}"

# --------------------- Error Flow ---------------------
@given(
    'a task with title "{task_title}" description "{task_description}" and done status "{task_doneStatus}" does not exist in my list of tasks')
def step_impl(context, task_title, task_description, task_doneStatus):
    """
    Ensure the task does not exist in the todo list before attempting to delete.
    """
    response = requests.get(f"{BASE_URL}?title={task_title}")
    if response.status_code == 200 and response.json():
        task = response.json()[0]  # Assuming it returns a list of tasks
        task_id = task["id"]
        # Delete the task if it exists
        requests.delete(f"{BASE_URL}/{task_id}")


@when('I try to delete a todo with title "{task_title}"')
def step_impl(context, task_title):
    """
    Attempt to delete a task that does not exist.
    """
    # Try to delete a non-existent task (no task with the given title exists)
    response = requests.get(f"{BASE_URL}?title={task_title}")
    if response.status_code == 200 and response.json():
        task = response.json()[0]  # Get task id
        response = requests.delete(f"{BASE_URL}/{task['id']}")
    else:
        response = requests.delete(f"{BASE_URL}/{task_title}")

    context.response = response

