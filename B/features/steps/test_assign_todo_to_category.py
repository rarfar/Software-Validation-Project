from behave import *
import requests
import xmltodict
from helpers import *

# NORMAL FLOW
# Given step is already implemented elsewhere
@When(u'I assign a todo "{todo_title}" with description "{todo_description}" to the category "{category_title}"')
def step_impl(context, todo_title, todo_description, category_title):
    
    # Send a POST request to create the relationship between the category and the todo
    response = requests.post(url_categories_id_todos % context.category_id, headers=xml_to_xml, data=todos_xml_1 % (todo_title, todo_description, "false"))
    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

@Then(u'the todo "{todo_title}" should be linked to the category "{category_title}"')
def step_impl(context, todo_title, category_title):
    # Send a GET request to retrieve the todos assigned to the category
    response = requests.get(url_categories_id_todos % context.category_id, headers=receive_xml)
    
    # Parse the XML response
    response_dict = xmltodict.parse(response.text)
    
    # Get the list of todos assigned to the category
    todos = response_dict["todos"]["todo"]
    
    # Handle the case where there is only one todo (a dictionary) or multiple todos (a list)
    if isinstance(todos, dict):  # Single todo
        todos = [todos]  # Convert to a list for consistency
    
    # Assert that the todo is in the list of todos assigned to the category
    assert any(todo["title"] == todo_title for todo in todos), f"Todo {todo_title} not found in the list of todos assigned to the category"

# ALTERNATE FLOW
# Given step is already implemented elsewhere
@When(u'I assign a todo "{todo_title}" with no description to the category "{category_title}"')
def step_impl(context, todo_title, category_title):
    
    # Send a POST request to create the relationship between the category and the todo
    response = requests.post(url_categories_id_todos % context.category_id, headers=xml_to_xml, data=todos_xml_1 % (todo_title, "", "false"))
    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

@Then (u'the todo "{todo_title}" without a definition should be linked to the category "{category_title}"')
def step_impl(context, todo_title, category_title):
    # Send a GET request to retrieve the todos assigned to the category
    response = requests.get(url_categories_id_todos % context.category_id, headers=receive_xml)
    
    # Parse the XML response
    response_dict = xmltodict.parse(response.text)
    
    # Get the list of todos assigned to the category
    todos = response_dict["todos"]["todo"]
    
    # Handle the case where there is only one todo (a dictionary) or multiple todos (a list)
    if isinstance(todos, dict):
        todos = [todos]
    
    # Assert that the todo is in the list of todos assigned to the category
    assert any(todo["title"] == todo_title for todo in todos), f"Todo {todo_title} not found in the list of todos assigned to the category"
    print(todos)
    # Assert that the todo has no description
    assert all(todo["description"] is None for todo in todos), "Todo has a description"

# ERROR FLOW
@When(u'I attempt to assign a todo "{todo_title}" to a category with an invalid ID "{category_id}"')
def step_impl(context, todo_title, category_id):
        
        # Send a POST request to create the relationship between the category and the todo
        response = requests.post(url_categories_id_todos % category_id, headers=xml_to_xml, data=todos_xml_1 % (todo_title, "Todo description", "false"))
        # Save the response in the context for validation in the next step
        context.response = response

        assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"

# Then step is already implemented elsewhere
