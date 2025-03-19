### Bug Summary Form

- Executive summary of bug in 80characters or less
- Description of bug
- Potential impact of bug on operation of system
- Steps to reproduce the bug

### BUG 1: Deleting the last task removes its project/category.
 - Description: When a user deletes the last remaining task in a project or category, the entire project or category is also removed, instead of just the task. This may lead to accidental loss of project structures.
 - Potential Impact: Users may unintentionally lose entire projects or categories when intending to remove only a single task. This could cause data loss, confusion, and workflow disruptions.
 - Steps to Reproduce:
   1. Create a project or category.
   2. Add one or more tasks to the project/category.
   3. Delete tasks one by one until only one remains.
   4. Delete the last remaining task.
   5. Observe that the entire project/category is removed instead of just the task.