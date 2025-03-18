from behave import *
import requests
import xmltodict
import subprocess
from helpers import *

# Normal Flow
@Given(u'there is no existing category with title "{category_title}" and with description "{category_description}"')
def step_impl(context, category_title, category_description):
    # check if the category already exists
    response = requests.get(url_categories, headers=receive_xml)
    categories = xmltodict.parse(response.text)["categories"]["category"]
    print(categories)
    assert not any(category["title"] == category_title for category in categories) and response.status_code == 200

@When(u'I create a category with title "{category_title}" and with description "{category_description}"')
def step_impl(context, category_title, category_description):
    # create the xml data for new category
    new_category_xml = f"""
    <category>
        <title>{category_title}</title>
        <description>{category_description}</description>
    </category>"""

    response = requests.post(url_categories, headers=send_xml, data=new_category_xml)
    assert response.status_code == 201

@Then(u'the category with title "{category_title}" and description "{category_description}" should be saved in the system')
def step_impl(context, category_title, category_description):
    # check if the category was saved
    response = requests.get(url_categories, headers=receive_xml)
    categories = xmltodict.parse(response.text)["categories"]["category"]
    # get matching category
    saved_category = None
    for category in categories:
        print(category["title"])
        if category["title"] == category_title:
            saved_category = category
            break
    assert saved_category["title"] == category_title and saved_category["description"] == category_description and response.status_code == 200

# Alternative Flow
@Given(u'there is no existing category with title "{category_title}"')
def step_impl(context, category_title):
    # check if the category already exists
    response = requests.get(url_categories, headers=receive_xml)
    categories = xmltodict.parse(response.text)["categories"]["category"]
    assert not any(category["title"] == category_title for category in categories) and response.status_code == 200

@When(u'I create a category with title "{category_title}" but with no description')
def step_impl(context, category_title):
    # create the xml data for new category
    new_category_xml = f"""
    <category>
        <title>{category_title}</title>
    </category>"""

    response = requests.post(url_categories, headers=send_xml, data=new_category_xml)
    assert response.status_code == 201

@Then(u'the category with title "{category_title}" should still be created successfully')
def step_impl(context, category_title):
    # check if the category was saved
    response = requests.get(url_categories, headers=receive_xml)
    categories = xmltodict.parse(response.text)["categories"]["category"]
    # get matching category
    saved_category = None
    for category in categories:
        print(category["title"])
        if category["title"] == category_title:
            saved_category = category
            break
    assert saved_category is not None and saved_category["title"] == category_title and response.status_code == 200

# Error Flow
@When(u'I attempt to add a category without a title')
def step_impl(context):
    # create the xml data for new category
    new_category_xml = f"""
    <category>
    </category>"""

    response = requests.post(url_categories, headers=send_xml, data=new_category_xml)
    context.response = response
    assert response.status_code == 400

@Then(u'I should receive an error: status code 400')
def step_impl(context):
    response = context.response
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    error_message = response.text
    assert "error" in error_message.lower(), f"Expected an error message, but got: {error_message}"