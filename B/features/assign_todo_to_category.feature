Feature: Assign a todo to a category
    As a user,
    I want to assign a todo to a category in /categories
    so that I can group related tasks together.

    # Normal Flow
    Scenario Outline: Successfully assign a todo to a category
        Given a category exists with title "<category_title>"
        When I assign a todo "<todo_title>" with description "<todo_description>" to the category "<category_title>"
        Then the todo "<todo_title>" should be linked to the category "<category_title>"
        Examples:
            | todo_title     | todo_description   | category_title |
            | Buy groceries  | Milk, Eggs, Butter | Shopping       |
            | Finish report  | Intro, Analysis    | Work           |

    # Alternative Flow
    Scenario Outline: Assign a todo without a description to a category
        Given a category exists with title "<category_title>"
        When I assign a todo "<todo_title>" with no description to the category "<category_title>"
        Then the todo "<todo_title>" without a definition should be linked to the category "<category_title>"
        Examples:
            | todo_title     | category_title |
            | Buy groceries  | Shopping       |
            | Finish report  | Work           |

    # Error Flow
    Scenario Outline: Attempt to assign a non-existent todo
        When I attempt to assign a todo "<todo_title>" to a category with an invalid ID "<category_id>"
        Then I should receive an error: status code 404
        Examples:
            | todo_title        | category_id  |
            | Buy Groceries     | 999          |
            | Finish report     | ABC          |
