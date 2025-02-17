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

 
