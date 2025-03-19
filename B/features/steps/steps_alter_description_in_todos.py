from behave import *  # Import all necessary decorators and functions from behave
import requests  # For making HTTP requests
from helpers import *  # Import helper variables and functions (e.g., headers, URLs)
import json

BASE_URL = "http://localhost:4567/todos"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


@given('a task exists with a title "{task_title}", description "{task_description}", and completion status "{task_doneStatus}"')
def step_impl(context, task_title, task_description, task_doneStatus):
    task_data = {
        "title": task_title,
        "description": task_description,
        "doneStatus": task_doneStatus.lower() == "true"
    }
    r = requests.post(BASE_URL, data=json.dumps(task_data), headers=HEADERS)
    assert r.status_code == 201
    context.task_id = r.json()["id"]
    context.task_title = task_title
    context.task_description = task_description
    context.task_doneStatus = task_doneStatus


@when('the description is changed to "{new_task_description}"')
def step_impl(context, new_task_description):
    task_update = {
        "title": context.task_title,
        "description": new_task_description
    }
    context.new_task_description = new_task_description
    response = requests.put(f"{BASE_URL}/{context.task_id}", data=json.dumps(task_update), headers=HEADERS)
    assert response.status_code == 200


@then("the task should reflect the updated description")
def step_impl(context):
    response = requests.get(f"{BASE_URL}/{context.task_id}", headers=HEADERS)
    todo = response.json()["todos"][0]
    assert response.status_code == 200 and str(context.new_task_description) == str(todo["description"])


@given('a task exists with a the title "{task_title}", description "{task_description}", and completion status "{task_doneStatus}"')
def step_impl(context, task_title, task_description, task_doneStatus):
    context.execute_steps(
        f'Given a task exists with a title "{task_title}", description "{task_description}", and completion status "{task_doneStatus}"')


@when("the description is cleared")
def step_impl(context):
    task_update = {
        "title": context.task_title,
        "description": ""
    }
    context.new_task_description = ""
    response = requests.put(f"{BASE_URL}/{context.task_id}", data=json.dumps(task_update), headers=HEADERS)
    assert response.status_code == 200


@then("the task should have an empty description")
def step_impl(context):
    response = requests.get(f"{BASE_URL}/{context.task_id}", headers=HEADERS)
    todo = response.json()["todos"][0]
    assert response.status_code == 200 and todo["description"] == ""


@given('no task exists with a title "{task_title}", description "{task_description}", and completion status "{task_doneStatus}"')
def step_impl(context, task_title, task_description, task_doneStatus):
    response = requests.get(BASE_URL, headers=HEADERS)
    tasks = response.json().get("todos", [])
    for task in tasks:
        assert not (task["title"] == task_title and task["description"] == task_description and str(
            task["doneStatus"]).lower() == task_doneStatus.lower())


@when('an attempt is made to update the description to "{new_task_description}" using the incorrect task ID "{wrong_task_id}"')
def step_impl(context, new_task_description, wrong_task_id):
    task_update = {
        "description": new_task_description
    }
    response = requests.put(f"{BASE_URL}/{wrong_task_id}", data=json.dumps(task_update), headers=HEADERS)
    context.response = response


@then("an error should indicate that the task was not found")
def step_impl(context):
    assert context.response.status_code == 404