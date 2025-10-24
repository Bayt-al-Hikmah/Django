## Objectives
- Rendering and Returning Templates
- Django Template Engine
- Managing and Serving Static Files
- Handling User Input with Forms

## Rendering and Returning Templates
In our previous session, we returned simple `HttpResponse` strings from our views. While perfect for simple tests or APIs, most web applications need to display rich, structured content. To achieve this, we use **HTML templates**.  
A template is an HTML file where we can embed dynamic data before sending it to the user's browser. This approach keeps our application's logic (written in Python) separate from its presentation (written in HTML), making our code cleaner and easier to maintain.
### Rendering Templates
When we want to render and return Html template we will use Django’s render() function to send an HTML template to the browser. The render() function combines a template with data (called a context) and generates the final HTML.
### The `templates` Folder
By default, Django looks for templates in a folder named `templates` inside each app. As a best practice, we should create a subfolder within this `templates` directory that matches the app’s name. This helps prevent template name conflicts when multiple apps contain templates with the same filename.
### Creating The App
Now, let’s put this into practice. We’ll start by creating a new Django project, then create an app named **`app1`** and configure it just like we did in Workshop One. We’ll add **`app1`** to the `INSTALLED_APPS` list, set up the URLs in both the project and the app, and make sure the app uses the **`app/`** endpoint. 
**``app1/urls.py``**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```
**``myproject/urls.py``**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app1/', include('app1.urls')),
]
```
With this setup, when we visit **`http://localhost:8000/app1/`**, Django will route the request to the **`index`** view inside **`app1`**, which renders and returns the **`index.html`** template.
Finally, we’ll create a view function that returns and renders a template called **`index.html`**.    
**``app1/view.py``**
```python
from django.shortcuts import render  

def index(request):     
	return render(request, 'app1/index.html')
```
The **`index`** function takes the request object and uses Django’s **`render()`** method to return an HTTP response containing the rendered HTML template.  
The **`render()`** function takes three main arguments:
1. **`request`** – the HTTP request object, which is required.
2. **`template_name`** – the path to the template you want to render, relative to any of the template directories.
3. **`context`** _(optional)_ – a dictionary of data you want to pass to the template.

In our case, we used **`render(request, 'app1/index.html')`**, where **`'app1/index.html'`** tells Django to look for the `index.html` file inside the **`templates/app1/`** directory of our app. This keeps our templates organized and prevents name conflicts between different apps.
### Creating The Template
Next, we’ll create our template, inside our app folder, create a folder named **`templates`**. Within this folder, create another subfolder with the same name as your app this helps avoid template conflicts. Finally, inside that subfolder, create the file **`index.html`**.     
**``app1/templates/app1/index.html``**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My First Template</title>
</head>
<body>
    <h1>Welcome to Our Website!</h1>
    <p>This page was rendered from a Django template.</p>
</body>
</html>
```
### Running The App
Now we can run our Django development server using:
```bash
python manage.py runserver
```
Once the server is running, open your browser and visit **`http://127.0.0.1:8000/app1/`**. We should see the content of our **`index.html`** template displayed on the page.
## Django Template Engine
With Django, we can do much more than just create and return static HTML templates. Django includes a powerful template engine that allows us to build dynamic and reusable pages. Using the template engine, we can insert variables, apply conditions, loop through data, and even define reusable layouts that other templates can extend.
### Adding Variables
In Django templates, we can display dynamic data passed from the view using **template variables**.  
For example, if we pass a context dictionary from our view like this:  
**`app1/views.py`**
```python
from django.shortcuts import render

def index(request):
    context = {
        'username': 'Alice',
        'age': 25
    }
    return render(request, 'app1/index.html', context)
```
Here, we updated our **`index`** view to include a **`context`** dictionary that holds dynamic data in this case, the username and age. This context is passed to the **`render()`** function, which makes the data available inside the **`index.html`** template, allowing us to display personalized information on the page.
We can then access these variables directly in our template using double curly braces (`{{ }}`):
**`app1/templates/app1/index.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My First Template</title>
</head>
<body>
    <h1>Welcome {{username}}!</h1>
    <p>You are {{ age }} years old.</p>
</body>
</html>
```
When rendered, Django replaces these variables with the actual values from the context.
### Using Conditions
The Django Template Engine also allows us to add **conditions** to our HTML templates, making our pages more dynamic and responsive to data.  
We can use **conditional statements** such as **`if`**, **`elif`**, and **`else`** to control what content is displayed based on specific conditions.
#### Example
Now, let’s create a new app called **`app2`**. We’ll configure it, set up its URLs, and add it to the **`INSTALLED_APPS`** list.  
**`app2/urls.py`**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('<str:role>/', views.index, name='index'),
]
```
After that, we’ll configure the **`views.py`** file to display different messages based on the **dynamic URL** the user visits.
**``app2/views.py``**
```python
from django.shortcuts import render  

