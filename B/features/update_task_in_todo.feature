Feature: Update the done status of a todo task
    As a user,
    After I complete a task from my todo list,
    I want to update the task's done status to True
    So that I can accurately track what still needs to get done.

    Background:
        Given the /todo system is running

    # Normal Flow
    Scenario Outline: Successfully mark a todo as done
        Given a todo exists with ID "<task_id>" and title "<task_title>", description "<task_description>", and doneStatus "<task_doneStatus>"
        When I update the doneStatus of the todo with ID "<task_id>" to "True"
        Then the todo should be updated with doneStatus "True"
        Examples:
            | task_title   | task_description | task_doneStatus |


    # Alternative Flow
    Scenario Outline: Alter the description of a task that may have changed but still needs to be done
        Given a todo exists with an ID "<task_id>" and title "<task_title>", description "<task_description>", and doneStatus "<task_doneStatus>"
        When I update the description of the todo with ID "<task_id>" to "<task_description>"
        Then the todo should be updated with description "<task_description>"
        Examples:
            | task_title   | task_description | task_doneStatus |


    # Error Flow
    Scenario Outline: Attempt to update the doneStatus of a non-existing todo
        Given there is no todo with ID "<task_id>"
        When I attempt to update the doneStatus of the todo with ID "<task_id>"
        Then I should receive an error: status code 404
        Examples:
            | task_id |

