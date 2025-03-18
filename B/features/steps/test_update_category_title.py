from behave import *  # Import all necessary decorators and functions from behave
import requests  # For making HTTP requests
import xmltodict  # For parsing XML responses
from helpers import *  # Import helper variables and functions (e.g., headers, URLs)

# NORMAL FLOW
# Given step is already implemented elsewhere

@When('I update the category title to "{new_category_title}"')
def step_impl(context, new_category_title):
    # Create the XML payload to update the category title
    xml = f'''
    <category>
        <title>{new_category_title}</title>
    </category>'''
    # Send a PUT request to update the category title
    response = requests.put(url_categories_id % context.category_id, headers=xml_to_xml, data=xml)
    # Save the new title in the context for validation in the next step
    context.new_category_title = new_category_title

@Then('the category title should be updated in the system')
def step_impl(context):
    # Send a GET request to retrieve the updated category
    response = requests.get(url_categories_id % context.category_id, headers=receive_xml)
    # Assert that the title in the system matches the updated title
    assert context.new_category_title == xmltodict.parse(response.text)["categories"]["category"]["title"]

@When(u'I update the category description to "{new_category_description}"')
def step_impl(context, new_category_description):
    # Create the XML payload to update the category description
    xml = f'''
    <category>
        <title>{context.category_title}</title>
        <description>{new_category_description}</description>
    </category>'''
    # Send a PUT request to update the category description
    response = requests.put(url_categories_id % context.category_id, headers=xml_to_xml, data=xml)
    # Save the new description in the context for validation in the next step
    context.new_category_description = new_category_description
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

@Then(u'the category description should be updated in the system')
def step_impl(context):
    # Send a GET request to retrieve the updated category
    response = requests.get(url_categories_id % context.category_id, headers=receive_xml)
    # Assert that the description in the system matches the updated description
    assert context.new_category_description == xmltodict.parse(response.text)["categories"]["category"]["description"]

# ERROR FLOW
# Given step is already implemented elsewhere

@When(u'I attempt to update category with ID "{category_id}"')
def step_impl(context, category_id):
    # Create the XML payload for the update attempt
    xml = '''
    <category>
        <title>nonexistent id</title>
        <description>should fail</description>
    </category>'''
    # Send a PUT request to update a category with a non-existent ID
    response = requests.put(url_categories_id % category_id, headers=xml_to_xml)
    # Save the response in the context for validation in the next step
    context.response = response
    # Assert that the response status code is 404 (Not Found)
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"

# Then step is already implemented elsewhere
