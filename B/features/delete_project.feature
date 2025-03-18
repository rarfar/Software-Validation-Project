Feature: Delete a Project
    As a user,
    I want to delete a project in /projects
    so that I can remove projects I no longer need.

    Background:
        Given the /projects system is running

    # Normal Flow: Successfully delete a project
    Scenario Outline: Successfully delete a project
        Given a project exists with title "<project_title>"
        When I delete the project with title "<project_title>"
        Then the project should no longer exist
        Examples:
            | project_title |
            | Fitness Plan  |
            | Home Repairs  |

    # Alternative Flow: Attempt to delete a project already deleted
    Scenario Outline: Attempt to delete a project twice
        Given a project exists with title "<project_title>"
        When I delete the project with title "<project_title>"
        And I attempt to delete the same project again
        Then I should receive an error: status code 404
        Examples:
            | project_title |
            | Old Workspace |
            | Gardening Plan |

    # Error Flow: Deleting a non-existent project
    Scenario Outline: Attempt to delete a non-existent project
        When I send a DELETE request to "/projects/999999"
        Then I should receive a 404 error when deleting a project

