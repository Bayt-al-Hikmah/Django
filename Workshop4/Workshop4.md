## Objectives

- Upload and manage files efficiently
- Work with settings files and project configuration
- Understand middleware and learn how to create custom middleware
- Implement testing and unit tests to ensure code quality
## Upload and Manage Files Efficiently
### Introduction
In modern web applications, allowing users to upload files—such as images, documents, or other media is a common requirement. Whether it’s profile pictures, project files, or shared resources, file uploads add interactivity and functionality to your app. However, handling file uploads in a web application introduces challenges like storage management, security, and performance optimization. Django provides a robust and secure framework for managing file uploads, making it easier to integrate this feature into your projects.  
We’ll explore how to configure Django to handle file uploads, discuss best practices for secure and efficient file management, and build a simple image-sharing app as an example. We’ll also cover how to manage URLs effectively using Django’s app_name to avoid naming conflicts and how to work with dynamic URLs using parameters and the reverse function for cleaner, more maintainable code.

### Configuration for File Uploads
To enable file uploads in a Django project, we need to configure our project to handle media files, as these are user-uploaded files distinct from static files (like CSS or JavaScript).   
Below are the key steps to configure Django for file uploads:
#### Updating settings.py
We need to **edit the `settings.py` file** to enable file uploads in our Django project.  
To do this, we use the `MEDIA_ROOT` and `MEDIA_URL` settings, which tell Django **where** to store uploaded files and **how** to serve them to users.  
- **`MEDIA_ROOT`**: The absolute filesystem path on the server where uploaded files are stored.
- **`MEDIA_URL`**: The base URL that allows users to access these files through the browser.

```python
# workshop4/settings.py

# Define where uploaded files will be stored
MEDIA_ROOT = BASE_DIR / 'media'

# URL to access uploaded files
MEDIA_URL = '/media/'
```
- `BASE_DIR / 'media'`  Creates a folder named `media` in your project’s root directory to store uploaded files.
- `MEDIA_URL = '/media/'` Makes uploaded files accessible through URLs that start with `/media/`, 

For example:
  ```
http://127.0.0.1:8000/media/myphoto.jpg
  ```  
#### Updating urls.py
Next, we need to **include the URL patterns** that will serve the uploaded files in our project’s `urls.py` file.
```python 
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Add other app URLs here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
Here we are appending additional URL patterns to serve uploaded media files during development. This tells Django to use the `MEDIA_URL` path (e.g., `/media/`) and serve files stored in the `MEDIA_ROOT` directory.  
The `static()` function is a helper provided by Django that makes it easy to serve media files when running the development server (`python manage.py runserver`). It automatically maps the media URLs to the correct file locations so that uploaded files can be displayed in the browser.  
However, this setup is intended **only for development**. In a **production environment**, Django should not handle file serving directly. Instead, we should configure a dedicated web server such as **Nginx** or **Apache** to serve our media files efficiently and securely.
### Building an Image Sharing App
To put this into practice, we’ll create a simple **Image Sharing App** that allows users to upload and view images.  
Each uploaded image will include a title and display on a gallery page.   
#### Createing a New Django App
First, let's create a new project for this workshop, inside it create the new ``image_share`` app
```bash
django-admin startproject workshop4
cd workshop4
python manage.py startapp image_share # python3 for mac/linux
```
After this we open `workshop4/settings.py` and add the app to the `INSTALLED_APPS` list:
```python
INSTALLED_APPS = [     
	'image_share',     
	'django.contrib.admin',     
	'django.contrib.auth',     
	'django.contrib.contenttypes',     
	'django.contrib.sessions',     
	'django.contrib.messages',     
	'django.contrib.staticfiles', 
]
```
#### Create the Photo Model
Lets create simple model for our app that store the uploaded images
**``image_share/models.py``**
```python
from django.db import models  

class Photo(models.Model):     
	title = models.CharField(max_length=100)     
	image = models.ImageField(upload_to='uploads/')     
	uploaded_at = models.DateTimeField(auto_now_add=True)   
	   
	def __str__(self):         
		return self.title
