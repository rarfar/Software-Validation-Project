Feature: Update an existing project
    As a user,
    I want to update a project title
    So that I can rename it if necessary

    Background:
    Given the /projects system is running

    # Normal Flow: Successfully update a project title
    Scenario Outline: Successfully update a project title
        Given a project with title "<old_title>" exists
        When I update the project title from "<old_title>" to "<new_title>"
        Then the project title should be updated to "<new_title>"
        Examples:
            | old_title       | new_title         |
            | Home Renovation  | House Renovation  |
            | Fitness Plan     | Workout Schedule |

    # Alternative Flow: Allow updating a project title to an existing title
    Scenario Outline: Update a project title to an existing title
        Given a project with title "<existing_title>" exists
        And a project with title "<old_title>" exists
        When I update the project title from "<existing_title>" to "<old_title>"
        Then the project title should be updated to "<old_title>"

        Examples:
            | existing_title  | old_title    |
            | Home Renovation | Fitness Plan |
            | Work Project    | Study Plan   |

    # Error Flow: Attempt to update a project that does not exist
    Scenario: Attempt to update a non-existent project
        When I attempt to update a non-existent project
        Then I should receive an error: status code 404