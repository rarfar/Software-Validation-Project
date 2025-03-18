Feature: Retrieve a category
    As a user,
    I want to retrieve a specific category from /categories
    so that I can see its details.

    # Normal Flow
    Scenario Outline: Successfully retrieve a category by ID
        Given a category exists with title "<category_title>"
        When I retrieve the category with its generated ID
        Then the response should include title "<category_title>"
        Examples:
            | category_title  |
            | Work            |
            | Personal        |

    # Alternative Flow
    Scenario Outline: Retrieve all categories regardless of ID
        Given at least one category exists in categories
        When I retrieve all categories
        Then the response should include the titles of every existing category
        

    # Error Flow
    Scenario Outline: Attempt to retrieve a non-existent category
        Given there is no category with ID "<category_id>"
        When I try to retrieve a category with an invalid ID "<category_id>"
        Then I should receive an error: status code 404
        Examples:
            | category_id  |
            | 999         |
            | ABC         |