```
In this model, we define three main fields. The **`title`** field is a `CharField` that stores a short descriptive name for the uploaded photo, limited to 100 characters. The **`image`** field is an `ImageField` that handles image uploads. The argument `upload_to='uploads/'` tells Django to store uploaded files inside a subdirectory named **`uploads`** within the `MEDIA_ROOT` directory. The **`uploaded_at`** field is a `DateTimeField` with `auto_now_add=True`, which automatically saves the date and time when the photo was uploaded.  
The `__str__()` method returns the photo’s title whenever the object is displayed (for example, in the Django admin panel), making it easier to identify records by name instead of by their ID.  
When handling files, Django provides two main model field types. The **`FileField`** is used for general file uploads such as PDFs, text documents, or any non-image files. The **`ImageField`**, which we used here, is a specialized field for images. It includes automatic validation to ensure that the uploaded file is a valid image format, such as JPEG or PNG.   
Before using the **`ImageField`**, we need to install an additional package called **Pillow**, this library allows Django to handle image files properly. Without it, we will encounter an error when trying to create migrations or upload images.
```shell
pip install Pillow #pip3 for mac/linux
```
We apply the migrations:
```shell
python manage.py makemigrations #python3 for mac/linux
python manage.py migrate #python3 for mac/linux
```
#### Creating the Upload Form
Now, let’s create a form that handles image uploads.  
**``image_share/forms.py``**
```python
from django import forms 
from .models import Photo  

class PhotoForm(forms.ModelForm):     
	class Meta:         
		model = Photo         
		fields = ['title', 'image']
```
This form  automatically generates form fields based on the `Photo` model. In this case, it creates a text input for the **title** and a file picker for the **image**.
#### Creating the Views
Next, we’ll create the views that handle displaying uploaded images and managing new uploads.  
`image_share/views.py`
```python
from django.shortcuts import render, redirect
from .models import Photo
from .forms import PhotoForm
from django.urls import reverse  

def gallery(request):    
    photos = Photo.objects.all().order_by('-uploaded_at')    
    return render(request, 'image_share/gallery.html', {'photos': photos})  

def upload_photo(request):    
    if request.method == 'POST':        
        form = PhotoForm(request.POST, request.FILES)        
        if form.is_valid():            
            form.save()            
            return redirect(reverse('gallery'))    
    else:        
        form = PhotoForm()    
    return render(request, 'image_share/upload.html', {'form': form})
```
The **`gallery`** view retrieves all uploaded photos from the database, ordered by upload date (newest first), and passes them to the `gallery.html` template for display.  
The **`upload_photo`** view handles both displaying the upload form and processing submitted data. When a `POST` request is sent, it reads both the form data (`request.POST`) and the uploaded file (`request.FILES`). If the form is valid, the new photo is saved and the user is redirected back to the gallery page. Otherwise, it simply renders the empty form for new uploads.
#### Creating the Templates
After we finished our views , let’s create the templates to display the uploaded images and the upload form. These templates will define the structure and layout of our web pages.   
**`image_share/templates/image_share/gallery.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Photo Gallery</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'image_share/css/style.css' %}">
</head>
<body>
    <h1>Photo Gallery</h1>
    <a href="{% url 'upload_photo' %}" class="btn">Upload New Photo</a>

    <div class="gallery">
        {% for photo in photos %}
            <div class="photo-card">
                <img src="{{ photo.image.url }}" alt="{{ photo.title }}">
                <p>{{ photo.title }}</p>
                <small>Uploaded at: {{ photo.uploaded_at|date:"Y-m-d H:i" }}</small>
            </div>
        {% empty %}
            <p>No photos uploaded yet.</p>
        {% endfor %}
    </div>
</body>
</html>
```
**`image_share/templates/image_share/upload.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload Photo</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'image_share/css/style.css' %}">
</head>
<body>
    <h1>Upload a New Photo</h1>

    <form method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn">Upload</button>
    </form>

    <a href="{% url 'gallery' %}" class="btn">Back to Gallery</a>
