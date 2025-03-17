Feature: Create a new todo task
    As a user, I want to create a new task in /todo so that I can track my work.


    # Normal Flow
    Scenario Outline: Successfully create a new todo
        Given there is no existing todo item with title "<task_title>", description "<task_description>" and doneStatus "<task_doneStatus>"
        When I create a todo with title "<task_title>" and description "<task_description>"
        Then the todo should be saved in the system with doneStatus "False"
        Examples:
            | task_title     | task_description                    | task_doneStatus |
            | Write report   | Finish the ECSE 429 Written report  | False           |
            | Buy groceries  | Milk, eggs, and bread               | False           |
            | Go to Gym      | 10xSquats, 10xLunges, 10xDeadlifts  | False           |

    # Alternative Flow
    Scenario Outline: Create a todo with only a title
        When I create a todo with title "<task_title>" and no description "<task_description>" and no doneStatus "<task_doneStatus>"
        Then the todo should be saved with an empty description and doneStatus "False"
        Examples:
            | task_title   | task_description | task_doneStatus |
            | Team meeting |                  | False           |
            | Submit essay |                  | False           |

    # Error Flow
    Scenario Outline: Attempt to create a todo without a title
        When I attempt to add a task without a title "<task_title>"
        And only provide a description "<task_description>"
        Then I should receive an error: status code 400
