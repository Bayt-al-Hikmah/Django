## Objectives
- Understanding the shift from Server-Side Rendering to APIs.
- Building REST API with Django
## Shifting from Server-Side Rendering to APIs.
### Introduction
In our past workshops, we used server-side rendering. With this approach, each request returned an entire HTML page. The problem is that every time we triggered an action in the web app or navigated to a new URL, the server re-rendered a whole page. This means we ended up downloading the full HTML again, even when only a small part of the page had changed.

This is referred to as a “Hotwire-like” approach, and while it works, it slow down the application. Often, we only need to retrieve a small piece of data and update a specific section of the page, rather than reloading everything.

To fix this, we can use an API to send and receive small chunks of data and update just the required parts of the interface.
### API
API (Application Programming Interface) is a layer that we add to our web app to connect the frontend with the backend. Our app uses the API to retrieve and send data to the server. The backend receives the data, saves the results, processes whatever is needed, and then returns the updated information to the frontend.   
APIs make it easier to extend our application and make it available on other platforms. For example, if we want to build a mobile application, we only need to create the user interface and connect it to our web server using the API. The same backend logic and data can be reused without any changes.

![](./api.png)


### Javascript Role
To use the API in our web application, we rely on JavaScript.  
JavaScript handles communication with the server by fetching data from the API and then dynamically updating the DOM to reflect that data, Instead of submitting a full form and reloading the page, we can let the user type in an input field, click a button, and then:
1. Catch the click event with JavaScript
2. Send a request to the API    
3. Receive the response from the server
4. Update the DOM using the data from the response

This way, only the necessary part of the page changes, and our app becomes much faster and smoother.
### REST API Architecture
There are many patterns to design APIs for our web apps, but the most common and beginner friendly one is the REST API.  
REST stands for Representational State Transfer. It is named this way because the server sends a representation of the requested resource usually as JSON, and the client is responsible for handling the state of the application on its side. 
### REST Main Properties
REST APIs are defined by several mandatory constraints that help achieve scalability, simplicity, and performance in a web service.
#### Stateless
Each request sent to the server must contain all the information needed to process it. The server does not store any information about previous requests. 
#### Client–Server Separation
The frontend and backend are separated, The frontend focuses only on the user interface and user experience, while the backend handles data storage and business logic. 
#### URLs Identify Resources
REST treats everything as a resource (users, tasks, posts, products, etc.), Each resource is identified by a clear and meaningful URL, for example:
- `/tasks`
- `/users/1`
#### Use of Standard HTTP Methods
REST relies on standard HTTP methods to describe actions instead of custom commands:
- ``GET`` Retrieve data
- ``POST`` Create new data
- ``PUT / PATCH`` Update existing data
- ``DELETE`` Remove data

By following these conventions, REST APIs remain predictable, easy to understand, and consistent across different applications.
## Building REST API with Django
Now that we understand how REST APIs work, we will apply these concepts by building a Task Management REST API.  
The API will be responsible for registering users, authenticating logins, updating user profiles, and displaying, editing, and deleting tasks associated with each user.
### Setting Our Envirenment
We start by creating virtual envirenment and activate it
```shell
# Creating the envirenment
python -m venv env # for mac/linux we use "python3"
# Activating it
./env/Script/activate # for mac/linux we use "source ./env/bin/activate"
```
### Creating Django Project
After activating our envirenment, we install Django
```shell
pip install django # for mac/linux we use "pip3"
```
After that, we create new Django project
```shell
django-admin startproject workshop5
cd workshop5
```
### Installing Rest Api Framework
To create Rest Api in Django we should install additional framework `djangorestframework`, This framework give us the basic tool we need to make and set Rest Api.
```shell
pip install djangorestframework
```
After installing it, we add it to INSTALLED_APPS inside the project `settings.py` file.
```python
INSTALLED_APPS = [
    # Other Apps
    'rest_framework', ## our Framework
]
```
### Creating Resource
Now we finished setting the basic configuration, Let's create the resouces for our API, we need three main apps to handel the resources:
- user: responsible for managing user-related actions such as updating username, password, email, and avatar.    
- task: responsible for creating, reading, updating, and deleting tasks that belong to authenticated users.
- auth: responsible for registration and login 

Let’s generate those apps:
```shell
python manage.py startapp user
python manage.py startapp task
python manage.py startapp users_auth
```
After that we add them to the INSTALLED_APPS inside our ``settings.py`` file
### Creating The Database Models
For our application we will need two core models: the User model and the Task model.   
The User Model represents application users and stores their basic information such as username, password, email, and avatar. The Task model represents tasks created by users, including details like task name, creation time, and current state (active or done).

