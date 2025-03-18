from behave import given, when, then
import requests

BASE_URL = "http://localhost:4567/todos"

# --------------------- Normal Flow ---------------------
@given('there are tasks with different "doneStatus" values')
def step_impl(context):
    """
    Create tasks with varying doneStatus values (True, False).
    """
    tasks = [
        {"title": "Task 1", "description": "Do something", "doneStatus": True},
        {"title": "Task 2", "description": "Do something else", "doneStatus": False},
        {"title": "Task 3", "description": "Do more work", "doneStatus": True},
    ]
    for task in tasks:
        response = requests.post(BASE_URL, json=task)
        assert response.status_code == 201, f"Failed to create task: {response.status_code}"

@when('I send a GET request to "/todos?doneStatus=<doneStatus>"')
def step_impl(context, doneStatus):
    """
    Send a GET request to filter tasks by the specified doneStatus.
    """
    url = f"{BASE_URL}?doneStatus={doneStatus}"
    context.response = requests.get(url)

@then('I should receive a status code of 200')
def step_impl(context):
    """
    Assert that the response status code is 200.
    """
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"

@then('the response should only contain tasks with doneStatus "<doneStatus>"')
def step_impl(context, doneStatus):
    """
    Assert that the response contains only tasks with the specified doneStatus.
    """
    tasks = context.response.json()
    for task in tasks:
        assert task["doneStatus"] == (doneStatus == "True"), \
            f"Expected task with doneStatus {doneStatus}, but got {task['doneStatus']}"

# --------------------- Alternative Flow ---------------------
@given('there are tasks in the system')
def step_impl(context):
    """
    Ensure that tasks are present in the system for the alternative flow.
    """
    tasks = [
        {"title": "Sample Task 1", "description": "Description 1", "doneStatus": False},
        {"title": "Sample Task 2", "description": "Description 2", "doneStatus": True},
    ]
    for task in tasks:
        response = requests.post(BASE_URL, json=task)
        assert response.status_code == 201, f"Failed to create task: {response.status_code}"

# --------------------- Error Flow ---------------------
@when('I send a GET request to "/todos?doneStatus=<invalid_doneStatus>"')
def step_impl(context, invalid_doneStatus):
    """
    Send a GET request with an invalid doneStatus value.
    """
    url = f"{BASE_URL}?doneStatus={invalid_doneStatus}"
    context.response = requests.get(url)

@then('I should receive a status code of 400')
def step_impl(context):
    """
    Assert that the response status code is 400 for invalid doneStatus.
    """
    assert context.response.status_code == 400, f"Expected 400, got {context.response.status_code}"

@then('the response should indicate a bad request error')
def step_impl(context):
    """
    Assert that the response contains a bad request error.
    """
    response_json = context.response.json()
    assert 'error' in response_json, "Expected error in response, but got: " + str(response_json)
    assert response_json['error'] == "Bad Request", f"Expected 'Bad Request', got: {response_json['error']}"
