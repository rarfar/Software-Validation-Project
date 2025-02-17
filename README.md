# ECSE429-Software-Validation-Project-A
 Part A: Exploratory Testing of Rest API\
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
To launch the rest api todo list manager, enter this command from your console while in the Application_Being_Tested directory:\
 java-jar runTodoManagerRestAPI-1.5.5.jar \
To execute the tests, navigate to the Softwate-Validation-Project directory in the terminal. Use pytest -v to run all tests.\
To run them in a random order, install pytest-random-order with pip install pytest-random-order, then execute pytest -v --random-order.\


