from behave import *  # Import all necessary decorators and functions from behave
import requests  # For making HTTP requests
import xmltodict  # For parsing XML responses
import subprocess  # For running subprocess commands (not used in this file)
from helpers import *  # Import helper variables and functions (e.g., headers, URLs)

# Normal Flow
@Given(u'there is no existing category with title "{category_title}" and with description "{category_description}"')
def step_impl(context, category_title, category_description):
    # Check if a category with the given title and description already exists
    response = requests.get(url_categories, headers=receive_xml)  # Send GET request to fetch all categories
    categories = xmltodict.parse(response.text)["categories"]["category"]  # Parse the XML response into a dictionary
    print(categories)  # Print the list of categories for debugging
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"  # Ensure the request was successful
    # Assert that no category with the given title exists
    assert not any(category["title"] == category_title for category in categories), f"Category with title '{category_title}' already exists"

@When(u'I create a category with title "{category_title}" and with description "{category_description}"')
def step_impl(context, category_title, category_description):
    # Create the XML data for the new category
    new_category_xml = f"""
    <category>
        <title>{category_title}</title>
        <description>{category_description}</description>
    </category>"""

    # Send a POST request to create the new category
    response = requests.post(url_categories, headers=send_xml, data=new_category_xml)
    assert response.status_code == 201  # Ensure the category was created successfully

@Then(u'the category with title "{category_title}" and description "{category_description}" should be saved in the system')
def step_impl(context, category_title, category_description):
    # Check if the category was saved in the system
    response = requests.get(url_categories, headers=receive_xml)  # Send GET request to fetch all categories
    categories = xmltodict.parse(response.text)["categories"]["category"]  # Parse the XML response into a dictionary
    # Find the category with the matching title
    saved_category = None
    for category in categories:
        if category["title"] == category_title:
            saved_category = category
            break
    # Assert that the category was saved with the correct title and description
    assert saved_category["title"] == category_title and saved_category["description"] == category_description and response.status_code == 200

# Alternative Flow
@Given(u'there is no existing category with title "{category_title}"')
def step_impl(context, category_title):
    # Check if a category with the given title already exists
    response = requests.get(url_categories, headers=receive_xml)  # Send GET request to fetch all categories
    categories = xmltodict.parse(response.text)["categories"]["category"]  # Parse the XML response into a dictionary
    # Assert that no category with the given title exists
    assert not any(category["title"] == category_title for category in categories) and response.status_code == 200

@When(u'I create a category with title "{category_title}" but with no description')
def step_impl(context, category_title):
    # Create the XML data for the new category without a description
    new_category_xml = f"""
    <category>
        <title>{category_title}</title>
    </category>"""

    # Send a POST request to create the new category
    response = requests.post(url_categories, headers=send_xml, data=new_category_xml)
    assert response.status_code == 201  # Ensure the category was created successfully

@Then(u'the category with title "{category_title}" should still be created successfully')
def step_impl(context, category_title):
    # Check if the category was saved in the system
    response = requests.get(url_categories, headers=receive_xml)  # Send GET request to fetch all categories
    categories = xmltodict.parse(response.text)["categories"]["category"]  # Parse the XML response into a dictionary
    # Find the category with the matching title
    saved_category = None
    for category in categories:
        print(category["title"])  # Print the title of each category for debugging
        if category["title"] == category_title:
            saved_category = category
            break
    # Assert that the category was saved with the correct title
    assert saved_category is not None and saved_category["title"] == category_title and response.status_code == 200

# Error Flow
@When(u'I attempt to add a category without a title')
def step_impl(context):
    # Create the XML data for the new category without a title
    new_category_xml = f"""
    <category>
    </category>"""

    # Send a POST request to create the new category
    response = requests.post(url_categories, headers=send_xml, data=new_category_xml)
    context.response = response  # Save the response in the context for the next step
    assert response.status_code == 400  # Ensure the server returns a 400 Bad Request status code

@Then(u'I should receive an error: status code 400')
def step_impl(context):
    # Validate the response status code and error message
    response = context.response  # Retrieve the response from the context
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"  # Ensure the status code is 400
    error_message = response.text if response.text else ""  # Get the response body
    assert error_message, "Expected an error message, but the response body is empty"  # Ensure the response body is not empty
    assert "error" in error_message.lower(), f"Expected an error message, but got: {error_message}"  # Check if the error message contains the word "error"