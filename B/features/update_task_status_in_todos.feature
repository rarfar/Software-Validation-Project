Feature: Update the done status of a todo task
    As a user,
    After I complete a task from my todo list,
    I want to update the tasks done status to True
    So that I can accurately track what still needs to get done.

    Background:
        Given the /todo system is running

    # Normal Flow
    Scenario Outline: Successfully mark a todo as done
        Given a todo exists with title "<task_title>", description "<task_description>" and doneStatus "<task_doneStatus>"
        When I update the doneStatus of "<task_title>" to "True"
        Then the todo should be saved with doneStatus "True"
        Examples:
            | task_title    | task_description | task_doneStatus |
            | Write report  | Finish report    | True            |
            | Buy groceries | Milk, eggs       | False           |

    # Alternative Flow
    Scenario Outline: Mark a completed todo as pending again
        Given a todo exists with title "<task_title>", description "<task_description>" and doneStatus "<task_doneStatus>"
        When I update the doneStatus of "<task_title>" to "False"
        Then the todo should be saved with doneStatus "False"
        Examples:
            | task_title    | task_description |task_doneStatus |
            | Write report  | Finish report    | False          |
            | Buy groceries | Milk, eggs       | False          |
    # Error Flow
    Scenario Outline: Attempt to update the doneStatus of a non-existing todo
        When I try to update the doneStatus of a non-existent task with name "<task_title>"
        Then I should receive an error: status code 404
        Examples:
            | task_title    | task_description |task_doneStatus |
            | Write report  | Finish report    | False          |
            | Buy groceries | Milk, eggs       | False          |

