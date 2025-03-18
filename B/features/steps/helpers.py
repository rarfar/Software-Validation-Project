# HEADERS
send_xml =       {"Content-Type":  "application/xml"}
send_json =      {"Content-Type":  "application/json"}
receive_xml =    {"Accept": "application/xml"}
receive_json =   {"Accept": "application/json"}
xml_to_xml =     {"Content-Type":  "application/xml", "Accept": "application/xml"}
xml_to_json =    {"Content-Type":  "application/xml", "Accept": "application/json"}
json_to_xml =    {"Content-Type":  "application/json", "Accept": "application/xml"}
json_to_json =   {"Content-Type":  "application/json", "Accept": "application/json"}

# URLs
# todos
url_todos = "http://localhost:4567/todos"
url_todos_id = "http://localhost:4567/todos/%s"
url_todos_id_tasksof = "http://localhost:4567/todos/%s/tasksof"
url_todos_id_tasksof_id = "http://localhost:4567/todos/%s/tasksof/%s"
url_todos_id_categories = "http://localhost:4567/todos/%s/categories"
url_todos_id_categories_id = "http://localhost:4567/todos/%s/categories/%s"
# projects
url_projects = "http://localhost:4567/projects"
url_projects_id = "http://localhost:4567/projects/%s"
# categories
url_categories = "http://localhost:4567/categories"
url_categories_id = "http://localhost:4567/categories/%s"
url_categories_id_todos = "http://localhost:4567/categories/%s/todos"
url_categories_id_todos_id = "http://localhost:4567/categories/%s/todos/%s"

# XML templates
# TODOS
# normal
todos_xml_1 = """ 
<todo>
    <title>Todo 1</title>
    <description>Todo 1 description</description>
    <doneStatus>false</doneStatus>
</todo> """
# PROJECTS

# CATEGORIES
# normal
categories_xml_1 = """
<category>
    <title>Category 1</title>
    <description>Category 1 description</description>
</category>"""

# no description
categories_xml_2 = """
<category>
    <title>Category 2</title>
</category>"""

# no title
categories_xml_3 = """ 
<category>
    <description>Category 3 description</description>
</category>"""