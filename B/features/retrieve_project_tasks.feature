Feature: Retrieve all tasks related to a specific project
    As a user,
    I want to retrieve all tasks related to a specific project in /projects/:id/tasks
    So that I can see the tasks associated with my project.

    # Normal Flow
    Scenario Outline: Successfully retrieve all tasks for a project
        Given a project exists with title "<project_title>"
        And the project has tasks "<task_title_1>" and "<task_title_2>"
        When I request all tasks for the project
        Then I should receive a list containing the tasks "<task_title_1>" and "<task_title_2>"
        Examples:
            | project_title  | task_title_1    | task_title_2     |
            | School Tasks   | Math Homework   | Science Report   |
            | Work Project   | Code Review     | Documentation    |

    # Alternative Flow
    Scenario Outline: Retrieve tasks when a project has no tasks
        Given a project exists with title "<project_title>"
        And the project has no tasks
        When I request all tasks for the project
        Then I should receive an empty task list
        Examples:
            | project_title |
            | Vacation Plan |

    # Error Flow
    Scenario: Attempt to retrieve tasks for a non-existent project
        When I request tasks for a non-existent project
        Then I should receive a response (even if the project does not exist)

