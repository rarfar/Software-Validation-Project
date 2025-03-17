Feature: List all tasks to review my progress
    As a user,
    I want to list all my tasks
    so that I can review my progress.

    Background:
        Given the /todos system is running

    # Normal Flow
    Scenario: Successfully list all tasks
        When I send a GET request to "/todos"
        Then I should receive a status code 200
        And the response should contain a list of all todo items

    # Alternative Flow
    Scenario: List all tasks when no tasks exist
        When I send a GET request to "/todos"
        Then I should receive a status code 200
        And the response should be an empty list

    # Error Flow
    Scenario: Attempt to list tasks when there is a system failure
        Given the /todos system is down
        When I send a GET request to "/todos"
        Then I should receive a status code 500
        And the response should indicate an internal server error
