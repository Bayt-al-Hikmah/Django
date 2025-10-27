## Objectives

- Upload and manage files efficiently
- Work with settings files and project configuration
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
## Implement Testing and Unit Tests
