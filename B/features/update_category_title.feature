Feature: Update a category name
    As a user,
    I want to update the name of a category in /categories
    so that I can rename it if needed.

    Background:
        Given the API is running

    # Normal Flow
    Scenario Outline: Successfully update a category name
        Given a category exists with title "<category_title>"
        When I update the category title to "<new_category_title>"
        Then the category title should be updated in the system
        Examples:
            | category_title  | new_category_title |
            | Work               | Office Work       |
            | Home               | House Tasks       |

    # Alternative Flow
    Scenario Outline: Update category description
        Given a category exists with title "<category_title>"
        When I update the category description to "<new_category_description>"
        Then the category description should be updated in the system
        Examples:
            | category_title | new_category_description |
            | Gym                | Gym and Fitness          |
            | School             | List of homework         |

    # Error Flow
    Scenario Outline: Attempt to update a non-existent category
        Given there is no category with ID "<category_id>"
        When I attempt to update category with ID "<category_id>"
        Then I should receive an error: status code 404
        Examples:
            | category_id |
            | 999        |
            | ABC        |
