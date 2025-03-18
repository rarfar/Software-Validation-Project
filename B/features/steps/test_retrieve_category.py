from behave import *
import requests
import xmltodict
from helpers import *

# NORMAL FLOW
@Given(u'a category exists with title "{category_title}"')
def step_impl(context, category_title):
    xml = f"""
    <category>
        <title>{category_title}</title>
    </category>"""
    response = requests.post(url_categories, headers=xml_to_xml, data=xml)
    context.category_id = xmltodict.parse(response.text)["category"]["id"]
    assert response.status_code == 201

@When(u'I retrieve the category with its generated ID')
def step_impl(context):
    response = requests.get(url_categories_id % context.category_id, headers=receive_xml)
    context.response = response
    assert response.status_code == 200

@Then(u'the response should include title "{category_title}"')
def step_impl(context, category_title):
    response = xmltodict.parse(context.response.text)
    print(response)
    assert response["categories"]["category"]["title"] == category_title

# ALTERNATIVE FLOW
@Given(u'at least one category exists in categories')
def step_impl(context):
    response = requests.get(url_categories, headers=receive_xml)
    context.response = response
    assert response.status_code == 200

@When(u'I retrieve all categories')
def step_impl(context):
    response = requests.get(url_categories, headers=receive_xml)
    context.response = response
    assert response.status_code == 200

@Then(u'the response should include the titles of every existing category')
def step_impl(context):
    response = xmltodict.parse(context.response.text)
    print(response)
    assert len(response["categories"]["category"]) > 0
    for category in response["categories"]["category"]:
        assert "title" in category

# ERROR FLOW
@Given(u'there is no category with ID "{category_id}"')
def step_impl(context, category_id):
    response = requests.delete(url_categories_id % category_id)
    assert response.status_code == 404

@When(u'I try to retrieve a category with an invalid ID "{category_id}"')
def step_impl(context, category_id):
    response = requests.get(url_categories_id % category_id, headers=receive_xml)
    context.response = response
    assert response.status_code == 404

@Then(u'I should receive an error: status code 404')
def step_impl(context):
    assert context.response.status_code == 404
