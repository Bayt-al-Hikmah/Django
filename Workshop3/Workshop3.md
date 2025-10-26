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
A **relational database** stores data in **tables**, similar to how a spreadsheet organizes information, each table represents a specific **entity type** for example, a `Customers` table or an `Orders` table, each **row** in a table represents a single record a specific customer, order, or product, each **column** defines a property or field, describing what kind of information is stored such as `name`, `email`, `order_date`, or `total_amount`.
#### Primary Keys
To keep data organized and ensure each record is unique, every table includes a **primary key**.   
A **primary key** is a special column (or combination of columns) that uniquely identifies each record in a table.
- It prevents duplicate entries.
- It allows the database to quickly find, update, or delete specific rows.

In most cases, the primary key is an automatically generated integer called `id`, but it can also be another unique value like an email address or a UUID.  
**Example: Customers Table**

| id (Primary Key) | name        | email                                         |
| ---------------- | ----------- | --------------------------------------------- |
| 1                | Alice Smith | [alice@example.com](mailto:alice@example.com) |
| 2                | Bob Johnson | [bob@example.com](mailto:bob@example.com)     |

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
Each record in Table A is linked to exactly one record in Table B, and vice versa, this is useful when splitting related data into separate tables.    
**Example:** A `Users` table and a `UserProfiles` table, where each profile corresponds to exactly one user via a foreign key referencing the user’s `id`.    
**One-to-Many**    
A single record in one table can be linked to multiple records in another, but each of those records refers back to only one parent, this is the most common type of relationship  for example, one customer can place many orders.    
**Example: Orders Table**

| id (Primary Key)  | order_date | total_amount  | customer_id (Foreign Key) |
| ----------------- | ---------- | ------------- | ------------------------- |
| 101               | 2025-10-25 | 45.99         | 1                         |
| 102               | 2025-10-26 | 29.50         | 1                         |
| 103               | 2025-10-27 | 100.00        | 2                         |

- The `customer_id` column is a **foreign key** referencing the `id` in the `Customers` table.
- This forms a **one-to-many** relationship: Customer 1 has two orders, while Customer 2 has one.

**Many-to-Many**    
In this relationship, multiple records in Table A can be linked to multiple records in Table B, to manage this, a third table often called a **junction** or **association** table  is used to store the connections.    
**Example:** In a library system, one **book** can have multiple **authors**, and one **author** can write multiple **books**.    
A `BookAuthors` table would contain pairs of foreign keys linking books and authors:

| book_id (FK) | author_id (FK) |
| ------------ | -------------- |
| 10           | 3              |
| 10           | 5              |
| 12           | 3              |

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
we’re mixing **raw SQL queries** directly with **Python logic** and potentially even **views or routes**, that makes our code harder to maintain, debug, and scale, Even worse, if we decide to switch databases (say, from SQLite to PostgreSQL), we’ll need to **rewrite every single query**, since SQL syntax and data types can vary slightly between systems.    
This approach doesn’t align with the **Django philosophy** of keeping code clean, organized, and reusable, luckily, Django gives us a much better solution through its built-in **Object-Relational Mapper (ORM)**.
### Understanding ORM and Its Benefits
An Object-Relational Mapper (ORM) is a layer of abstraction that bridges the gap between our application's code  and the relational database's tabular structure. It translates Python operations into SQL queries automatically, handling the underlying database interactions without us writing SQL directly.      
Here are the key roles and benefits of using an ORM:
#### Abstraction and Portability:  
You define your data structure using Python classes, and the ORM generates the appropriate SQL commands for your chosen database backend (e.g., SQLite, PostgreSQL, or MySQL).    
If you ever switch databases, you only need to change a configuration setting not rewrite your queries.
#### Improved Productivity and Readability:  
Instead of juggling raw SQL strings, you work entirely in Python. This keeps your code cleaner, more expressive, and easier to maintain, especially as your project grows.
#### Data Integrity and Security:  
The ORM enforces relationships like primary and foreign keys, manages schema migrations, and automatically escapes inputs protecting your app from SQL injection and ensuring consistent, valid data.
#### Query Optimization and Flexibility:  
Django’s ORM supports **lazy loading**, **filtering**, and **complex lookups** using a fluent API, letting you perform advanced queries efficiently without writing raw SQL.
#### Team Consistency and Maintainability:  
By using the same data access patterns, all developers on a team can easily read and extend each other’s code without worrying about database-specific syntax.