def index(request,role):     
	return render(request, 'app2/index.html',{
		"role":role})

```
After that lets create our template and display deff message depend on the role that is provided on the dynamic dynamic url   
**``app2/templates/app2/index.html``**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>App 2</title>
</head>
<body>
    {% if role == 'admin' %}
        <h1>Welcome, Admin!</h1>
        <p>You have full access to the system.</p>
    {% elif role == 'editor' %}
        <h1>Welcome, Editor!</h1>
        <p>You can edit and manage content.</p>
    {% elif role == 'viewer' %}
        <h1>Welcome, Viewer!</h1>
        <p>You can browse and read the available content.</p>
    {% else %}
        <h1>Welcome, Guest!</h1>
        <p>Your role is not recognized. Please log in or contact the administrator.</p>
    {% endif %}
</body>
</html>
```
Here we using  Django’s **`if`**, **`elif`**, and **`else`** tags to display different messages based on the value of the **`role`** variable passed from the view.  
When a user visits a URL like `/app2/admin/` or `/app2/viewer/`, Django will render the appropriate message dynamically.
### Using Loops
The Django Template Engine also allows us to **loop through data** in our HTML templates. This is especially useful when we need to display lists, tables, or collections of items dynamically, such as a list of users, products, or posts.  
We can use the **`for`** tag to iterate over data passed from our view.
#### Example
Now, let’s create a new app called **`app3`**. We’ll configure it, set up its URLs, and add it to the **`INSTALLED_APPS`** list.  
**`app3/urls.py`**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```
Next, we’ll configure the **`views.py`** file to pass a list of items to our template.  
**`app3/views.py`**
```python
from django.shortcuts import render  

def index(request):     
    context = {
        'fruits': ['Apple', 'Banana', 'Cherry', 'Mango', 'Orange']
    }
    return render(request, 'app3/index.html', context)