We also add a one-to-many relationship between users and tasks:
- A user can have many tasks
- Each task belongs to exactly one user
#### Creating User model
We start by creating the user model, inside our ``user`` app we define `UserModel` class it inherite from Django basic ``AbstractUser`` model and add to it the avatar field.   
**``user/models.py``**
```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/') 
```
We are using `ImageField` so we need to install the pillow package.
```shell
pip install pillow
```
We set the media folder in our `settings.py`, so we can upload files to our server.
```python
MEDIA_ROOT = BASE_DIR / 'media' 
MEDIA_URL = '/media/'
```
Finally we need to tall Django to use our costume model for authentication instead the default one, we do this in our ``settings.py`` file.
```python
AUTH_USER_MODEL = 'user.UserModel'
```
#### Creating The Task Model
Now we move to create the Task Model, we do that inside `task` app.   
**`task/models.py`**
```python
from django.db import models
from user.models import UserModel

class Task(models.Model):
    user = models.ForeignKey(UserModel, related_name="tasks",on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    state = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```
### Creating The Serializer
In our previous applications, we used forms to receive data from users, and Django forms to validate and handle that data. However, when working with REST APIs, data is received in JSON format, and responses are also returned to the user as JSON.

To handle this, we use serializers. Serializers are special class that are responsible for transforming our models into JSON format and returning them to the user. They also convert incoming JSON data into model instances and validate the data sent by the user.
#### Creating Auth Serializers
We Start by creating the auth serializers, that will work with the registration and login data, inside the `users_auth` folder we create `serializers.py` file and inside it we define our classes.  
First we import `get_user_model` and use it to get the User model, which we set in the ``settings.py`` in our case it will be the `UserModel` that we declared inside `user/models.py`.  
After this we create our serializers classes we will need two classes.   
- ``RegisterSerializer``: This serializer inherits from ``ModelSerializer`` which is a special class tied directly to a Django model. It automatically generates serializer fields based on the model fields and provides built-in ``create()`` and ``update()`` methods. We will use it to create new users. First thing we do it marking our password field as as write_only so it is not returned in responses. After this we define `Meta` class where we set the model our serializer will use and the fields we will recive, Next we override the `create` method, we get our password we create User instance using the validated data, we hashes and set the password using ``set_password()`` before then we save the user to the database and return it.
- `LoginSerializer`: This serializer inherits from Serializer, which is a basic serializer where all fields and validation logic are explicitly defined. It is not connected to a Django model by default.
Inside this class, we receive the username and password, then define a validate method that uses Django’s built-in authenticate() function to check whether the user credentials are valid. If authentication succeeds, the authenticated user is added to the validated data and returned; otherwise, a validation error is raised.
```python
from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'avatar']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data
```
#### Creating User Serializers
We also need serialiers for user, it will handel updating profile data like username, email, avatar and password, lets create two class.
- `UpdatePasswordSerializer`: inherits from Serializer class, it responsible for updating the user password.
- `UpdateUserSerializer`: inherits from `ModelSerializer` it use the `User` model and expose the `username`, `email` and `password` fields. it use the `ModelSerializer` predifined methods to update the user data
```python
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UpdatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']
```
#### Creating Task Serializers
Finally, we create the Task serializer. This serializer is used to handle all task-related operations, such as creating new tasks, updating existing tasks, and deleting tasks.  
We set the `user` and `created_at` fields to read only so we prevents users from assigning tasks to other users
```python
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'state', 'created_at', 'user']
        read_only_fields = ['user', 'created_at']
```
### Creating the Views
After defining our serializers, the next step is to create the views. Views are responsible for handling HTTP requests, using serializers to validate data, and returning appropriate responses.  
We will use Django REST Framework views to handle authentication, user profile updates, and task operations.
#### The Authentication Views
We will create two authentication views: one for registration and one for login. These views use the authentication serializers defined earlier. Instead of using function-based views, we use class-based views by inheriting from `APIView`. This allows us to organize our logic clearly and take advantage of Django REST Framework features.