In short, Django’s ORM lets us focus on your application’s **logic** rather than the low-level details of **database management** making development faster, safer, and far more enjoyable.
### Working with Django Models
Now that we understand what the ORM is and why it’s useful, let’s see how Django actually applies it in our projects, each time we create a **new Django app**, Django automatically includes a file called **`models.py`**.   
This file is where we define our **data models** the Python classes that describe the structure of our database tables.  Each **model class** represents a table, and each **class attribute** represents a column inside that table.   
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
Inside the class, we define three fields. The first one, **`title`**, is a `CharField`  a short text field that stores the name or title of our task. We set `max_length=200` to limit it to 200 characters.    
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
    'todo_list',  # Added todo app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
#### Creating The Task Model
Now, we’ll define the structure of our tasks by creating a model. open **`todo_list/models.py`** and add the following code:  
**`todo_list/models.py`:**
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
Now let’s define the **views** that will handle how our app responds to user actions. These views will connect our **templates**, **form**, and **database** together allowing users to view existing tasks and add new ones seamlessly, open **`todo_list/views.py`** and add the following code:   
**`todo_list/views.py`:** 
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
            return redirect(reverse('task_list'))
    else:
        form = TodoForm()
    return render(request, 'todo_list/add_task.html', {'form': form})

```
The **`task_list`** view acts like a “reader.”, every time a user visits the main page of our to-do list, this function asks the database for **all existing tasks** using `Todo.objects.all()`. It then sends that list of tasks to the **`tasks.html`** template, where Django’s template engine takes over and displays them neatly on the page, so whenever we load the page, the app dynamically shows the most recent data no manual refresh or hardcoding needed.    
On the other hand, the **`add_task`** view is more like a “writer.” It’s responsible for adding new tasks to the database. When the user first opens the page, Django sends them an **empty form** to fill out. But when they submit the form (sending a **POST** request), the view captures the data, wraps it in a `TodoForm`, and checks if it’s valid, if everything looks good, the form automatically creates and saves a new record in the database no need for us to write any SQL or call extra functions.    
Finally, Django redirects the user back to the task list so they can immediately see their newly added task.
#### Create the Templates
Inside our **`todo_list`** app folder, create a new folder named **`templates`**, and inside it, another folder named **`todo_list`**  inside this folder we create our templates.    
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
            {{ form.as_div }}
            <button type="submit" class="btn">Save Task</button>
        </form>
        <a href="{% url 'task_list' %}" class="btn back">Back to List</a>
    </div>
</body>
</html>
```
This template displays the form for adding new tasks. The `{{ form.as_div }}` tag automatically generates the form fields with proper formatting, while the `{% csrf_token %}` tag protects against CSRF attacks. When submitted, the form saves the new task and redirects the user back to the task list.
#### Adding the Stylesheet
We’ll now use the stylesheet from our **materials** folder. Create a file called **`style.css`** inside `todo_list/static/todo_list/` and paste the styles from  the ``material/styles.css`` file.
#### Setting The Urls
Finally, we need to connect our views to URLs so users can access them through the browser, create a new file named **`todo_list/urls.py`** and add the following code:  
**`todo_list/urls.py`:** 
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
Authentication is the process of verifying the identity of a user, device, or system before granting access to resources or data. In the context of web applications, it ensures that only authorized individuals can interact with certain parts of the app, such as viewing personal information, making changes, or performing actions.  
Without authentication, anyone could access or modify data, leading to security risks like unauthorized edits, data breaches, or misuse. Authentication typically involves credentials like usernames and passwords, but it can also include more advanced methods such as two-factor authentication (2FA), biometrics, or token-based systems.
### Authentication in Django
Django provides a robust, built-in authentication system that handles user management out of the box, saving developers from building everything from scratch. It includes models for users, views for login/logout, and utilities for password hashing and permissions. This system is flexible and can be customized for specific needs.  
Django's authentication is based on **sessions**, which allow the server to remember users across requests. Since HTTP is stateless (each request is independent), sessions provide a way to maintain state, like keeping a user logged in as they navigate pages.
#### Session on Django
How does a web application "remember" us between clicks? The web itself is **stateless** each request is independent, and the server doesn't naturally remember who we are from one page to the next.   
To solve this, Django uses **sessions**. A **session** is a mechanism that allows Django to store user-specific data between requests  essentially acting as temporary memory for the user’s interaction with the app.   
For example, once a user logs in, Django stores their user ID in a session so the app can recognize them on every subsequent page without requiring them to log in again.  
Django manages sessions seamlessly through several built-in components:  
- **Session Middleware**:  
    Automatically creates, loads, and saves session data for each request. By default, Django uses a secure, signed cookie to store the session ID, while the actual session data is stored on the server (typically in the database).  
