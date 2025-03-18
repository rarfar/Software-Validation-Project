Feature: Create a new category
    As a user,
    I want to create a new category in /categories
    so that I can organize my todos or projects.

    

    # Normal Flow
    Scenario Outline: Successfully create a new category
        Given there is no existing category with title "<category_title>" and with description "<category_description>"
        When I create a category with title "<category_title>" and with description "<category_description>"
        Then the category with title "<category_title>" and description "<category_description>" should be saved in the system
        Examples:
            | category_title  | category_description |
            | Work            |  work category       |
            | Personal        |  personal category   |
            | School          |  school category     |

    # Alternative Flow
    Scenario Outline: Create a category with no description
        Given there is no existing category with title "<category_title>"
        When I create a category with title "<category_title>" but with no description
        Then the category with title "<category_title>" should still be created successfully
        Examples:
            | category_title  |
            | No description  |

    # Error Flow
    Scenario Outline: Attempt to create a category without a title
        When I attempt to add a category without a title
        Then I should receive an error: status code 400
        Examples:
            | category_title  |
            |                 |
