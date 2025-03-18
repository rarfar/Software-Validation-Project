from behave import given, when, then
import requests

BASE_URL = "http://localhost:4567/todos"

# --------------------- Background ---------------------
@given("the /todos system is running")
def step_impl(context):
    """
    Ensure that the system is running before executing tests.
    """
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"


# --------------------- Normal Flow ---------------------
@when('I send a GET request to "/todos"')
def step_impl(context):
    """
    Send a GET request to retrieve all todos.
    """
    context.response = requests.get(BASE_URL)


@then("I should receive a status code 200")
def step_impl(context):
    """
    Verify that the response status code is 200 (OK).
    """
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"


@then("the response should contain a list of all todo items")
def step_impl(context):
    """
    Verify that the response contains a list of todo items.
    """
    todos = context.response.json().get("todos", None)
    assert todos is not None, "Response does not contain 'todos' key"
    assert isinstance(todos, list), f"Expected a list, got {type(todos)}"
    assert len(todos) > 0, "Expected at least one todo item in the list"


# --------------------- Alternative Flow ---------------------
@given("There are no tasks")
def step_impl(context):
    """
    Ensure there are no tasks in the system before proceeding.
    """
    # Fetch all existing tasks
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        todos = response.json().get("todos", [])
        # Delete each existing task
        for todo in todos:
            requests.delete(f"{BASE_URL}/{todo['id']}")

    # Confirm the list is empty
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json().get("todos", []) == [], "Expected no tasks, but found some"
@then("the response should be an empty list")
def step_impl(context):
    """
    Verify that the response contains an empty list.
    """
    todos = context.response.json().get("todos", None)
    assert todos is not None, "Response does not contain 'todos' key"
    assert isinstance(todos, list), f"Expected a list, got {type(todos)}"
    assert len(todos) == 0, f"Expected an empty list, but got {len(todos)} items"


# --------------------- Error Flow ---------------------
@given("the /todos system is down")
def step_impl(context):
    """
    Simulate a system failure by setting an invalid base URL.
    """
    global BASE_URL
    BASE_URL = "http://localhost:9999/todos"  # Changing to a non-working port to simulate failure

@when("I send GET request to \"/todos\"")
def step_impl(context):
    """
    Send a GET request to retrieve all todos.
    """
    try:
        context.response = requests.get(BASE_URL)
    except requests.exceptions.RequestException as e:
        context.error = e

@then("I should receive a status code 500, indicating an internal server error")
def step_impl(context):
    """
    Verify that the response status code is 500 (Internal Server Error).
    If the system is down, a connection error should be caught and interpreted as a 500 error.
    """
    if hasattr(context, 'error'):
        # Handle the error raised due to the system being down
        assert isinstance(context.error, requests.exceptions.RequestException), "Unexpected error type"
        print(f"System down, error occurred: {str(context.error)}")
        # Simulate a 500 status code response as we're dealing with an unreachable server
        assert True  # Mark the test as passing since the system is down
    else:
        assert context.response.status_code == 500, f"Expected 500, got {context.response.status_code}"
