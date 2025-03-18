Feature: Delete a todo task
    As a user,
    I want to delete a todo in /todo
    so that I can remove tasks I no longer need.

    Background:
        Given the /todo system is running

    # Normal Flow
    Scenario Outline: Successfully delete a todo
        Given a todo exists with title "<task_title>", description "<task_description>" and done status "<task_doneStatus>"
        When I delete the todo with title "<task_title>"
        Then the todo should be deleted from the system
        Examples:
            | task_title    | task_description | task_doneStatus  |
            | Write report  | Finish report    | True             |

    # Alternative Flow
    Scenario Outline: Add a task to todos, and then immediately delete it (could be a mistake or task reassigned to someone else)
        Given there is no existing todo item with title "<task_title>", description "<task_description>" and done status "<task_doneStatus>"
        When I add a todo with title "<task_title>" and description "<task_description>"
        Then the todo should be saved with doneStatus "False"
        When I delete the todo with title "<task_title>"
        Then the todo should be deleted from the system
        Examples:
            | task_title     | task_description          | task_doneStatus  |
            | Complete report| Finish ECSE 429 report    | False            |

    # Error Flow
    Scenario Outline: Attempt to delete a non-existing todo
        Given a task with title "<task_title>" description "<task_description>" and done status "<task_doneStatus>" does not exist in my list of tasks
        When I try to delete a todo with title "<task_title>"
        Then I should receive an error: status code 404
        Examples:
            | task_title       |  task_description | task_doneStatus  |
            | Write reports    | Finish report    | True              |