- **Session Engine**:  
    Determines how and where session data is stored. Django supports multiple backends including database-backed (default), cache-based, and file-based sessions ensuring that session data can persist even if the server restarts.
- **Security Features**:  
    Django sessions include built-in security mechanisms such as expiration times, automatic invalidation on logout, and protection against common attacks like session fixation.

We don’t need to build an authentication system from scratch Django already includes a powerful, built-in **authentication and authorization framework**.  
This framework is pre-configured in your project’s **`workshop3/settings.py`** file. You’ll see these apps listed under `INSTALLED_APPS`:
- `'django.contrib.auth'`: Handles user accounts, passwords, permissions, and authentication logic.
- `'django.contrib.sessions'`: Manages session data that tracks logged-in users.

It also comes with essential middleware that works automatically in the background:
- `'django.contrib.sessions.middleware.SessionMiddleware'`: Manages sessions for every user request and response.
- `'django.contrib.auth.middleware.AuthenticationMiddleware'`: Attaches the currently logged-in user as a `user` object to each incoming request, making it easy to check authentication status in views and templates.
### Updating Our To-Do List App
Our current to-do app works perfectly for adding and displaying tasks but there’s one major issue: **it doesn’t implement authentication**. Right now, all users share the same task list, meaning anyone can view or add tasks that are visible to everyone else.  
To make our app more realistic and secure, we need to update it so that **each user only sees and manages their own tasks**. In other words, when a user logs in, they should only see the tasks they created and be able to edit or delete only those.   
To achieve this, we’ll:
1. **Add user authentication** a login and registration system using Django’s built-in auth framework.
2. **Update the `Todo` model** to include a reference to the user who created each task.
3. **Modify our views and templates** so that each user only interacts with their personal to-do list.
#### Adding User Authentication
Before we restrict tasks by user, we need a way for users to **register**, **log in**, and **log out**. Django makes this process simple thanks to its built-in **authentication system**, which provides all the tools we need to manage users securely no need to code it from scratch.  
Let’s start by creating a new app called **`accounts`**, which will handle all user-related features such as login, registration, and logout.
```
python manage.py startapp accounts
```
Then, we go to **`settings.py`** and add `'accounts'` to the `INSTALLED_APPS` list:
```python 
INSTALLED_APPS = [
    'todo_list',
    'accounts',  # Added accounts app for authentication
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
Now, we’ll create the templates for login and registration.  
**``accounts/templates/accounts/login.html``**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'todo_list/style.css' %}">
</head>
<body>
    <div class="container">
        <h1>Login</h1>
        <form method="POST">
            {% csrf_token %}
            {{ form.as_div }}
            <button type="submit">Login</button>
        </form>
        <p>Don’t have an account? <a href="{% url 'register' %}">Register here</a></p>
    </div>
</body>
</html>
```
And now the register template.  
**``accounts/templates/accounts/register.html``**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Register</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'todo_list/style.css' %}">
</head>
<body>
    <div class="container">
        <h1>Create an Account</h1>
        <form method="POST">
            {% csrf_token %}
            {{ form.as_div }}
            <button type="submit">Register</button>
        </form>
        <p>Already have an account? <a href="{% url 'login' %}">Login here</a></p>
    </div>