```
Now let’s create our template and display the list dynamically using a loop.   
**``app3/templates/app3/index.html``**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>App 3 - Using Loops</title>
</head>
<body>
    <h1>Available Fruits</h1>
    <ul>
        {% for fruit in fruits %}
            <li>{{ fruit }}</li>
        {% empty %}
            <li>No fruits available at the moment.</li>
        {% endfor %}
    </ul>

    <p>Total fruits: {{ fruits|length }}</p>
</body>
</html>
```
Here, we’re using the Django **`for`** tag to loop through each item in the **`fruits`** list and display it as a list item.  
We also added the **`{% empty %}`** tag, which defines what should be shown if the list is empty in this case, it displays a message saying _“No fruits available at the moment.”_  
Finally, we used the **`length`** filter to display the total number of fruits.  
When we run the server and visit **`http://127.0.0.1:8000/app3/`**, Django will render the page and show the fruit list dynamically or the empty message if no items are available.
### Template Inheritance (Base Layouts)
In larger projects, many pages share the same layout such as a common header, navigation bar, or footer.  
Instead of repeating HTML code across multiple templates, Django allows us to create a **base layout** and let other templates **extend** it.  
This approach keeps our templates clean, organized, and easier to maintain.  
**`app1/templates/app1/base.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>App 1</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```
In this file, we define a **block** called **`content`** using the `{% block %}{% endblock %}` tags.  
This block acts as a **placeholder** it tells Django, Other templates that extend this one can insert their content here.    
**`app1/templates/app1/index.html`**
```html
{% extends 'app1/base.html' %}
{% block content %}
    <h2>Welcome to the Home Page!</h2>
    <p>This content is unique to the index page.</p>
{% endblock %}
```
The `{% extends 'app1/base.html' %}` tag tells Django that this template is built on top of the base layout. Django first loads the base template and then replaces the `{% block content %}` section with the HTML defined in the extending file. As a result, the final rendered page combines both templates the layout from **`base.html`** and the page-specific content from **`index.html`**.    
This mechanism makes it easy to maintain a consistent layout across our site while allowing each page to display unique content where needed.
### Including Template Parts (Reusable Components)
Django also allows us to include smaller parts of a layout, similar to using components in modern frameworks.  
For example, we can create separate templates for elements like the **navigation bar**, **footer**, or **sidebar**, and include them in multiple pages using the **`{% include %}`** tag.
We’ll start by creating a folder called **`components`** inside the **`app1/templates/app1/`** directory.  
In this folder, we’ll place our reusable components such as the **navbar** and **footer**.  
**`app1/templates/app1/components/navbar.html`**
```html
<nav>
    <a href="#">Home</a> |
    <a href="#">About</a> |
    <a href="#">Contact</a>
</nav>
```
Next, let’s create our footer component.  
**`app1/templates/app1/components/footer.html`**
```html
<footer>
    <p>&copy; 2025 My Website</p>
</footer>
```
We can then include both the navbar and the footer in any other template.  
A common practice is to include them in the **`base.html`** layout so that all templates extending it automatically display these shared components.
**`app1/templates/app1/base.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>App 1</title>
</head>
<body>
    <header>
        <h1>My Website</h1>
        {% include 'app1/components/navbar.html' %}
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    {% include 'app1/components/footer.html' %}
</body>
</html>
```
Here, the **`{% include 'app1/components/navbar.html' %}`** and **`{% include 'app1/components/footer.html' %}`** tags tell Django to load and render these templates at the specified locations.  
This component-based approach helps keep your templates **modular**, **clean**, and **easy to maintain**, especially as your project grows in complexity.

## Managing and Serving Static Files

The Django Template Engine helps us build dynamic templates that change depending on the provided data.  
However, real web applications also need **styles**, **images**, and sometimes **videos** to enhance the user experience, These files which don’t change dynamically are called **static files**.   
Django provides a simple and efficient way to manage and serve these static files, such as **CSS**, **JavaScript**, and **images**, directly from each app’s directory.
### Setting Up Static Files in an App
Let’s create a new app called **`app4`** to demonstrate how Django handles static files, Inside **`app4`**, we’ll create a folder structure to organize our static assets such as CSS, JavaScript, and images.   
We place these files inside a folder named **`static/app4/`** so Django can easily locate them when rendering pages.  
Using the app’s name (**`app4`**) inside the **`static`** folder helps prevent conflicts if other apps use files with similar names (for example, multiple apps having a `style.css` file).  
**Folder structure:**
```
app4/
│
├── static/
│   └── app4/
│       ├── css/
│       │   └── style.css
│       └── images/
│           └── logo.png
│
└── templates/
    └── app4/
        └── index.html
```
### Creating Styles file
Next, let’s create a **CSS file** that will define the styles for our page.  
We’ll name it **`style.css`** and place it inside the **`app4/static/app4/css/`** folder.  
**`app4/static/app4/css/style.css`**
```css
body {
    font-family: Arial, sans-serif;
    background-color: #f9f9f9;
    text-align: center;
    margin: 50px;
}

h1 {
    color: #2c3e50;
}

img {
    width: 150px;
    margin-top: 20px;
}
```
This stylesheet controls the appearance of our webpage it sets a clean background, centers the content, and styles the heading and image for a simple, modern look.
### Building the Template
Now that our static files are properly set up, it’s time to use them in a Django template. We’ll create a simple page that loads a CSS stylesheet to style our content and displays an image from our static folder. This will help us understand how Django connects HTML templates with static resources such as images, stylesheets, and JavaScript files.  
**`app4/templates/app4/index.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>App 4 - Static Files</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'app4/css/style.css' %}">
</head>
<body>
    <h1>Welcome to App 4</h1>
    <p>This page demonstrates how to use static files in Django.</p>
    <img src="{% static 'app4/images/logo.png' %}" alt="App 4 Logo">
</body>
</html>
```
In this template, we start by loading Django’s **static template tag** with `{% load static %}`. This line tells Django that we plan to use static files inside this HTML document. Without it, Django wouldn’t know how to interpret the `{% static %}` statements that follow.

