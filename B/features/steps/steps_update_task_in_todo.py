from behave import *  # Import all necessary decorators and functions from behave
import requests  # For making HTTP requests
from helpers import *  # Import helper variables and functions (e.g., headers, URLs)


@given('a todo exists with ID "{task_id}" and title "{task_title}", description "{task_description}", and doneStatus "{task_doneStatus}"')
def step_impl(context, task_id, task_title, task_description, task_doneStatus):
    json_payload = json.dumps({
        "title": task_title,
        "description": task_description,
        "doneStatus": task_doneStatus
    })
    response = requests.post(url_todos,headers=json_to_json,data=json_payload)
    assert response.status_code in [200, 201], f"Expected status code 201 or 200, but got {response.status_code}"
    # Extract the assigned task ID from the response
    response_data = response.json()
    task_id = response_data.get("id")

    # Save task details in the context for use in later steps
    context.task_id = task_id
    context.task_title = task_title
    context.task_description = task_description
    context.task_doneStatus = task_doneStatus
    context.response = response


@when('I update the doneStatus of the todo with ID "{task_id}" to "True"')
def step_impl(context, task_id):
    payload = json.dumps({
        "doneStatus": "True"
    })
    response = requests.put(url_todos_id % context.task_id, headers=json_to_json,data=json_payload)
    assert response.status_code in [200, 201], f"Expected status code 201 or 200, but got {response.status_code}"


@then('the todo should be updated with doneStatus "True"')
def step_impl(context):
    response = requests.get(url_todos_id % context.task_id)
    response_data = response.json()
    task_status = response_data.get("doneStatus")
    assert task_status in ["True"]

#Alternative Flow

#given implemented above
@when('I update the doneStatus of the todo with ID "{task_id}" to "False"')
def step_impl(context, task_id):
     payload = json.dumps({
        "doneStatus": "False"
    })
    response = requests.put(url_todos_id % context.task_id, headers=json_to_json,data=json_payload)
    assert response.status_code in [200, 201], f"Expected status code 201 or 200, but got {response.status_code}"
    response_data = response.json()
    task_status = response_data.get("doneStatus")
    assert task_status in ["True"]