</body>
</html>
```
After this we define our views to handle user registration and login.  
**``accounts/views.py``**
```python 
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
```
Here, we define three main views to handle user authentication. The **`register_view`** lets new users create an account using Django’s built-in `UserCreationForm`; once registered, they are automatically logged in and redirected to their task list. The **`login_view`** uses Django’s `AuthenticationForm` to verify a user’s credentials and log them in securely.   
Finally, the **`logout_view`** ends the user’s session and redirects them back to the login page. These views make use of Django’s ready-made authentication system, so we don’t need to build login or registration logic from scratch.
We can notice that we imported new utilities **`UserCreationForm`**, **`AuthenticationForm`**, **`login()`**, and **`logout()`**. Here’s what they do:
The **`UserCreationForm`** is a built-in Django form that handles user registration. It automatically includes fields for username and password (with password confirmation), along with built-in validation to ensure strong passwords and unique usernames.    
`AuthenticationForm`  A ready-to-use form that handles user login. It checks the provided username and password against the database and ensures the account is active before allowing access.    
**`login()` and `logout()`**: These are helper functions from `django.contrib.auth`. The `login()` function starts a session for the authenticated user, while `logout()` ends that session, clearing all stored session data to securely log the user out.

After we finish the views we configure the URLs for these views.   
**``accounts/urls.py``**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
```
And include this in the main project’s `urls.py`:  
**`workshop3/urls.py`**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/', include('todo_list.urls')),
    path('accounts/', include('accounts.urls')),
]
```
Now, users can register for an account, log in, and log out securely using Django’s built-in authentication system.  Once this is set up, we can link tasks to individual users so each person sees only their own to-do list.
#### Update The todo_list App
Now that authentication is set up, let’s update our **`todo_list`** app so that each user only sees and manages their own tasks. Currently, all tasks are visible to everyone we’ll fix that by linking each task to its owner.  
First, open **`todo_list/models.py`** and modify the model to include a `user` field:  
**`todo_list/models.py`**
```python 
from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```
Here we added a **foreign key** relationship to Django’s built-in `User` model, this ensures that every task is associated with a specific user, and when a user is deleted, their tasks are removed automatically (`on_delete=models.CASCADE`). we’ve also added the `related_name="tasks"` attribute to the `user` field.  
This allows us to easily access all tasks belonging to a specific user using the reverse relationship for example, `user.tasks.all()` will return all `Todo` items linked to that user.
Next, update **`todo_list/views.py`** to show only the logged-in user’s tasks and assign new ones to them:   
**``todo_list/views.py``**
```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Todo
from .forms import TodoForm