</body>
</html>
```
The style file used here can be found inside the **`material` folder** attached to the workshop. It contains predefined styles for buttons, layouts, and the gallery grid to keep your pages visually consistent.
#### Configuring the settings.py 
Before Django can handle uploaded files, we need to configure where those files will be stored and how they can be accessed. This is done by adding **media settings** to the `settings.py` file.    
We go to  **`settings.py`** file and add the following lines near the bottom:
```python
MEDIA_ROOT = BASE_DIR / 'media' 
MEDIA_URL = '/media/'
```
The **`MEDIA_ROOT`** variable defines the **absolute path** on your server where uploaded files will be stored. In this case, it creates a folder named `media` inside your project’s base directory.  
The **`MEDIA_URL`** variable specifies the **URL prefix** that will be used to access these uploaded files from the browser. For example, if you upload an image named `photo.jpg`, it will be available at:
#### Configuring the Urls
#### Configuring the URLs

Finally, we need to set up the **URL configurations** for our app so Django knows how to route requests to the correct views.   
First, create a new **`urls.py`** file inside your app folder (`image_share/urls.py`) if it doesn’t already exist. Then, add the following code:   
**``image_share/urls.py``**
```python
# image_share/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('upload/', views.upload_photo, name='upload_photo'),
]
```
This file defines two routes:
- The root path (`''`) displays the **gallery** view that shows all uploaded photos.
- The `'upload/'` path handles the **upload form**, allowing users to add new photos.

Next, we need to include these URLs in the **main project’s URL configuration** (`workshop4/urls.py`).  
We also need to configure Django to serve uploaded media files during development.    
**`workshop4/urls.py`**
```python
# workshop4/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('image_share.urls')),  # Include app URLs
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```
Now, if we run the development server using the command below:
```shell
python manage.py runserver #python3 for mac/linux 
```
and open the browser at **`http://127.0.0.1:8000/`**, we’ll see the **photo gallery page**.  
From there, we can click on **“Upload New Photo”** to go to the upload form, select an image, and submit it.  
After uploading, Django will automatically save the image inside the **`media/uploads/`** folder, and it will instantly appear in the gallery view.  
This confirms that our file upload system, URL routing, and media configuration are all working correctly.
## Project Configuration
In the previous sections, we built applications using Django's default settings. While these defaults are excellent for getting started, real-world projects often require more specific configurations.   
We will see how to customize your Django project's settings to manage **static files**, connect to different **databases**, centralize **templates**, and implement advanced **URL routing** with namespaces and dynamic parameters.
### Static Files Configuration
While `MEDIA` files are uploaded by users, **`STATIC`** files are the assets we provide as part of our application's design, such as CSS, JavaScript, and site logos.  
By default, Django looks for static files inside a `static/` folder within each app (e.g., `image_share/static/image_share/css/style.css`). This structure is great for reusable apps, but for project-wide assets like a main stylesheet or logo, it's often cleaner to use a **centralized static directory**. We can configure this in our project's **`settings.py`** file. By adding our central folder's path to the **`STATICFILES_DIRS`** list, we tell Django to look for static files in that location _in addition_ to the app-specific folders.  

```python
import os 

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles' 

STATICFILES_DIRS = [
    BASE_DIR / 'static', 
]
```
**`STATIC_URL`** defines the base URL path through which static files are accessed in the browser, for example, if we have a CSS file named `style.css`, it will be available at: `http://127.0.0.1:8000/static/style.css`   

**`STATIC_ROOT`:** This is the single **destination** folder where all static files are copied when we run `python manage.py collectstatic`. This folder is only used for production. Our web server (like Nginx or Apache) is then configured to serve all files from this single, optimized directory.

**`STATICFILES_DIRS`** This is a list of **source** folders where Django looks for static files, _in addition_ to the `static/` folder inside each app.   
- **In development:** `runserver` finds and serves files from these folders on the fly.
- **For production:** `collectstatic` uses this list to find files to copy.
#### Example
To illustrate this, let's consider a new project with an app called `blog`.
With this configuration, we can use a **hybrid approach** for our static files:  
1. We create a single `static/` folder at the top level of our project (at the same level as our `blog` app). We use this folder for **project-wide** assets, such as the general `style.css` or `logo.png` that are shared across all apps.  
2. We can still place static files that are **specific** to an app inside that app's static folder (e.g., `blog/static/blog/blog_posts.css`).