Next, we use the `{% static %}` function to reference our CSS file and image. Django replaces these template tags with the actual file paths at runtime. This means we don’t have to manually type the full URL or worry about where the files are stored Django takes care of it automatically.  
For example, the line
```html
<link rel="stylesheet" href="{% static 'app4/css/style.css' %}">
```
tells Django to load the `style.css` file located in the `app4/static/app4/css/` folder. Similarly, the image tag
```html
<img src="{% static 'app4/images/logo.png' %}" alt="App 4 Logo">
```
instructs Django to display the logo image from the same static directory.  
When you open this page in your browser, Django will render the HTML and replace each `{% static %}` tag with the correct URL path for the file. As a result, your styles will be applied, and the logo image will appear correctly.

### Creating the View
Now that we’ve built our template and static files, let’s connect everything through a Django view. A view in Django is responsible for receiving a request, processing any necessary logic, and returning a response usually an HTML page. In our case, the view will simply render the **`index.html`** template we just created.  
**`app4/views.py`**
```python
from django.shortcuts import render  

def index(request):     
    return render(request, 'app4/index.html')
```
### Configuring URLs
To make our view accessible through the browser, we need to define a URL pattern for it. Each Django app can have its own **`urls.py`** file, where we map specific URLs to views.  
**`app4/urls.py`**
```python 
from django.urls import path
from . import views  

urlpatterns = [     
    path('', views.index, name='index'), 
]
```
Here, we’ve mapped the root URL of **`app4`** (`''`) to the **`index`** view. This means that when someone visits `/app4/` in their browser, Django will automatically call the **`index()`** function and render the associated template.  

Next, we need to include this app’s URL configuration inside the main project’s URL configuration so that Django knows where to look when a user visits the `/app4/` route.  
**`myproject/urls.py`**
```python
from django.contrib import admin  
from django.urls import path, include  

urlpatterns = [     
    path('admin/', admin.site.urls),     
    path("app1/",include("app1.urls")),
    path("app2/",include("app2.urls")),
    path("app3/",include("app3.urls")),
    path('app4/', include('app4.urls')), 
]
```
By using the **`include()`** function, we’re telling Django to look for additional URL patterns inside the **`app4`** app. 
Finally, we add **`app4`** to our **`INSTALLED_APPS`** section inside **`settings.py`**. This step ensures that Django recognizes the app and knows where to find its templates and static files.
## Handling User Input with Forms
So far, our Django apps have focused on **displaying data** to users rendering templates, managing static files, and serving dynamic content. However, real-world web applications do much more than that. They also need to receive data from users, process it, and often save it or use it to produce a result.  
The most common way to collect user input in web applications is through HTML forms. Django provides robust support for handling forms from basic HTML forms to advanced Django Form classes that simplify validation and data handling.
### Create a Feedback App
Let’s create a new app called **`feedback`** that allows users to submit their feedback and enables us to store and view these submissions.  
First, create the app using this command:
```
python manage.py startapp feedback
```
Then, open **`settings.py`** and add `'feedback'` to the `INSTALLED_APPS` list:
**``myproject/setting.py``**
```python
INSTALLED_APPS = [
	'app1',
	'app2',
	'app3',
	'app4',
	'feedback',  # Added feedback app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
### Creating The Template
After setting up our app, it’s time to create the **templates** that will handle user interaction and data display.  
We’ll need **two templates**:
1. One for the feedback form, where users can submit their feedback.
2. Another for displaying submitted feedback

**feedback/templates/feedback/form.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Submit Feedback</title>
</head>
<body>
    <h1>We Value Your Feedback</h1>

    <form method="POST">
        <input type="text" name="name" placeholder="Your Name" required><br><br>
        <input type="email" name="email" placeholder="Your Email" required><br><br>
        <textarea name="message" rows="5" placeholder="Your Feedback" required></textarea><br><br>
        <button type="submit">Submit</button>
    </form>

</body>
</html>
```
This template displays a simple HTML form where users can enter their **name**, **email**, and **message**.   
When the user submits the form, the data will be sent to the server using the **POST** method and handled by our Django view.   
**feedback/templates/feedback/feedbacks.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Client Feedback</title>
</head>
<body>
    <h1>Submitted Feedback</h1>
        <ul>
            {% for item in feedback_list %}
                <li>
                    <strong>{{ item.name }}</strong> ({{ item.email }})<br>
                    {{ item.message }}<br>
                    <small>Submitted on {{ item.created_at }}</small>
                </li>
                <hr>
            {% empty %}
            <li>No feedback has been submitted yet.</li>
            {% endfor %}
        </ul>
