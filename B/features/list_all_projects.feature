Feature: List all projects
    As a user,
    I want to retrieve a list of all projects in /projects
    so that I can see all my ongoing work.

    # Normal Flow
    Scenario: Successfully retrieve all projects
        Given there are existing projects in the system
        When I request a list of all projects
        Then I should receive a response containing all projects

    # Alternative Flow
    Scenario: Retrieve projects when no projects exist
        Given there are no projects in the system
        When I request a list of all projects
        Then I should receive an empty list of projects

    # Error Flow
    Scenario: Attempt to retrieve projects from an invalid endpoint
        When I send a GET request to an invalid endpoint "/invalid_projects"
        Then I should receive an error: status code 404