Next, we update our `settings.py` to tell Django about this new central folder by adding its path to the **`STATICFILES_DIRS`** list:
```python
import os 

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles' 

STATICFILES_DIRS = [
    BASE_DIR / 'static', 
]
```
Now, in our templates, we can directly reference files from this central `static` folder. We no longer need to include the app name in the path.
```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<link rel="stylesheet" href="{% static 'blog/css/blog_posts.css' %}">
```
### Templates Configuration
Similar to static files, Django's default setting is to look for templates inside a `templates/` folder within each installed app (e.g., `image_share/templates/image_share/gallery.html`).  
The repetition of the app name (`templates/image_share/`) is intentional. It creates a "namespace" for the templates, so if you have two apps with a `gallery.html` file, Django can tell them apart.  
However, for some projects, it's simpler to have one central `templates` folder for the entire project, this will make it easier to share layout and compenont.   
To apply this we modify the `TEMPLATES` setting in `workshop4/settings.py`:
```python
# workshop4/settings.py  
TEMPLATES = [     
	{         
	'BACKEND': 'django.template.backends.django.DjangoTemplates',         
	'DIRS': [BASE_DIR / 'templates'],  
	# Add global templates directory         
	'APP_DIRS': True,         
	'OPTIONS': {             
		'context_processors': [                 
			'django.template.context_processors.debug',                
			'django.template.context_processors.request',                
			'django.contrib.auth.context_processors.auth',                
			'django.contrib.messages.context_processors.messages',             
		],         
	},     
	}, 
]
```
**`'DIRS': [BASE_DIR / 'templates']`**: This is the key change. It's a list of **source** folders where Django will look for templates, in addition to the app-specific folders. We've added our main project-level `templates/` directory here.     
**`'APP_DIRS': True`**: By keeping this `True`, we get the best of both worlds. Django will _first_ look in the folders defined in `DIRS` (our central folder) and _then_ look inside each app's `templates/` folder
#### Example
To illustrate this, let's make our  `blog` take layout from ``base.html`` inside this centralized folder.
We'll create a single `templates/` folder at the top level of our project, at the same level as our `blog` app folder. Inside it, we can place a shared layout file.
```
my_project/
├── manage.py
├── blog/
├── my_project/
│   └── settings.py
└── templates/  <-- Our new central folder
	└── base.html
```
After configuring `settings.py` as shown above, any template in any app can now directly extend `base.html`.  
In a template like `blog/templates/blog/post_list.html`, we can now write:
```
{% extends "base.html" %}

{% block content %}
    {% endblock %}
```
This works perfectly, even though `base.html` is not inside the `blog` app. This makes sharing layouts simple and clean.


---

### Database Configuration
By default, Django uses SQLite, a lightweight, file-based database suitable for development. However, for production or more complex projects, we mostly use more robust database like PostgreSQL or MySQL. Django’s ORM supports multiple database backends, making it easy to switch with minimal code changes.
#### SQLite Configuration
When we first create a Django project, it comes pre-configured with this `DATABASES` setting:
```python
DATABASES = {     
	'default': {         
		'ENGINE': 'django.db.backends.sqlite3',         
		'NAME': BASE_DIR / 'db.sqlite3',     
	} 
}
```
**`ENGINE`**: This tells Django to use its built-in backend for **SQLite 3**.       
**`NAME`**: Unlike server-based databases (like PostgreSQL or MySQL) that require a database name, SQLite stores the entire database in a single file. This line tells Django to create and use a file named `db.sqlite3` right in our project's main directory (`BASE_DIR`).
#### PostgreSQL Configuration
Before Django can communicate with a PostgreSQL database, it needs a **database driver**. `psycopg2-binary` is the most popular Python package that acts as this bridge, allowing Django's ORM (Object-Relational Mapper) to translate Python code into PostgreSQL queries and understand the results.   
First, install the driver:
```
pip install psycopg2-binary # pip3 for mac/linux
```
After this, we change the `DATABASES` dictionary inside the `settings.py` file so we can log in to our database:
```python
DATABASES = {     
	'default': {         
		'ENGINE': 'django.db.backends.postgresql',         
		'NAME': 'workshop_db',         
		'USER': 'postgres',         
		'PASSWORD': 'mypassword',         
		'HOST': 'localhost',         
		'PORT': '5432',     
		} 
	}
```
**`ENGINE`**: This tells Django which database backend to use. `'django.db.backends.postgresql'` is the official Django backend for PostgreSQL, which relies on the `psycopg2-binary` package we installed.      
**`NAME`**: The name of the specific database we want Django to use. We must create this database (named `workshop_db` in this example) inside our PostgreSQL server before we can run `python manage.py migrate`.    
**`USER`**: The username that Django will use to log in to the PostgreSQL server. (`'postgres'` is the default administrator, but for security, we should create a dedicated, less-privileged user for our project).   
**`PASSWORD`**: The password that corresponds to the `USER`.    
**`HOST`**: The address of our database server. `localhost` (or `127.0.0.1`) means the database is running on the same machine as our Django application. In production, this might be an IP address or a domain name.   
**`PORT`**: The network port that the PostgreSQL server is listening on. `5432` is the standard, default port for PostgreSQL. This line is often optional if you're using the default port.
#### MySQL Configuration
Similarly, to connect to MySQL, you first need to install its specific Python driver, `mysqlclient`.
```shell
pip install mysqlclient # pip3 for mac/linux
```
After installing the driver, we update the `DATABASES` dictionary inside `settings.py` with our MySQL server's details.
```python
DATABASES = {     
	'default': {         
		'ENGINE': 'django.db.backends.mysql',         
		'NAME': 'workshop_db',         
		'USER': 'root',         
		'PASSWORD': 'mypassword',         
		'HOST': 'localhost',         
		'PORT': '3306',     
	} 
}
```
These settings function just like the ones for PostgreSQL, but are specific to MySQL:
**`ENGINE`**: Tells Django to use its built-in MySQL backend.    
**`NAME`**: The name of your database (e.g., `workshop_db`), which you must create in MySQL first.
**`USER`**: Your MySQL username.    
**`PASSWORD`**: The corresponding password for that user.    
**`HOST`**: The database server's address (usually `localhost` for development).    
**`PORT`**: The network port MySQL is on. `3306` is the standard default for MySQL.    