</body>
</html>
```
This template loops through the list of submitted feedback entries using Django’s **`for`** tag.  
For each feedback item, it displays the **name**, **email**, **message**, and **submission date**.  
If no feedback has been submitted, the **`{% empty %}`** tag displays a message saying “No feedback has been submitted yet.”

### Creating the view logic
Now that we’ve created our templates, it’s time to define the view logic .
Our view will perform two main tasks:
1. **Display the feedback form** so users can submit their feedback.
2. **Display all submitted feedback** stored in the database.

**``feedback/views.py``**
```python
from django.shortcuts import render, redirect

feedbacks = []
def submit_feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        feedbacks.append({"name":name,"email":email,"message":message})
        return redirect('feedbacks')  
    return render(request, 'feedback/form.html')

def feedback_list(request):
    return render(request, 'feedback/feedbacks.html', {'feedback_list': feedbacks})
```
Here we’re using a simple in-memory list called `feedbacks` to temporarily store submitted feedback instead of saving it to a database.
- The **`submit_feedback`** function checks if the request is a **POST** request.
    - If it is, it retrieves the form data (`name`, `email`, and `message`) using `request.POST.get()`, adds it to the `feedbacks` list, and then redirects the user to the feedback list page.
    - If the request is a **GET**, it simply displays the feedback form.
- The **`feedback_list`** function renders the `feedbacks.html` template and passes the `feedbacks` list so all submitted feedback can be displayed.
### Setting the URLs Pattern
Finally, we need to configure the **URL patterns** for our feedback app.  
In our case, we’ll create two routes:
1. One for submitting new feedback.
2. Another for displaying all submitted feedback.

**`feedback/urls.py`**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_feedback, name='submit_feedback'),
    path('feedbacks/', views.feedback_list, name='feedbacks'),
]
```
Finally, we include this app’s URL configuration in our main project’s `urls.py` file so Django knows where to find these routes.
**`project/urls.py`**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # The other apps
    #..
    path('feedback/', include('feedback.urls')),
]

```
Now when we visit:
- **`http://127.0.0.1:8000/feedback/`** we will see the feedback form.
- **`http://127.0.0.1:8000/feedback/feedbacks/`** we will see all submitted feedback displayed dynamically.

If we try to submit our form right now, our application will **crash with a “CSRF verification failed” error**.  
This happens because Django, by default, enables **CSRF protection** for all POST requests.  
You can confirm this by checking the **`MIDDLEWARE`** list in your `settings.py` file one of the middlewares listed is:
```python
'django.middleware.csrf.CsrfViewMiddleware',
```
This middleware helps protect our app from a common web security threat called **Cross-Site Request Forgery (CSRF)**.
### What Is CSRF?
**CSRF (Cross-Site Request Forgery)** is a type of attack where a malicious website tricks a logged-in user into performing unwanted actions on another website where they’re authenticated.  
For example, without CSRF protection, a hacker could create a hidden form on another site that automatically submits data to your app possibly changing user settings or posting messages without the user’s consent.  
Django includes built-in CSRF protection to prevent this by requiring a **unique token** to be sent with every form submission.  
If the token is missing or invalid, Django rejects the request
### Adding the CSRF Token
To fix our form and make it work safely, we need to include a CSRF token in our HTML form.  
We do this by adding `{% csrf_token %}` inside the `<form>` tag.  
Edit **`feedback/templates/feedback/form.html`** like this:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Submit Feedback</title>
</head>
<body>
    <h1>We Value Your Feedback</h1>

    <form method="POST">
        {% csrf_token %}
        <input type="text" name="name" placeholder="Your Name" required>
        <input type="email" name="email" placeholder="Your Email" required>
        <textarea name="message" placeholder="Your Feedback" required></textarea>
        <button type="submit">Submit</button>
    </form>

