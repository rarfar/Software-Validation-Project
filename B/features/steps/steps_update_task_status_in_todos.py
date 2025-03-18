from behave import given, when, then
import requests

BASE_URL = "http://localhost:4567/todos"


# --------------------- Normal Flow ---------------------
@given('a todo exists with title "{task_title}", description "{task_description}" and doneStatus "{task_doneStatus}"')
def step_impl(context, task_title, task_description, task_doneStatus):
    """
    Ensure the todo exists with a specified title, description, and doneStatus.
    """
    task_data = {
        "title": task_title,
        "description": task_description,
        "doneStatus": task_doneStatus == "True"
    }
    response = requests.post(BASE_URL, json=task_data)
    assert response.status_code == 201, f"Failed to create task: {response.status_code}"

@when('I update the doneStatus of "{task_title}" to "True"')
def step_impl(context, task_title):
    """
    Update the doneStatus of a given task to True.
    """
    response = requests.put(f"{BASE_URL}/{task_title}", json={"doneStatus": True})
    context.response = response

@then('the todo should be saved with doneStatus "True"')
def step_impl(context):
    """
    Assert that the task's doneStatus is True after updating.
    """
    task = context.response.json()
    assert task["doneStatus"] is True, f"Expected doneStatus to be True, but got {task['doneStatus']}"

# --------------------- Alternative Flow ---------------------
@when('I update the doneStatus of "{task_title}" to "False"')
def step_impl(context, task_title):
    """
    Update the doneStatus of a given task to False.
    """
    response = requests.put(f"{BASE_URL}/{task_title}", json={"doneStatus": False})
    context.response = response


# --------------------- Error Flow ---------------------
@when('I try to update the doneStatus of a non-existent task with name "{task_title}"')
def step_impl(context, task_title):
    """
    Attempt to update the doneStatus of a non-existent task.
    """
    response = requests.put(f"{BASE_URL}/{task_title}", json={"doneStatus": False})
    context.response = response