Django’s ORM (Object-Relational Mapper) abstracts away database-specific differences, allowing us to switch between databases with minimal changes to your code.
After modifying the configuration, we can test the connection by running:
```shell
python manage.py migrate # python3 for mac/linux
```
If everything is configured correctly, Django will create the necessary database tables.

---



### Using Namespaces for URL Organization
As your project grows, it may contain multiple apps that define views with the same name (e.g., multiple apps each having a `detail` view). To prevent conflicts and improve clarity, Django allows us to define namespaces for each app’s URLs.   
Here’s we can do it:  
#### In Our App’s `urls.py`:
The cleanest and most common way to add a namespace is by setting the `app_name` variable inside our **app's `urls.py` file**. This makes our app self-contained and reusable.
```python
from django.urls import path
from . import views

app_name = 'image_share'

urlpatterns = [
	path('', views.gallery, name='gallery'),
	path('upload/', views.upload_photo, name='upload_photo'),
]
```
By adding `app_name = 'image_share'`, we are telling Django that all URL names in this file (like `'gallery'`) are now part of the `image_share` namespace.
#### In Our Project’s `urls.py`:
We can also define a namespace in our **project's `urls.py`** file when we `include()` the app's URLs:
```python
from django.contrib import admin 
from django.urls import path, include  

urlpatterns = [     
	path('admin/', admin.site.urls),     
	path('', include('image_share.urls', namespace='image_share')), 
]
```
#### Referencing Standard URLs 
Let's use our `image_share` app as an example, where `app_name = 'image_share'` and we have a URL named `'gallery'`.   
**In Templates** We use the `{% url %}` template tag with the namespaced name in the format `'app_name:view_name'`.
```html
<a href="{% url 'image_share:gallery' %}">View Gallery</a>

<a href="{% url 'image_share:upload_photo' %}">Upload New Photo</a>
```
**In Views** we use the `reverse()` function to find the URL, and `redirect()` to send the user there.  
- **`reverse()`**: A function that looks up the URL path string from its name.
- **`redirect()`**: A shortcut function that takes a URL name (or path) and returns an HTTP redirect response.
```python
from django.shortcuts import redirect
from django.urls import reverse

def my_view(request):
    # ...
    # Using the redirect() shortcut is most common.
    # It understands the 'app_name:view_name' format.
    return redirect('image_share:gallery')
    # Or
    
    # We can also use reverse() explicitly to get the URL string first
    # This is useful if we need to use the URL in another way
    url_path = reverse('image_share:gallery')  # This will return the string '/'
    return redirect(url_path)
```
#### Referencing Dynamic URLs 
This is where namespaces and URL reversing are most powerful. Let's imagine our `image_share` app has a dynamic URL for a photo's detail page.  
**`image_share/urls.py`:**
```python
app_name = 'image_share'
urlpatterns = [
	# This URL expects an integer named 'photo_id'
	path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
]
```
To reference this URL, we **must** provide a value for `photo_id`.  
**In Templates :** We pass the parameters to the `{% url %}` tag as additional arguments. The argument name (`photo_id=...`) must match the variable name in the `path()` (e.g., `<int:photo_id>`).
```html
{% for photo in photos %}
    <a href="{% url 'image_share:photo_detail' photo_id=photo.pk %}">
        View Photo {{ photo.title }}
    </a>
{% endfor %}
```
If we know we need only one argument we can pass it directly without the need of it name
```html
{% for photo in photos %}
    <a href="{% url 'image_share:photo_detail' photo.pk %}">
        View Photo {{ photo.title }}
    </a>
{% endfor %}
```
**In Views:**  We pass the dynamic data using **`args`** (a list of positional arguments) or **`kwargs`** (a dictionary of keyword arguments). Using **`kwargs`** is highly recommended because it's more explicit and less error-prone.
```python
from django.shortcuts import redirect
from django.urls import reverse

def photo_upload_success(request, new_photo_id):
    # 'new_photo_id' is just a variable, let's say its value is 5

    # --- Method 1: Using kwargs (Recommended) ---
    # The key 'photo_id' MUST match the name in the path()
    url = reverse('image_share:photo_detail', kwargs={'photo_id': new_photo_id})
    # url is now '/photo/5/'
    return redirect(url)


    # --- Method 2: Using args ---
    # This works but is less readable. The order must be correct.
    url = reverse('image_share:photo_detail', args=[new_photo_id])
    # url is now '/photo/5/'
    return redirect(url)


    # --- Method 3: The redirect() shortcut ---
    # redirect() is smart enough to pass keyword arguments to reverse()
    return redirect('image_share:photo_detail', photo_id=new_photo_id)
```

