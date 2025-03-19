from behave import *  # Import all necessary decorators and functions from behave
import requests  # For making HTTP requests
from helpers import *  # Import helper variables and functions (e.g., headers, URLs)

BASE_URL = "http://localhost:4567/todos"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

@given('a todo exists with ID "{task_id}" and title "{task_title}", description "{task_description}", and doneStatus "{task_doneStatus}"')
def step_impl(context, task_id, task_title, task_description, task_doneStatus):
    task_data = {
        "title": task_title,
        "description": task_description,
        "doneStatus": task_doneStatus == "False"
    }
    response = requests.post(BASE_URL, headers=HEADERS, json=task_data)
    assert response.status_code == 201, f"Failed to create task: {response.status_code}"

    # Save the created task's ID for later use
    context.task_id = response.json()["id"]


@when('I update the doneStatus of the todo with ID "{task_id}" to "True"')
def step_impl(context, task_id):
    payload ={
        "doneStatus": "True"
    }
    response = requests.put(f"{BASE_URL}/{context.task_id}", headers=HEADERS, json=payload)
    assert response.status_code in [200, 201], f"Expected status code 201 or 200, but got {response.status_code}"
    context.response = response

@then('the todo should be updated with doneStatus "True"')
def step_impl(context):

    response_data = context.response.json()
    task_status = response_data.get("doneStatus")
    assert task_status in ["True"]

#Alternative Flow

@given(
    'a todo exists with an ID "{task_id}" and title "{task_title}", description "{task_description}", and doneStatus "{task_doneStatus}"')
def step_impl(context, task_id, task_title, task_description, task_doneStatus):
    task_data = {
        "title": task_title,
        "description": task_description,
        "doneStatus": task_doneStatus == "False"
    }
    response = requests.post(BASE_URL, headers=HEADERS, json=task_data)
    assert response.status_code == 201, f"Failed to create task: {response.status_code}"

    # Save the created task's ID for later use
    context.task_id = response.json()["id"]


@when('I update the title of the todo with ID "{task_id}" to "{task_title}"')
def step_impl(context, task_id, task_title):
    payload = {
        "title":"New HW"
    }
    response = requests.put(f"{BASE_URL}/{context.task_id}", headers=HEADERS, json=payload)
    assert response.status_code in [200, 201], f"Expected status code 201 or 200, but got {response.status_code}"
    context.response = response


@then('the todo should be updated with description "{task_description}"')
def step_impl(context, task_description):
    response_data = context.response.json()
    task_tit= response_data.get("title")
    assert task_tit in ["New HW"]


# --------------------- Error Flow ---------------------

@given('there is no todo with ID "{task_id}"')
def step_impl(context, task_id):
   response = requests.get(f"{BASE_URL}/{task_id}")
   assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"

@when('I attempt to update the doneStatus of the todo with ID "{task_id}"')
def step_impl(context, task_id):
    payload = {
        "doneStatus": "True"
    }
    response = requests.put(f"{BASE_URL}/{task_id}", headers=HEADERS, json=payload)
    assert response.status_code == 404