- `RegisterView`: This view handles user registration and uses the `POST` method because data is sent from the client. Inside the method, we create `RegisterView` serializer instance using the request data and check whether it is valid. If the data is valid, the serializer saves the new user and returns a success message. Otherwise, it returns a response containing the validation errors.  
- `LoginView`: This view also uses the `POST` method and relies on the `LoginSerializer` to validate the incoming login credentials. If the credentials are valid, the serializer returns the authenticated user and log him in; otherwise, an error response is sent.
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import login

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response(
                {"message": "Login successful"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```
#### The User Views
We also create views that allow the authenticated user to manage their profile data. These views are protected using the `IsAuthenticated` permission, which ensures that only logged-in users can access them.
- `UserProfileView`: This class to retrive loged in user information, we use the `get` method, we retriving data using `GET` HTTP method. inside it we use `UpdateUserSerializer(request.user)` to retrive loged in user information and return them back.
- `UpdateUserView`: This class to update the logged in user information avatar, email nd username, we used the `PUT` method.
- `UpdatePasswordView`: Finally this class update the logged in user password. we used the `PATCH` method.
```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UpdatePasswordSerializer, UpdateUserSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UpdateUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateUserSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UpdatePasswordSerializer(
            instance=request.user,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password updated successfully"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```
#### User Task Views
Now we create the last views, The task views. we will use ``ModelViewSet`` because it provides a complete set of CRUD operations (Create, Read, Update, Delete) for our Task model with minimal code. ModelViewSet automatically gives us all these actions (list, retrieve, create, update, partial_update, and destroy) in a single class.  
We override the ``get_queryset()`` method to ensures that a user can only access their own tasks, by filtering tasks based on the currently authenticated user (self.request.user). 
We also override the ``perform_create()`` method which is called when a new task is created; here, we automatically associate the task with the logged-in user. 
```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```
### Configuring the URLs
Now we set up our URL routing to connect the views we created with actual API endpoints. Since our project contains both regular API views `APIView` and a `ModelViewSet`, we will combine standard path-based routing with router-based routing.
#### Why we use a Router
For the task views, we used a `ModelViewSet`, which works best with a DRF router. A router automatically generates all the required URLs for CRUD operations (`list`, `create`, `retrieve`, `update`, `partial_update`, `destroy`) without us having to define each one manually. This keeps the `urls.py` file clean and consistent with RESTful conventions.
#### Defining Auth `urls.py`
We start by defining the ``urls.py`` for the `users_auth` app, we use the `RegisterView` and `LoginView` view, when we register them we use the `as_view()` method,.
```python
from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
```
#### Defining User `urls.py`
Same as Before we create `urls.py` file inside our ``user`` app directory, in this directory we configure the `urlpatterns` for the user app.
```python
from django.urls import path
from .views import UserProfileView, UpdateUserView, UpdatePasswordView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('update/', UpdateUserView.as_view(), name='user-update'),
    path('update-password/', UpdatePasswordView.as_view(), name='user-update-password'),
]
```
#### Defining Task `urls.py`
Finally we define the task ``urls.py``, Since we used `ModelViewSet`, we use a router here. 
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]
```
 This will expose the following endpoints
- `GET /tasks/`  List user tasks
- `POST /tasks/` Create a new task
- `GET /tasks/<id>/` Retrieve a specific task
- `PUT /tasks/<id>/` Update a task
- `PATCH /tasks/<id>/` Partially update a task
- `DELETE /tasks/<id>/` Delete a task

Finally we set the main ``urls.py`` to include all our apps urlspatterns
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include('users_auth.urls')),
    path('api/users/', include('users.urls')),
    path('api/tasks/', include('tasks.urls')),
]
```
### Creating The Interface
Now that our API is fully functional, we need a user interface to interact with it. Instead of the server rendering HTML pages for every route, we will serve a single HTML file (Single Page Application approach) and use JavaScript to fetch data from our API and update the DOM dynamically.
#### Serving the Entry Point
To serve our frontend entry point (index.html) and static assets, we create a dedicated app called index. This app has a single responsibility: handling the main entry point of our application.
```shell
python manage.py startapp index
```
After that we add the app to ``INSTALLED_APPS`` on our ``settings.py`` file
```python
INSTALLED_APPS = [
    # other apps
    'index',
]
```
Now we create the index view inside ``views.py``, we define a simple view that returns the ``index.html`` template.  
We use TemplateView because no backend logic is required.
```python
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"
```
We create and configure `urls.py` for the index App
```python
from django.urls import path
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
```
Finally, we include the index app URLs in the main project urls.py.
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/auth/', include('users_auth.urls')),
    path('api/users/', include('users.urls')),
    path('api/tasks/', include('tasks.urls')),

    # Frontend entry point
    path('', include('index.urls')),
]
```
Now, when you visit `http://127.0.0.1:8000/`, Django will serve the HTML file, and the rest of the application interaction will happen via JavaScript calling our API endpoints.
#### The HTML and CSS
We created a simple interface with two main sections: a Login section and a Dashboard section. Initially, the dashboard is hidden. After the user successfully logs in, the login section will be hidden, and the dashboard will be displayed.

We can find the HTML template and styling files inside the ``materials`` folder. The ``index.html`` file should be moved to the ``templates`` folder and the ``style.css`` file should be moved to the ``static/css`` folder.
#### Client-Side Logic (JavaScript)
This is the most important part. The JavaScript file acts as the bridge between HTML events (such as clicks) and the Express REST API.

The code listens for form submissions and button clicks, then makes API calls using fetch to the corresponding endpoints. For example, when a user logs in, it sends a POST request to ``/api/login``, stores the session, and updates the view to display the user’s tasks. Similarly, task actions like creating, updating, or deleting a task are sent to the ``/api/tasks`` endpoints, and the page updates dynamically without reloading.

Helper functions handle view switching, displaying messages, and ensuring that only logged-in users can access protected sections.

The file is currently in the ``materials`` folder. We should move it  to the ``static/js`` folder so it can be served as a static asset by Django.
### Token-Based Authentication 
In the current Task Manager API, we use Secure-Session to manage authentication. This approach is effective for traditional web applications where the server and client are closely tied, and the browser handles session cookies automatically.  
However, modern APIs often require authentication that is stateless and can be easily used by various clients (mobile apps, other servers, JavaScript frontends). This is where Token-Based Authentication comes in.
#### How Tokens Work
Instead of the server storing session data for every user (stateful), the server issues a secure, self-contained token (like a JSON Web Token or JWT) upon successful login.
1. **Client Logs In:** The user sends credentials (username/password) to the `/api/login` endpoint.
2. **Server Generates Token:** If successful, the server creates a unique token containing the user's ID, expiration time, and a secure signature. The token is returned in the response.
3. **Client Stores Token:** The frontend (e.g., JavaScript) stores this token (usually in local storage).
4. **API Access:** For every subsequent request to protected endpoints (e.g., `/api/tasks`), the client includes this token in the `Authorization` header, typically prefixed with `Bearer`.
5. **Server Verification:** The server receives the request, verifies the token's signature, extracts the user ID, and grants access. No database lookup for a session is required, making the API stateless and faster.
### Implementing Token Authentication with NestJs
We use the `@nestjs/jwt` and ``@nestjs/passport`` to impliment the Token Authentication.

First, we install it using:
```shell
npm install @nestjs/jwt @nestjs/passport passport passport-jwt
```
#### Setting the JWT Token
We set the auth module to apply the JWT Authentication. and we add `JwtStrategy` to our providers
```ts
// we add this to the import
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { JwtStrategy } from './jwt.strategy';
require('dotenv').config(); // load env variable
// And inside Module decorator imports we add 
imports: [
    PassportModule,
    JwtModule.register({
      secret: process.env.JWT_SECRET,
      signOptions: { expiresIn: '1h' },
    }),// other imports
  ], 

providers: [AuthService,JwtStrategy],
```
- secret is used to sign and verify JWT tokens
- expiresIn defines token lifetime
#### Creating the JWT Strategy
After that we create The JWT Streategy,it is responsible for verifying incoming tokens.  
**``auth\jwt.strategy.ts``**
```ts
import { Injectable } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      secretOrKey: process.env.JWT_SECRET,
    });
  }

  async validate(payload: any) {
    return payload;
  }
}
```
This Strategy extract the token from the ``Authorization`` header,verify it then the decoded payload is attached to `request.user`.
#### Editing The Guard 
Now we not using session we need to edit our guards to apply the JWT Authentication
```ts
import { Injectable } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';

@Injectable()
export class Authorized  extends AuthGuard('jwt') {}
```
We now need only one guard, the Authorized it extand the `AuthGuard` and implement the `jwt`. we remove the guard from the `auth.controller`.
#### Editing the Controller
Finally we need to edit our controllers, we start by editing the login controller instead of saving userId in session, we generat and return token.
```ts
import { Controller, Post, Body, Req,Res,UseGuards} from '@nestjs/common';
import { AuthService } from './auth.service';
import { CreateUserDto,LoginDto } from '../users/dto/create-user.dto';
import type { FastifyRequest,FastifyReply } from 'fastify';
import { File } from 'src/parameter_decorators/parameter.decorator.file'
import { Fields } from 'src/parameter_decorators/parameter.decorator.fields'
import type { MultipartFile} from '@fastify/multipart';
import { JwtService } from '@nestjs/jwt';
@Controller('api')

export class AuthController {
  constructor(private readonly authService: AuthService,
    private jwtService: JwtService
  ) {}
  @Post('register')
  async register(@File() file:MultipartFile,@Fields() fields:CreateUserDto,@Res() res:FastifyReply) {
    const filename:string = await this.authService.uploadAvatar(file);
    fields.avatar = filename
    await this.authService.register(fields);
    return res.status(201).send({ message: 'Registred' });
  }
  @Post('login')
  async create(@Body() loginDto: LoginDto, @Req() req: FastifyRequest,@Res() res:FastifyReply) { 
    const user = await this.authService.login(loginDto);
    if(!user){
    return res.status(401).send({ message: 'Invalid credentials' });
    }
    const payload = {
      userId:user.id,
      email:user.email
    }
    return res.status(201).send({ message: 'logged in' ,access_token:this.jwtService.sign(payload)});
  } 
}
```
We import `JwtService` add it to our ``AuthController``, then generate the token using the `sing` method.
Finally we edit our tasks and users controller we replace `req.session.get("userId")` with `req.user.userId`. We Also remove the `FastifyRequest` type from the `@Req() req`.
#### Editing the Javascript
Now we update our JavaScript to work with JWT authentication. When a user logs in, the backend returns a token, which we store in the browser using:
```javascript
localStorage.setItem('token', data.access_token);
```
For every subsequent API request, we need to include this token in the **Authorization header** so the backend can verify the user. This is done by adding:
```js
'Authorization': `Bearer ${localStorage.getItem('token')}` 
```
to the headers of each `fetch` request. This ensures that only authenticated users can access protected endpoints.
### API Rate Limiting
As our API gains more users, we need to protect it from abuse, excessive load, and denial-of-service (DoS) attacks. Rate Limiting is the practice of restricting the number of API requests a user (or IP address) can make within a specific time window.

#### Implementing Rate Limiting
To protect our NestJs application from abuse and excessive requests, we implement rate limiting. Rate limiting helps prevent brute-force attacks, reduces server load, and improves overall API reliability.  
In NestJs, the most common and recommended solution is the **`@nestjs/throttler`**,We start by installing it using:
```
npm install @nestjs/throttler
```
#### Installing Redis
Redis (Remote Dictionary Server) is a very fast, in-memory data store. It is commonly used for caching, sessions, queues, and rate limiting. Because Redis stores data in memory, it is significantly faster than traditional databases, making it ideal for tracking API requests in real time.  
Redis is used with rate limiting plugin to persist rate-limit data. This allows rate limits to remain consistent even if the server restarts or runs across multiple instances.  
We install it as following

- Ubuntu / Debian:

```
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

- macOS (Homebrew):

```
brew install redis
brew services start redis
```

- Windows Redis is not officially supported on Windows, but we can use **Redis for Windows** provided by the community [Redis for Windows](https://github.com/tporadowski/redis/releases).

After that we install the redis package
```
npm install  @nest-lab/throttler-storage-redis ioredis
```
#### Create Redis Client
Now we need to create a Redis connection. 
**`src/redis/redis.client.ts`** 
```ts
import Redis from 'ioredis';

export const redis = new Redis({
  host: process.env.REDIS_HOST,
  port: Number(process.env.REDIS_PORT),
});
```
#### Configure Throttler with Redis Storage
After creating our redis client, we update ``app.module.ts`` to use  Throttler with redis as storage
```ts
// we add this to the import
import { ThrottlerModule } from '@nestjs/throttler';
import { APP_GUARD } from '@nestjs/core';
import { ThrottlerGuard } from '@nestjs/throttler';
import {redis } from 'src/redis/redis.client'

@Module({
  imports: [
     ThrottlerModule.forRoot({
      throttlers:[{
      ttl: 60,
      limit: 100,
    }],
    storage: new ThrottlerStorageRedisService(redis) // setting storage to redis
    }),// other imports
  ], 
  providers: [
    {
      provide: APP_GUARD,
      useClass: ThrottlerGuard,
    },// other providers
  ],
})
export class AppModule {}
```
- ttl: 60000  time window in mini seconds here we set it to 60000 which mean one minute.
- limit: 100 mean max 10 requests per minute per IP.
- storage: we set it to the `ThrottlerStorageRedisService(redis)`
### Configuring The Routes
This configuration will work globally in all our application all our routes wiill have rate limit of 10 request per second, we can override this, in our controller for example we can use `@SkipThrottle()` Decorator to skip and don't apply the rate limit for specific route or controller. we can also use `@Throttle(100, 1000)` Decorator to override the rate limit for specific.  
Example lets make the main route `/` skip the rate limit
```ts
import { Controller, Get,Render } from '@nestjs/common';
import { AppService } from './app.service';
import { SkipThrottle } from '@nestjs/throttler';

@SkipThrottle()
@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}
  @Get()
  @Render('index')
  index(){
  }
}
```
Now the rate limit wont work on this Controller.  