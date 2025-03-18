Feature: Create a new project
    As a user,
    I want to create a new project in /projects
    so that I can organize my tasks efficiently.

    # Normal Flow
    Scenario Outline: Successfully create a new project
        Given there is no existing project with title "<project_title>" and with description "<project_description>"
        When I create a project with title "<project_title>" and with description "<project_description>"
        Then the project with title "<project_title>" and description "<project_description>" should be saved in the system
        Examples:
            | project_title         | project_description                      |
            | ECSE 429 Final Report | Complete and submit report for ECSE 429 |
            | Home Renovation       | Plan and execute home renovation tasks  |
            | Fitness Program       | Organize weekly workout routine         |

    # Alternative Flow
    Scenario Outline: Create a project with no description
        Given there is no existing project with title "<project_title>"
        When I create a project with title "<project_title>" but with no description
        Then the project with title "<project_title>" should still be created successfully
        Examples:
            | project_title    |
            | Startup Business |
            | Reading List     |

    # Error Flow
    Scenario Outline: Attempt to create a project without a title
        When I attempt to add a project without a title
        Then the project should be created with an empty title
        Examples:
            | project_title |
            |              |