## Middlewares
### Introduction
Sometimes in our webapplication we oneed to process requests and responses globally, before they reach the views or after they leave them. Django provides a powerful mechanism for this through middleware.  
Middleware are **hooks** that sit between Django’s request/response processing. Each middleware component is a lightweight layer that can modify the request before it reaches the view or the response before it is returned to the client.    
When a request comes in, it passes through each middleware layer (from top to bottom) before it reaches our view. After our view produces a response, that response passes back through the layers (from bottom to top) before being sent to the browser.   
### How Middleware Works
We can visualize middleware as a series of layers, like an onion, with our view at the very center. Every request and response must pass through these layers.   
This process happens in two distinct phases:
1. **Request Phase**: The request travels _inward_ through each middleware layer (from top-to-bottom as listed in `settings.py`) before it reaches the view.
2. **Response Phase**: The response travels _outward_ through each layer (from bottom-to-top, in reverse order) before it’s sent back to the client.
#### The Flow of Data
This flow is critical to understand. A request passes _down_ through the list, and the response passes _up_.
```
Client
   │
   │ Request (Top-Down)
   ↓
[ Middleware 1 ]
   ↓
[ Middleware 2 ]
   ↓
[ Middleware 3 ]
   ↓
( Your View )
   ↑
[ Middleware 3 ]
   ↑
[ Middleware 2 ]
   ↑
[ Middleware 1 ]
   ↑
   │ Response (Bottom-Up)
   │
Client
```
#### Order Is Critical
We register our middleware as a list in `settings.py` under the `MIDDLEWARE` setting. The order in this list is not arbitrary; it defines the execution order:
- **Request processing** follows the list **top-to-bottom**.
- **Response processing** follows the list in **reverse, bottom-to-top**.

This is why, for example, `SessionMiddleware` must come _before_ `AuthenticationMiddleware`. The request must first have the session loaded (top-down) before the authentication middleware can use that session to find the user.
#### Capabilities of Middleware
During this two-way journey, each middleware layer has the power to:
- **Inspect and modify** the incoming `request` object before it reaches the view. 
- **Process and modify** the outgoing `response` object after the view has finished.
- **Handle exceptions** that might be raised by the view.
- **Execute custom logic** during either phase, such as performing authentication checks, logging, adding security headers, or managing sessions.

