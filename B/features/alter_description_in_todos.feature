Feature: Update Task Description
  As a user,
  I want to modify a task's description
  so that it accurately reflects what needs to be done.

  # Normal Flow
  Scenario Outline: Updating a task description
    Given a task exists with a title "<task_title>", description "<task_description>", and completion status "<task_doneStatus>"
    When the description is changed to "<new_task_description>"
    Then the task should reflect the updated description

    Examples:
      | task_title            | task_description | task_doneStatus | new_task_description |
      | read chapter 4        | pages 90 - 100   | False           | pages 90 - 105       |
      | write chapter report  | 3 pages          | True            | 4 pages              |


  # Alternative Flow
  Scenario Outline: Removing a task description
    Given a task exists with a the title "<task_title>", description "<task_description>", and completion status "<task_doneStatus>"
    When the description is cleared
    Then the task should have an empty description

    Examples:
      | task_title            | task_description | task_doneStatus |
      | read chapter 4        | pages 90 - 100   | False           |
      | write chapter report  | 3 pages          | True            |


  # Error Flow
  Scenario Outline: Attempting to update a non-existent task
    Given no task exists with a title "<task_title>", description "<task_description>", and completion status "<task_doneStatus>"
    When an attempt is made to update the description to "<new_task_description>" using the incorrect task ID "<wrong_task_id>"
    Then an error should indicate that the task was not found

    Examples:
      | task_title            | task_description | task_doneStatus | new_task_description | wrong_task_id |
      | read chapter 4        | pages 90 - 100   | False           | pages 90 - 105       | ABC           |
      | write chapter report  | 3 pages          | True            | 4 pages              | -9            |