</body>
</html>
```
Now, when we submit the form, Django will verify the CSRF token and safely accept our feedback without errors.
### Using Django Form
Our app works, but the current form lacks **validation** and can easily accept empty or invalid inputs.  
To solve this, Django provides a more powerful and structured way to handle forms — using the **Django Form** class.  
Django Forms help you:
- Automatically **validate** user input (e.g., check required fields, valid emails, etc.).
- Re-render the form with error messages when validation fails.
- Cleanly separate form logic from your templates.
### Creating a Django Form
We’ll begin by creating a new file named **`forms.py`** inside our **`feedback`** app. This file will contain the form class responsible for collecting and validating user input.  
**``feedback/forms.py``**
```python
from django import forms

class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Your Email")
    message = forms.CharField(widget=forms.Textarea, label="Your Feedback")

```
This defines a **Django Form** with built-in validation features.
- The **`CharField`** and **`EmailField`** automatically ensure that users provide valid data.
- The **`widget=forms.Textarea`** makes the `message` field appear as a multi-line text box in the form.
### Updating the View Logic
Now let’s update our **`views.py`** file to use this form instead of handling raw POST data.  
**`feedback/views.py`**
```python
from django.shortcuts import render, redirect
from .forms import FeedbackForm
from django.urls import reverse
feedbacks = []
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedbacks.append(form.cleaned_data)
            return redirect(reverse('feedback'))
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/form.html', {'form': form})

def feedback_list(request):
    return render(request, 'feedback/feedbacks.html', {'feedback_list': feedbacks})
```
In the **first view (`submit_feedback`)**, we import our **`FeedbackForm`** and use it to handle form submissions instead of manually processing POST data. When a user submits the form, Django automatically validates the input using the `form.is_valid()` method. If the submitted data passes all validation checks, we safely access the cleaned and verified input through `form.cleaned_data`, store it in the `feedbacks` list, and then redirect the user to the feedback page using `redirect(reverse('feedbacks'))` so they can see their submission along with others.   
The `reverse()` function helps us generate URLs dynamically based on the URL name defined in `urls.py`. This is better than hardcoding URLs directly in our views or templates, as it makes the code more maintainable and less error-prone when URL patterns change.   
If the form is **not valid**, Django automatically attaches error messages to the specific fields that failed validation. Since we pass the `form` back to the template, these errors are displayed directly on the page, clearly showing the user what needs to be corrected before resubmitting.  
If the request is not a POST request (for example, when a user first visits the page), an empty form instance is created and displayed. Finally, the `render()` function loads the appropriate template and passes the form as context data. This approach keeps the code cleaner, safer, and more user-friendly while taking full advantage of Django’s built-in form validation and error-handling system.  
In the **second view (`feedback_list`)**, we simply load the template and pass the list of all stored feedback items as context. This allows the template to dynamically display every submitted feedback entry on the page.
### Updating the Template
Finally, let’s edit our form template to use Django’s built-in form rendering.  
**`feedback/templates/feedback/form.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Submit Feedback</title>
</head>
<body>
    <h1>We Value Your Feedback</h1>

    <form method="POST">
        {% csrf_token %}
        {{ form.as_div }}
        <button type="submit">Submit</button>
    </form>

</body>
</html>
```
Finally in our template we include the form inside a `<form>` element and add the `{% csrf_token %}` tag to protect against Cross-Site Request Forgery attacks.  
The line `{{ form.as_div }}` tells Django to automatically render all the form fields wrapped in `<div>` elements, this approach saves time, ensures proper formatting, and automatically includes validation error messages when the form is re-rendered after invalid input.
#### Remarque
Django also supports other rendering methods such as `{{ form.as_p }}` (which wraps fields in paragraphs) or `{{ form.as_table }}` (which displays them in a table layout).