#### Example of Default Middleware
We can expect the default middleware in our settings.py file to understand how they work
```python
MIDDLEWARE = [     
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',    
	'django.middleware.common.CommonMiddleware',    
	'django.middleware.csrf.CsrfViewMiddleware',    
	'django.contrib.auth.middleware.AuthenticationMiddleware',    
	'django.contrib.messages.middleware.MessageMiddleware',    
	'django.middleware.clickjacking.XFrameOptionsMiddleware', 
]
```
Each of these performs a specific function. For instance, `AuthenticationMiddleware` populates `request.user`, and `CsrfViewMiddleware` protects against Cross-Site Request Forgery attacks.   
### Creating Custom Middleware
In Django, we can create our own custom middleware to add specific logic that runs for every request and response.  
Middleware can be written in **two ways**:
- As a **function-based** middleware (a simple function that takes `get_response` and `request`).
- As a **class-based** middleware (a class that defines `__init__` and `__call__` methods).

Let’s create two simple examples to understand how both approaches work.
#### Logging Request and Response 
In this example, we’ll make a middleware that logs the **HTTP method** (like GET or POST) and the **requested path**, as well as the **response status code** after the view runs.we create new file inside our app folder named `middleware.py` and we define our middleware class inside it.   
**`blog/middleware.py`**
```python
class LoggingMiddleware:
    def __init__(self, get_response):
        # get_response is the next layer (view or middleware)
        self.get_response = get_response

    def __call__(self, request):
        # This runs before the view
        print(f"[Request] Method: {request.method}, Path: {request.path}")

        # Call the next middleware or view
        response = self.get_response(request)

        # This runs after the view
        print(f"[Response] Status Code: {response.status_code}")

        return response
```
When we create a middleware as a **class**, Django uses two special methods inside it:  `__init__()` and `__call__()`.     

**`__init__(self, get_response)`**: This part runs only once, when Django starts the server. Django gives our middleware a special function called **`get_response`**, which represents the **next step** in the request chain (the next middleware or the view).     

`__call__(self, request)`
This method runs **every time** a new request is received, Here’s what happens step by step:
1. Django calls the `__call__` method and gives it the incoming **request**.
2. Before sending the request to the view, we can do something with it for example, print the HTTP method and path:  
```python
print(f"[Request] Method: {request.method}, Path: {request.path}")
```
3. Then, we pass the request to the next layer using:
```   python
response = self.get_response(request)
``` 
This line allows the view (or next middleware) to run and produce a response.    

4. After the view returns a response, we can again do something  here, we print the response’s status code:
```python
print(f"[Response] Status Code: {response.status_code}")
```
5. Finally, we return the response back to Django so it can send it to the user’s browser.

To use it, we add our middleware to `MIDDLEWARE` list inside  ``settinga.py``:
```python
MIDDLEWARE = [
    # ... existing middleware ...
    'blog.middleware.LoggingMiddleware',
]
```
Now when we visit any page, Django will print messages like:  
```shell
[Request] Method: GET, Path: / [Response] Status Code: 200
```
#### Blocking Specific IP 
Sometimes, we may want to **block access** to our website from certain IP addresses for example, to stop spam bots or restrict internal access.    
We can easily do this by creating a **function-based middleware** that checks the visitor’s IP address before allowing the request to continue.    
This time, we’ll place our middleware **inside the main project folder**  
**``project_name/middleware.py``**
```python
from django.http import HttpResponseForbidden  

def block_ip_middleware(get_response):
    def middleware(request):
        blocked_ips = ['127.0.0.2']  # You can add more IPs here
        client_ip = request.META.get('REMOTE_ADDR')  # Get the user’s IP address

        # Check if the user's IP is in the blocked list
        if client_ip in blocked_ips:
            return HttpResponseForbidden("Access denied from your IP address.")

        # Otherwise, continue normally
        response = get_response(request)
        return response

    return middleware
```
The outer function `block_ip_middleware(get_response)` runs **once** when Django starts. Its job is to receive `get_response` (the next layer in the chain) and return another function that will handle each request.   

The inner function `middleware(request)` is the real worker  it runs for every request. It checks the visitor’s IP address, and if it’s in the blocked list, it immediately returns an `HttpResponseForbidden`, stopping the request before it reaches the view. If the IP is not blocked, it simply calls `get_response(request)` to continue the normal flow and then returns the response.

Finally, the outer function returns this inner `middleware` function to Django, which then calls it automatically for every new request.  

Now we need to tell Django to use our middleware.  we open  **`settings.py`** and add it to the `MIDDLEWARE` list:
```python
MIDDLEWARE = [
    # ... existing middleware ...
    'workshop4.middleware.block_ip_middleware',
]
```

## Implement Testing and Unit Tests
