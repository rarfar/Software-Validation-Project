import subprocess

# List of test files to run
test_files = [
    "test_add_category.py",
    "test_add_project.py",
    "test_add_todo.py",
    "test_change_category.py",
    "test_change_project.py",
    "test_change_todo.py",
    "test_delete_category.py",
    "test_delete_project.py",
    "test_delete_todo.py",
]

# Relative path for the test files from dir software-validation-project
path = "C/tests/"

# Run each test file
for test_file in test_files:
    print(f"\n\nRunning {test_file}...\n")
    try:
        # Execute the test file
        subprocess.run(["python", path + test_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while running {test_file}: {e}\n")

print("\n\nAll tests completed.\n")