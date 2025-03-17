### Bug Summary Form

- Executive summary of bug in 80characters or less
- Description of bug
- Potential impact of bug on operation of system
- Steps to reproduce the bug

### BUG 1: Incorrect JSON Example for Creating a Todo in Documentation
 - Description:
The REST API documentation provides an example JSON input for creating a todo, 
but attempting to use it results in an error. This inconsistency may mislead users 
and cause confusion. 
 - Here is what is supplied in the documentation:
Example JSON Input to API calls
{
  "title": "ur sint occaecat cup",
  "doneStatus": "false",
  "description": "m dolore eu fugiat n"
}
 - Steps to reproduce:
1. Start the todo list server with: java -jar runTodoManagerRestAPI-1.5.5.jar
2. Open another terminal and cd into Software-Validation-Project
3. execute: Invoke-WebRequest -Uri "http://localhost:4567/todos" `
  -Method Post `
  -Headers @{"Content-Type" = "application/json"} `
  -Body '{"title": "ur sint occaecat cup", "doneStatus": "false", "description": "m dolore eu fugiat n"}'
4. Observe error: Invoke-WebRequest : The remote server returned an error: (400) Bad Request.

### BUG 2: Invalid status code when supplying an invalid ID in categories/:id/projects
- Description:

The GET /categories/:id/projects endpoint returns a 200 OK status code when the specified category ID does not exist. This is incorrect behavior because a 200 OK response implies that the request was successful and that the requested resource (projects for the specified category) was found and returned. However, since the category does not exist, the server should return a 404 Not Found status code. 

- Potential Risks:

  1. Clients may interpret the 200 OK response as a successful request and attempt to process the response data, leading to unexpected behavior or errors.
  2. Clients may incorrectly assume that the category exists and proceed with operations that depend on it.

- Steps to reproduce:

  1. Open a terminal in Software-Validation-Project/Application_Being_Tested
  2. Launch the todo list server with: java -jar runTodoManagerRestAPI-1.5.5.jar
  3. Open a second terminal in Software-Validation-Project
  4. execute: Invoke-WebRequest -Uri "http://localhost:4567/categories/99999/projects" `
    -Method Get 
    * Note that 99999 is an ID number we know doesn't exist
  5. Observe error (or lack thereof): StatusCode: 200 OK, Content: {"projects":[]}

### BUG 3: Invalid status code when supplying an invalid ID in categories/:id/todos
- Description:

Very similar to BUG 2, the GET /categories/:id/todos endpoint returns a 200 OK status code when the specified category ID does not exist. This is incorrect behavior because a 200 OK response implies that the request was successful and that the requested resource (projects for the specified category) was found and returned. However, since the category does not exist, the server should return a 404 Not Found status code. 

- Potential Risks:

  1. Clients may interpret the 200 OK response as a successful request and attempt to process the response data, leading to unexpected behavior or errors.
  2. Clients may incorrectly assume that the category exists and proceed with operations that depend on it.

- Steps to reproduce:

  1. Open a terminal in Software-Validation-Project/Application_Being_Tested
  2. Launch the todo list server with: java -jar runTodoManagerRestAPI-1.5.5.jar
  3. Open a second terminal in Software-Validation-Project
  4. execute: Invoke-WebRequest -Uri "http://localhost:4567/categories/99999/todos" `
    -Method Get 
    * Note that 99999 is an ID number we know doesn't exist
  5. Observe error (or lack thereof): StatusCode: 200 OK, Content: {"todos":[]}

 
