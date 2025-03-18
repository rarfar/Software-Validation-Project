Feature: Get all todos from a category
    As a user,
    I want to retrieve all todos in a category from /categories
    so that I can see all tasks related to that category.

    Background:
        Given the API is running


    # Normal Flow
    Scenario Outline: Successfully retrieve all todos in a category
        Given a category exists with title "<category_title>"
        And the category contains todos "<todo_title_1>", "<todo_title_2>"
        When I retrieve all todos from the category
        Then the response should include todos "<todo_title_1>", "<todo_title_2>"
        Examples:
            | category_title | todo_title_1    | todo_title_2  |
            | Work           | "Finish report" | Emails        |
            | Shopping       | "Groceries"     | Play sports   |

    # Alternative Flow
    Scenario Outline: Retrieve todos when category is empty
        Given a category exists with title "<category_title>"
        And the category has no todos
        When I retrieve all todos from the category
        Then the response should indicate an empty list
        Examples:
            | category_title |
            | Travel        |
            | Fitness       |

    # Error Flow
    Scenario Outline: Attempt to retrieve todos from a non-existent category
        When I try to retrieve todos from category with a non-existent ID "<category_id>"
        Then I should receive an error: status code 404
        Examples:
            | category_id  |
            | 999         |
            | ABC         |