@login_required
def task_list(request):
    tasks = Todo.objects.filter(user=request.user)
    return render(request, 'todo_list/tasks.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TodoForm()
    return render(request, 'todo_list/add_task.html', {'form': form})
```
We used the **`@login_required`** decorator to make sure only authenticated users can access the task list or add new tasks. In the `task_list` view, we filter tasks using `Todo.objects.filter(user=request.user)` so that each user sees only their own.  
In the `add_task` view, we assign the logged-in user to each new task before saving it.
### Running the App
Before running the server, we first need to apply our database changes, each time we create or modify a model, Django requires us to make and apply migrations.  
In our terminal, we run the following commands:
```bash
python manage.py makemigrations # python3 for mac/linux
python manage.py migrate # python3 for mac/linux
```
These commands generate migration files based on our models and apply them to the database, once the migrations are done, start the development server using:
```bash
python manage.py runserver # python3 for mac/linux
```
After this you can register a new user, log in, and start managing your own to-do list each user will only see their own tasks.
#### Remark
If you encounter an issue while running `python manage.py makemigrations`, it usually means you already have existing task data from an older version of the app. Since your models have changed, Django doesn’t know how to update the old data.
To fix this, simply reset your database and migrations:
1. **Delete** the `db.sqlite3` file from your project root.
2. **Remove** everything inside the `migrations` folder of your `todo_list` app (except for the `__init__.py` file).
3. Then run the following commands to rebuild the database from scratch:

```bash
python manage.py makemigrations # python3 for mac/linux
python manage.py migrate # python3 for mac/linux
```
This will give you a clean start with the new model structure.
## Working with the Django Shell
We built our **to-do list app**, connected it to a database, added authentication, and made it fully functional through the browser, But sometimes, we will need to test a query, fix a record, or experiment with models without creating a new view, template, or URL every time.   
For these situations, Django gives us a powerful interactive tool: the **Django Shell**.
### What is the Django Shell?
The Django shell is an interactive Python environment that's pre-loaded with our project's settings and models. It allows us to run Python code in the context of our Django app, making it perfect for experimenting with our database, models, and other components without writing full scripts or views. We can think of it as a playground where we can query, create, update, or delete data on the fly.   
It allows you to:
- Test queries directly on your database.
- Create, read, update, or delete records easily.
- Debug model issues without running the server.
- Experiment with data or logic safely before writing actual view code.

### Starting Django Shell
To start the Django shell, we first open the terminal, navigate to our project directory (e.g., workshop3), and run the following command:
```shell
python manage.py shell  # or python3 on mac/linux
```
This opens an interactive prompt (`>>>`) with full access to our Django project.  
We can install **IPython** package (`pip install ipython`), So Django will use it automatically providing syntax highlighting and auto-completion.  
Once inside, the shell gives us access to everything in our Django project:
- Our models (e.g., Todo from todo_list).
- Django's ORM for database operations.
- Built-in utilities like authentication tools.
- Any custom functions or settings we have defined.
### Importing Models and Preparing to Work with Data
Before we can manipulate data, we will need to import the models we want to use.  
For our to-do list app:
```
>>> from todo_list.models import Todo
>>> from django.contrib.auth.models import User
```
Here, we're importing the ``Todo`` model to interact with tasks and the built-in ``User`` model since our tasks are linked to users via a foreign key. Once imported, you can use Django's ORM methods like ``.objects.all()``, ``.filter()``, or ``.create()`` to perform database operations.    
If we need to work with other parts of Django, such as forms or views, we can import those too. For example:
```
>>> from todo_list.forms import TodoForm
```
This setup allows us to test form validation or even simulate view logic directly in the shell.
### Querying and Selecting Data
One of the most common uses of the Django shell is to retrieve and inspect data from the database. Django's ORM provides a Pythonic way to query our models without writing raw SQL, making it easy to select, filter, and access specific records.
#### Basic Retrieval
To get all records from a model, use the ``.objects.all()`` manager:
```python
>>> all_tasks = Todo.objects.all()
>>> print(all_tasks)
<QuerySet [<Todo: Buy groceries>, <Todo: Finish report>]>
```
This returns a **QuerySet** a lazy collection of objects that you can iterate over or slice like a list. For example:
```python
>>> for task in all_tasks:
...     print(task.title, task.done)
Buy groceries False
Finish report True
```
Here, we loop through all the tasks and display their titles, as well as whether each one is marked as done or not. 
#### Getting Single Record
We can select a single record using `objects.get()`, by providing the task’s **ID** or **primary key (pk)** as a parameter.
```python
>>> task = Todo.objects.get(pk=1)
>>> print(task.title)
```
The  `.get()` must match exactly one record if none or multiple match, it raises an error.
#### Filtering Data
We can also filter the results for example select only tasks that are marked as done. To do this, we use `objects.filter()` and specify the attribute and value we want to filter by. For example, `Todo.objects.filter(done=True)` will return only the completed tasks.
```python
>>> done_tasks = Todo.objects.filter(done=True) # Get a specific user
```
We can also perform more complex filtering.    
For example, we can select tasks that belong to a specific user and are not marked as done yet.  
To achieve this, we combine multiple conditions inside the `filter()` method, like this:
```python
>>> user = User.objects.get(username='alice')  # Get a specific user
>>> user_tasks = Todo.objects.filter(user=user, done=False)
>>> print(user_tasks)
<QuerySet [<Todo: Buy groceries>]>
```
Here, we're filtering tasks that belong to 'alice' and are not yet done. We can chain filters or use lookups like __exact, __contains, or __gt (greater than):
```python
>>> recent_tasks = Todo.objects.filter(created_at__gt='2025-10-01')
```

### Accessing Related Data
Because our `Todo` model has a **foreign key** to `User`, we can access tasks from either direction.  
From a task we can access the user data:
```python
>>> task = Todo.objects.get(id=1)  # Get a task by its primary key
>>> print(task.user.username)  # Access the owner's username
'alice'
```
From a user by using `related_name="tasks"` we can ask all tasks that the user made:
```python
>>> user = User.objects.get(username='alice')
>>> print(user.tasks.all())  # All tasks for this user
<QuerySet [<Todo: Buy groceries>, <Todo: Schedule meeting>]>
```
This returns all tasks owned by that user a clear, readable way to handle relationships between models.
#### Advanced Querying
We can also create more advanced queries using different ORM methods.  
For instance, we can use `.exclude()` (the opposite of `.filter()`) to retrieve a set of records while excluding specific ones.  
We can also use `.order_by()` to sort our results based on certain fields, and `.values()` to get the data in a dictionary format instead of model instances.
```python
>>> sorted_tasks = Todo.objects.order_by('-created_at')  # Newest first
>>> task_dicts = Todo.objects.values('title', 'done')  # Just specific fields
>>> print(task_dicts)
<QuerySet [{'title': 'Buy groceries', 'done': False}, ...]>
```
We can also count records or check existence:
```python
>>> task_count = Todo.objects.filter(user=user).count()
>>> print(task_count)
3
>>> has_tasks = Todo.objects.filter(user=user).exists()
>>> print(has_tasks)
True
```
These querying tools make the shell ideal for verifying data integrity or debugging why certain records aren't appearing in our views.
### Creating New Records
The shell isn't just for reading data we can create new records directly using the ORM. This is useful for seeding initial data, testing model validation, or fixing issues manually, We have 2 ways to create new record
#### Method 1 Create and Save:
We simply create a new object (an instance) from the `Todo` model, set its attributes, and then use the `.save()` method to store it permanently in the database.  
```python
>>> user = User.objects.get(username='alice')
>>> new_task = Todo(title='Clean the house', description='Vacuum and dust', user=user)
>>> new_task.save()  # Commit to the database
```
This creates a Todo object in memory and saves it to the database with .save(). Django automatically handles the primary key and any default values (like created_at).
#### Method 2: Using the `.create()` Manager
We can also create and save a new record in a single step using the `.create()` method on the model’s manager. This is a convenient shortcut when we don’t need to modify the object before saving.
```python
>>> user = User.objects.get(username='alice')
>>> task = Todo.objects.create(title="Wash the car", user=user, done=False)
```
This command both **creates** the `Todo` instance and **saves** it directly to the database in one line.
#### Method 2 Bulk Creation :
If we need to add several tasks at once, we can use the `.bulk_create()` method to insert multiple records efficiently.
```python
>>> user = User.objects.get(username='alice')
>>> tasks = [
...     Todo(title="Task 1", user=user),
...     Todo(title="Task 2", user=user),
... ]
>>> Todo.objects.bulk_create(tasks)
```
This method performs all the insertions in a **single database operation**, making it much faster and more efficient when working with large datasets.
### Updating Data
Once we have data in the database, we can easily modify it using the Django shell.  
This is especially useful for quick updates like marking completed tasks, changing descriptions, or correcting mistakes without needing to use the web interface.
#### Updating a Single Instance
To update one record, we first **fetch** the object, **change its attributes**, and then **save** the changes using the `.save()` method.
```python
>>> task = Todo.objects.get(id=1)  # Fetch the task by its ID
>>> task.done = True               # Mark it as completed
>>> task.description = 'Updated description'  
>>> task.save()                    # Save the updated record
```
Here, Django only updates the fields that were modified, making the operation efficient.  this method is perfect when updating individual records or testing model behavior interactively.
#### Bulk Updates
If we want to update several records at once (for example, marking all of a user’s tasks as done), we can use the `.update()` method on a **QuerySet**.
```python
>>> Todo.objects.filter(user=user, done=False).update(done=True)
2  # Returns the number of updated rows
```
This command applies the update to **all matching records** directly in the database,  without loading each object into memory.
### Deleting Data
The Django shell also allows us to **safely remove data** from the database.  
When deleting, Django automatically respects model relationships for example, if a user is deleted, their related tasks will also be removed because of the `on_delete=models.CASCADE` option in our model.
#### Deleting a Single Instance
To delete a specific record, first retrieve it using `.get()`, then call the `.delete()` method.
```python
>>> task = Todo.objects.get(id=1)  # Fetch the task by ID
>>> task.delete()                  # Permanently delete it
(1, {'todo_list.Todo': 1})         # Returns the number of deleted objects
```
This removes the object from the database permanently. Django confirms how many objects were deleted and from which model.
#### Deleting Multiple Records
If you want to delete several records at once, use `.delete()` directly on a **QuerySet**.
```python
>>> Todo.objects.filter(done=True).delete()
(3, {'todo_list.Todo': 3})  # Deletes all completed tasks
```
This method efficiently removes all matching records without loading them into memory.
#### Deleting All Records 
To remove **every record** in the model:
```python
>>> Todo.objects.all().delete()
```
We should careful when running this command there’s no undo in the database.    
Always verify your query before executing a delete operation, especially in production environments.
### Working with Forms and Validation
Beyond manipulating data directly, the **Django shell** allows us to experiment with other components of our application such as **forms**, **authentication**, and even **settings** all without starting the web server.  
This makes it an excellent environment for testing logic, debugging issues, and exploring how different Django features behave in real time.
#### Testing Forms and Validation
With  the shell, we can test how our form behaves when given valid or invalid data.
```python
>>> form = TodoForm(data={'title': 'Invalid', 'description': ''})
>>> form.is_valid()
False
>>> print(form.errors)
{'description': ['This field is required.']} 
```
Here, we created a form instance manually and passed some data to it.  When we call `.is_valid()`, Django checks if all fields meet the model’s validation rules.    
In this example, since the description field is required but left empty, Django returns a helpful error message.  
This is very useful for testing form validation logic before integrating it into your views or templates.
#### Working with Authentication
The Django shell can also simulate authentication processes such as logging in a user.  
This is especially handy when you need to test user login behavior or verify password configurations without building a view.
```python
>>> from django.contrib.auth import authenticate
>>> user = authenticate(username='alice', password='password123')
>>> if user:
...     print("User authenticated")
```
Here, `authenticate()` checks whether the provided credentials are correct, if valid, it returns the user object; otherwise, it returns `None`.  
This is the same function Django uses behind the scenes in the login process.
#### Running Custom Queries or Raw SQL
While Django’s ORM is powerful and safe, sometimes we might need to execute **raw SQL queries** directly for example, when debugging or testing complex database behavior.
```python 
>>> for task in Todo.objects.raw('SELECT * FROM todo_list_todo WHERE done = 1'):
...     print(task.title)
```
The `.raw()` method lets you run SQL statements directly and returns model instances as results.  
This gives us low-level control over our database when needed, while still keeping Django’s model structure intact.
#### Debugging Settings or Middleware
We can also access and inspect our project’s configuration settings directly from the shell.
```python 
>>> from django.conf import settings
>>> print(settings.DATABASES)
```
This is helpful for verifying database connections, middleware settings, or environment-specific configurations without opening configuration files.
### Exiting and Cleaning Up
Once we are done experimenting, you can exit the shell in one of two ways:
- Type `exit()` and press **Enter**
- Or simply press **Ctrl + D**
#### Important Reminder  
When we use the **Django shell**, every operation we perform like creating, updating, or deleting objects directly affects our real database.   
That means if we delete all records or modify existing ones, those changes **can’t be undone** unless we restore a backup.    
For example:
```python
>>> from todo_list.models import Todo
>>> Todo.objects.all().delete()
(5, {'todo_list.Todo': 5})
```

This command will **permanently remove** all 5 tasks from our database instantly!  
There’s no confirmation message or warning like we get in the admin panel.    
So if we’re experimenting or testing new code, it’s very easy to make irreversible changes by mistake.
#### Safe Experimentation Options 
To avoid accidental data loss or unwanted changes,The safest approach is to create a temporary database just for testing.      
We can configure it in our `settings.py` like this:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
}
```
Then we run:
```shell
python manage.py migrate
```
Now we can freely test, add, or delete data in this new database without touching our real (production) data.  
When we’re done, we simply delete the `test_db.sqlite3` file and everything is clean again.
## Managing the Admin Panel
