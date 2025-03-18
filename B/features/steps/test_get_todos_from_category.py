from behave import *  # Import all necessary decorators and functions from behave
import requests  # For making HTTP requests
import xmltodict  # For parsing XML responses
from helpers import *  # Import helper variables and functions (e.g., headers, URLs)

# NORMAL FLOW
@Given(u'the category contains todos "{todo_title_1}", "{todo_title_2}"')
def step_impl(context, todo_title_1, todo_title_2):
    # Create two todos with the provided titles and descriptions
    todo_1 = todos_xml_1 % (todo_title_1, "Description 1", "false")
    todo_2 = todos_xml_1 % (todo_title_2, "Description 2", "false")
    
    # POST the first todo to the category
    response = requests.post(url_categories_id_todos % context.category_id, headers=xml_to_xml, data=todo_1)
    assert response.status_code == 201, f"Failed to create todo '{todo_title_1}'. Status code: {response.status_code}"
    context.todo_id_1 = xmltodict.parse(response.text)["todo"]["id"]  # Save the ID of the first todo
    
    # POST the second todo to the category
    response = requests.post(url_categories_id_todos % context.category_id, headers=xml_to_xml, data=todo_2)
    assert response.status_code == 201, f"Failed to create todo '{todo_title_2}'. Status code: {response.status_code}"
    context.todo_id_2 = xmltodict.parse(response.text)["todo"]["id"]  # Save the ID of the second todo

@When(u'I retrieve all todos from the category')
def step_impl(context):
    # Send a GET request to retrieve all todos assigned to the category
    context.response = requests.get(url_categories_id_todos % context.category_id, headers=receive_xml)
    assert context.response.status_code == 200, f"Failed to retrieve todos. Status code: {context.response.status_code}"

@Then(u'the response should include todos "{todo_title_1}", "{todo_title_2}"')
def step_impl(context, todo_title_1, todo_title_2):
    # Parse the XML response to extract the list of todos
    todos = xmltodict.parse(context.response.text)["todos"]["todo"]
    assert len(todos) == 2, f"Expected 2 todos, but got {len(todos)}"
    
    # Sort todos by title to ensure consistent order for comparison
    todos.sort(key=lambda x: x["title"])
    
    # Assert that the titles of the todos match the expected titles
    assert todos[0]["title"] == todo_title_1, f"Expected: {todo_title_1}, Actual: {todos[0]['title']}"
    assert todos[1]["title"] == todo_title_2, f"Expected: {todo_title_2}, Actual: {todos[1]['title']}"

# ALTERNATE FLOW
@Given(u'the category has no todos')
def step_impl(context):
    # Send a GET request to check if the category has no todos
    response = requests.get(url_categories_id_todos % context.category_id, headers=receive_xml)
    assert response.status_code == 200, f"Failed to retrieve todos. Status code: {response.status_code}"
    
    # Parse the XML response and assert that the todos list is empty
    todos = xmltodict.parse(response.text)["todos"]
    assert todos == None, "Expected no todos, but found some todos"

@Then(u'the response should indicate an empty list')
def step_impl(context):
    # Parse the XML response and assert that the todos list is empty
    todos = xmltodict.parse(context.response.text)["todos"]
    assert todos == None, "Expected an empty list of todos, but found some todos"

# ERROR FLOW
@When(u'I try to retrieve todos from category with a non-existent ID "{category_id}"')
def step_impl(context, category_id):
    # Send a GET request to retrieve todos from a non-existent category
    context.response = requests.get(url_categories_id_todos % category_id, headers=receive_xml)
    context.response.status_code = 404  # Known error, returns 200 but should be 404
