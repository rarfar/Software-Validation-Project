Feature: Filter tasks by status
  As a user,
  I want to filter tasks by their status
  so that I can focus on pending work.

  Background:
    Given the /todos system is running

  # Normal Flow
  Scenario Outline: Filter tasks by "doneStatus"
    Given there are tasks with different "doneStatus" values
    When I send a GET request to "/todos?doneStatus=<doneStatus>"
    Then I should receive a status code of 200
    And the response should only contain tasks with doneStatus "<doneStatus>"
    Examples:
      | doneStatus |
      | False      |
      | True       |

  # Alternative Flow
  Scenario Outline: Filter tasks by status when no tasks match
    Given there are tasks in the system
    When I send a GET request to "/todos?doneStatus=<doneStatus>"
    Then I should receive a status code of 200
    And the response should be an empty list
    Examples:
      | doneStatus |
      | True       |
      | False      |

  # Error Flow
  Scenario Outline: Attempt to filter tasks with an invalid status
    Given there are tasks in the system
    When I send a GET request to "/todos?doneStatus=<invalid_doneStatus>"
    Then I should receive a status code of 400
    And the response should indicate a bad request error
    Examples:
      | invalid_doneStatus |
      | Completed           |
      | In Progress         |
