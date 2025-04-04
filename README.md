# ECSE429-Software-Validation-Project
 The application under test is a “rest api todo list manager” which may be run as a local host.\
 The application is made available by Alan Richardson and can be found online at:\
 https://github.com/eviltester/thingifier/releases \
 OR\
 can be found in this repo in the Application_Being_Tested folder
 
Requirements:
 - Python 3.11
 - import requests (if uninstalled: enter pip install requests in console)
 - import pytest   (pip install pytest)
 - import xml.etree.ElementTree 
 - pip install pytest-random-order
# Setup
To launch the rest api todo list manager, enter this command from your console while in the Application_Being_Tested directory (or wherever it is downloaded): ```java-jar runTodoManagerRestAPI-1.5.5.jar```

Enter http://localhost:4567 in your web browser to view the App's GUI.

### Running Pytest Tests (Part A)
To execute the tests, navigate to the Softwate-Validation-Project directory in the terminal. Use ```pytest -v``` to run all tests.\
To run them in a random order, install pytest-random-order with pip install pytest-random-order, then execute ```pytest -v --random-order```.\
\
You can run these tests consecutively, however, these tests add, alter and delete many elements in this app. To restore them to the default elements, you must shutdown the app and reboot it again from your console following the same steps as above.

### Running Story Tests with Behave (Part B)
To execute the story tests, navigate to the features directory and run: ```python -m behave```\
This will execute all Gherkin feature files and validate API functionality.

* If you run the tests multiple times in a row, the API must be restarted between runs to ensure a clean testing environment.
* Since the tests add, modify, and delete data, running them twice without restarting the API may result in inconsistent results or failures due to leftover data from the previous execution.

Enter http://localhost:4567/shutdown to terminate the app.

### Performance Testing (Part C)
Performance testing for the REST API was implemented using Python and psutil to track execution time, memory usage, and CPU utilization.

* All performance test scripts are located in: C/tests/
* 9 separate test files were written: Each test dynamically creates randomized data using the Faker library and logs performance as the number of operations increases. Each script also generates and saves a graph to visualize: Execution time, Memory usage and CPU percentage
* Generated graphs are saved in the root of the tests/ folder as .png files (e.g., project_add_graph.png).

### Static Analysis with SonarQube (Part C)
Static code analysis was performed using SonarQube (Community Edition). After downloading and running SonarQube locally, a new project was created via the web interface at http://localhost:9000. The source code of the REST API (thingifier-master) was analyzed using Maven with the following command:
```
mvn clean verify sonar:sonar \
  -DskipTests \
  -Dsonar.projectKey=RestAPIProject \
  -Dsonar.projectName=RestAPIProject \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=<your_token_here>
```

# Roles
TODOS       - Ryan McGregor, 260 868 511 \
PROJECTS    - Emmy Song, 261 049 871 \
CATEGORIES  - Brenden Trudeau, 260 941 695

