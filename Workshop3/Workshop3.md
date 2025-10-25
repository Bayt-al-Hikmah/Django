## Objectives
- Working with Database and Django Models  
- Authentication and Session Management  
- Working with Django Shell  
- Managing the Admin Panel
## Databases and Django Models  
In our previous sessions, we built apps that displayed dynamic content. For example, in our `feedback` app, we accepted user input and stored it in a simple Python list. However, that list exists only in **RAM (memory)** meaning it’s temporary.  
This approach has a serious limitation: **data stored in memory is volatile**. As soon as the Django server restarts, shuts down, or crashes whether due to maintenance, updates, or deployment all the information in that list is instantly **lost**.  
To build real, reliable web applications, we need a way to store data **permanently**, so it remains available even after the server restarts. This is where **databases** come in.
### Database
A database is a specialized, structured system for storing, managing, and retrieving information efficiently. Instead of vanishing when the server stops, a database saves our data permanently on disk, ensuring it's still there the next time our application starts.  
Databases are essential because they:
- **Store data persistently** (it doesn't disappear when the app restarts).
- **Organize data** in a structured, reliable format.
- Allow us to **query and filter** data efficiently (e.g., "find all tasks for user 'Alice'").
- **Maintain data integrity and security**, even when many users are reading and writing data at the same time.
### Types of Databases
Databases aren’t one-size-fits-all. They come in different types, depending on how they organize and manage data.    
The two main categories you’ll encounter are:
#### Relational Databases (SQL)
These are the most common type of database. They store data in **tables** made up of **rows** and **columns**, much like organized spreadsheets that can be linked together.  
Relational databases use a specialized language called **SQL (Structured Query Language)** to create, read, update, and delete data.  
They’re ideal for applications where data relationships and structure are important.  
**Examples:** SQLite, PostgreSQL, MySQL, Oracle.
#### Non-Relational Databases (NoSQL)
These databases are more flexible and store data in various formats such as **documents** (like JSON), **key-value pairs**, **wide-column stores**, or **graphs**.  
They’re often used for large-scale systems, unstructured data, or applications that need to handle rapidly changing information.   
**Examples:** MongoDB, Redis, Cassandra

For most web applications and especially for Django projects we use a **relational database**. Django is designed around the structured, table-based model, and its most powerful features are built to work seamlessly with it.
### Relational Databases Structure
A **relational database** stores data in **tables**, similar to how a spreadsheet organizes information.  
Each table represents a specific **entity type** for example, a `Customers` table or an `Orders` table.  
Each **row** in a table represents a single record a specific customer, order, or product.  
Each **column** defines a property or field, describing what kind of information is stored such as `name`, `email`, `order_date`, or `total_amount`.
#### Primary Keys
To keep data organized and ensure each record is unique, every table includes a **primary key**.  
A **primary key** is a special column (or combination of columns) that uniquely identifies each record in a table.
- It prevents duplicate entries.
- It allows the database to quickly find, update, or delete specific rows.

In most cases, the primary key is an automatically generated integer called `id`, but it can also be another unique value like an email address or a UUID.
**Example: Customers Table**

|id (Primary Key)|name|email|
|---|---|---|
|1|Alice Smith|[alice@example.com](mailto:alice@example.com)|
|2|Bob Johnson|[bob@example.com](mailto:bob@example.com)|

Here:
- Each row represents one unique customer.
- Each column stores a property of that customer.
- The `id` column serves as the **primary key**, guaranteeing that no two customers share the same identifier.

The database enforces **data integrity** by applying rules such as data types (text, numbers, dates) and constraints (e.g., required fields or unique values).

### Foreign Keys and Relationships
Relational databases are powerful because they can define **relationships** between tables linking related data without duplicating it. This is done through **foreign keys**.    
A **foreign key** is a column in one table that refers to the **primary key** of another table.  
This creates a connection between records and ensures consistency for example, preventing the deletion of a customer who still has existing orders.

### Common Types of Relationships
**One-to-One**  
Each record in Table A is linked to exactly one record in Table B, and vice versa.  
This is useful when splitting related data into separate tables.  
**Example:** A `Users` table and a `UserProfiles` table, where each profile corresponds to exactly one user via a foreign key referencing the user’s `id`.  

**One-to-Many**  
A single record in one table can be linked to multiple records in another, but each of those records refers back to only one parent.    
This is the most common type of relationship  for example, one customer can place many orders.  
**Example: Orders Table**

| id (Primary Key) | order_date | total_amount | customer_id (Foreign Key) |
| ---------------- | ---------- | ------------ | ------------------------- |
| 101              | 2025-10-25 | 45.99        | 1                         |
| 102              | 2025-10-26 | 29.50        | 1                         |
| 103              | 2025-10-27 | 100.00       | 2                         |

- The `customer_id` column is a **foreign key** referencing the `id` in the `Customers` table.
- This forms a **one-to-many** relationship: Customer 1 has two orders, while Customer 2 has one.

**Many-to-Many**  
In this relationship, multiple records in Table A can be linked to multiple records in Table B.  
To manage this, a third table often called a **junction** or **association** table  is used to store the connections.  
**Example:** In a library system, one **book** can have multiple **authors**, and one **author** can write multiple **books**.    
A `BookAuthors` table would contain pairs of foreign keys linking books and authors:

|book_id (FK)|author_id (FK)|
|---|---|
|10|3|
|10|5|
|12|3|

This structure keeps the data organized and avoids duplication while preserving relationships.
### Connecting Apps to Databases
Now that we understand what databases are and how they store data, let’s talk about how our **Django application** can actually communicate with one.  
In Python, we can connect to a database using various **database connector modules**. For example:
- `sqlite3` for SQLite databases (built into Python)
- `mysqlclient` or `PyMySQL` for MySQL
- `psycopg2` for PostgreSQL

Once connected, we can write **SQL queries** directly inside our Python code to create tables, insert data, or retrieve records.  
For example, using SQLite directly in Python:
```python 
import sqlite3

# Connect to a database (or create it)
connection = sqlite3.connect("example.db")

# Create a cursor to run SQL commands
cursor = connection.cursor()

# Create a table
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")

# Insert data
cursor.execute("INSERT INTO users (name) VALUES ('Alice')")

# Commit changes and close
connection.commit()
connection.close()
```
This works, but there’s a **big drawback**:  
we’re mixing **raw SQL queries** directly with **Python logic** and potentially even **views or routes**.  
That makes our code harder to maintain, debug, and scale.  
Even worse, if we decide to switch databases (say, from SQLite to PostgreSQL), we’ll need to **rewrite every single query**, since SQL syntax and data types can vary slightly between systems.  
This approach doesn’t align with the **Django philosophy** of keeping code clean, organized, and reusable.  
Luckily, Django gives us a much better solution through its built-in **Object-Relational Mapper (ORM)**.
### Understanding ORM and Its Benefits
An Object-Relational Mapper (ORM) is a layer of abstraction that bridges the gap between our application's code  and the relational database's tabular structure. It translates Python operations into SQL queries automatically, handling the underlying database interactions without us writing SQL directly.     
Here are the key roles and benefits of using an ORM:
#### Abstraction and Portability:  
You define your data structure using Python classes, and the ORM generates the appropriate SQL commands for your chosen database backend (e.g., SQLite, PostgreSQL, or MySQL).  
If you ever switch databases, you only need to change a configuration setting — not rewrite your queries.
#### Improved Productivity and Readability:  
Instead of juggling raw SQL strings, you work entirely in Python. This keeps your code cleaner, more expressive, and easier to maintain, especially as your project grows.
#### Data Integrity and Security:  
The ORM enforces relationships like primary and foreign keys, manages schema migrations, and automatically escapes inputs protecting your app from SQL injection and ensuring consistent, valid data.
#### Query Optimization and Flexibility:  
Django’s ORM supports **lazy loading**, **filtering**, and **complex lookups** using a fluent API, letting you perform advanced queries efficiently without writing raw SQL.
    
#### Team Consistency and Maintainability:  
By using the same data access patterns, all developers on a team can easily read and extend each other’s code without worrying about database-specific syntax.

In short, Django’s ORM lets you focus on your application’s **logic** rather than the low-level details of **database management** making development faster, safer, and far more enjoyable.
### Working with Django Models
Now that we understand what the ORM is and why it’s useful, let’s see how Django actually applies it in our projects.  
Each time we create a **new Django app**, Django automatically includes a file called **`models.py`**.  
This file is where we define our **data models** the Python classes that describe the structure of our database tables.  Each **model class** represents a table, and each **class attribute** represents a column inside that table.  
When we define a model, Django’s ORM automatically creates the corresponding table (and columns) in the database once we apply the migrations.  
Here’s a simple example of what a model looks like inside `models.py`:
```python
from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```
In this example, we start by importing Django’s **`models`** module, which provides all the tools we need to define our database models. Then, we create a class called **`Todo`** that inherits from `models.Model`. This inheritance tells Django that our class represents a database table, and that each attribute we define inside it should become a column in that table.  
Inside the class, we define three fields. The first one, **`title`**, is a `CharField`  a short text field that stores the name or title of our task. We set `max_length=200` to limit it to 200 characters.  
The second field, **`description`**, is a `TextField` used for longer text, allowing us to write detailed information about the task without any character limit.   
Finally, the **`created_at`** field is a `DateTimeField` with `auto_now_add=True`, which means Django will automatically record the date and time when each todo item is first created.  

Together, these three fields define the structure of our **`Todo`** model and once we apply migrations, Django will create a corresponding table in the database. Each instance of the `Todo` class will represent one row in that table, making it easy to store, retrieve, and manage our todo items directly through Python.
### Creating Our App
Let’s create a new app called **`todo_list`** to put our model knowledge into practice. This app will let us **view tasks** and **add new ones**, as well as keep track of whether each task is completed or not.  
First, let’s create a new Django project named **`workshop3`**, then create a new app inside it called **`todo_list`** using the following commands:
```bash
django-admin startproject workshop3
cd workshop3
python manage.py startapp todo_list #python3 for mac/linux
```
Next, we need to add our new app to the list of installed apps in the project’s settings file.  
Open **`workshop3/settings.py`** and update the `INSTALLED_APPS` list like this:
```python
INSTALLED_APPS = [
    'todo_list',  # Added todo app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
#### Creating The Task Model
Now, we’ll define the structure of our tasks by creating a model.  
Open **`todo_list/models.py`** and add the following code:
```python
from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```
Here’s what each field does:
- **`title`** – a short text field that holds the name of the task.
- **`description`** – a longer text area for task details.
- **`done`** – a boolean value to track whether the task is completed or not.
- **`created_at`** – automatically stores the date and time when the task was created.

After creating a model, we always need to create and apply migrations so Django can update the database structure accordingly.    
To do this, we run the following commands in the terminal:
```bash
python manage.py makemigrations # python3 for mac/linux
python manage.py migrate # python3 for mac/linux
```
- **`makemigrations`** tells Django to prepare migration files based on the changes we made to our models.
- **`migrate`** applies those migrations to the database, creating or updating the necessary tables.
#### Creating the Form
Now that we’ve defined our model and set up the database, we’ll create a **form** that allows users to add new tasks easily.
Django provides a powerful feature called **ModelForm**, which automatically creates a form based on our model’s fields, this saves us from writing repetitive HTML form code and keeps our form consistent with the model definition.  
Let’s create a new file called **`forms.py`** inside our `todo_list` app:  
**`todo_list/forms.py`**
```python 
from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description']
```
First, we import the `forms` module from Django, along with our `Todo` model.  
Next, we define a new class called **`TodoForm`**, which inherits from `forms.ModelForm`. This tells Django that our form should be built based on a model rather than being defined manually.  
Inside the class, we include an inner class called **`Meta`**, which provides metadata about the form.  
Here, we set the `model` attribute to our `Todo` model, indicating which model the form is connected to.  
We also specify a list of `fields` in this case, `title`, `description`, and `status` that we want to include in the form. Django will automatically create input fields for these attributes.  
The great thing about ModelForms is that they include built-in **validation** and **data handling** based on the model’s definitions.   
This means we don’t need to write extra code to ensure, for example, that required fields are filled in or that data types match.  
Once this form is created, we’ll be able to use it inside our view to both **display the input fields to users** and **save the submitted data directly to the database** all with just a few lines of code.
#### Creating the Views
Now let’s define the **views** that will handle how our app responds to user actions. These views will connect our **templates**, **form**, and **database** together allowing users to view existing tasks and add new ones seamlessly.  
Open **`todo_list/views.py`** and add the following code:
```python
from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm
from django.urls import reverse

def task_list(request):
    tasks = Todo.objects.all()
    return render(request, 'todo_list/tasks.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(revers('task_list'))
    else:
        form = TodoForm()
    return render(request, 'todo_list/add_task.html', {'form': form})
```

The **`task_list`** view acts like a “reader.”  
Every time a user visits the main page of our to-do list, this function asks the database for **all existing tasks** using `Todo.objects.all()`. It then sends that list of tasks to the **`tasks.html`** template, where Django’s template engine takes over and displays them neatly on the page.  
So whenever we load the page, the app dynamically shows the most recent data no manual refresh or hardcoding needed.  
On the other hand, the **`add_task`** view is more like a “writer.”  
It’s responsible for adding new tasks to the database. When the user first opens the page, Django sends them an **empty form** to fill out. But when they submit the form (sending a **POST** request), the view captures the data, wraps it in a `TodoForm`, and checks if it’s valid.  
If everything looks good, the form automatically creates and saves a new record in the database no need for us to write any SQL or call extra functions.  
Finally, Django redirects the user back to the task list so they can immediately see their newly added task.

#### Create the Templates
Inside our **`todo_list`** app folder, create a new folder named **`templates`**, and inside it, another folder named **`todo_list`**  inside this folder we create our templates.  
We start with our first template the one that will show the list of all to-do items saved in the database.  
**`todo_list/templates/todo_list/tasks.html`**
```html 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My To-Do List</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'todo_list/style.css' %}">
</head>
<body>
    <div class="container">
        <h1>My To-Do List</h1>
        <a href="{% url 'add_task' %}" class="btn">Add New Task</a>
        
 
        <ul class="task-list">
            {% for task in tasks %}
                <li class="{% if task.status %}done{% endif %}">
                    <strong>{{ task.title }}</strong><br>
                    {{ task.description }}
                </li>
            {% empty %}
                <li>No tasks added yet. Start by creating one!</li>
            {% endfor %}
        </ul>

    </div>
</body>
</html>
```
This template displays all the tasks,The `{% url 'add_task' %}` tag generates the link to the “Add New Task” page by referencing the route name defined in `urls.py`, so we don’t have to hardcode URLs. In the body, the template loop through the tasks using `{% for task in tasks %}`, displaying each task’s title and description with `{{ task.title }}` and `{{ task.description }}`. If a task is marked as done, the class “done” is added to style it differently. If there are no tasks yet, a simple message invites the user to create one.   

Now let’s create the form template that allows users to add new to-do items.   
**`todo_list/templates/todo_list/add_task.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Add New Task</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'todo_list/style.css' %}">
</head>
<body>
    <div class="container">
        <h1>Add a New Task</h1>

        <form method="POST">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn">Save Task</button>
        </form>

        <a href="{% url 'task_list' %}" class="btn back">Back to List</a>
    </div>
</body>
</html>
```
This template displays the form for adding new tasks. The `{{ form.as_p }}` tag automatically generates the form fields with proper formatting, while the `{% csrf_token %}` tag protects against CSRF attacks. When submitted, the form saves the new task and redirects the user back to the task list.
#### Adding the Stylesheet
We’ll now use the stylesheet from our **materials** folder. Create a file called **`style.css`** inside `todo_list/static/todo_list/` and paste the styles from  the ``material/styles.css`` file.
#### Setting The Urls
Finally, we need to connect our views to URLs so users can access them through the browser.    
Create a new file named **`todo_list/urls.py`** and add the following code:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
]
```
Next, weinclude the app’s URL configuration in the main project’s **`urls.py`** file .  
**``workshop3/urls.py``**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/', include('todo_list.urls')),
]
```
Now, when we visit **`http://127.0.0.1:8000/todo`**, we will see our task list, and at **`http://127.0.0.1:8000/todo/add/`**, we will be able to add new tasks.

## Authentication and Session Management  