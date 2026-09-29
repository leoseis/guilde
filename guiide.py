"""
DJANGO BLOG PROJECT
Backend Class Teaching Guide

This file is a teaching reference for a simple Django Blog project.
It is written as valid Python so it can be opened directly in VS Code.

PROJECT GOAL
------------
Build one simple Blog application gradually while each class focuses
on one Django topic at a time.

The project will grow through:
1. Django setup
2. Models and databases
3. Admin
4. URLs
5. Views
6. Templates
7. Static files
8. Media files
9. Forms
10. CRUD
11. Authentication
12. Relationships and other advanced features

IMPORTANT:
Do not try to teach all of these topics at once.
At each stage, only introduce the Django concepts needed for that lesson.


============================================================
CURRENT PROJECT STRUCTURE
============================================================

blog/
|
|-- blogapp/
|   |-- migrations/
|   |-- templates/
|   |   `-- blogapp/
|   |       |-- base.html
|   |       |-- post_list.html
|   |       `-- post_detail.html
|   |
|   |-- admin.py
|   |-- apps.py
|   |-- models.py
|   |-- urls.py
|   `-- views.py
|
|-- myproject/
|   |-- settings.py
|   `-- urls.py
|
|-- static/
|   `-- css/
|       `-- style.css
|
|-- media/
|   `-- posts/
|
|-- db.sqlite3
|-- manage.py
|-- requirements.txt
`-- venv/


============================================================
PART 1 — CREATE THE ENVIRONMENT
============================================================

Run these commands in the terminal.

Create a virtual environment:

    python3 -m venv venv

Activate it on Linux:

    source venv/bin/activate

Install Django:

    pip install django

Install Pillow for image uploads:

    pip install pillow

Save installed packages:

    pip freeze > requirements.txt

Check Django:

    django-admin --version


============================================================
PART 2 — CREATE THE DJANGO PROJECT
============================================================

Create the project:

    django-admin startproject myproject .

Create the blog application:

    python manage.py startapp blogapp

Start the development server:

    python manage.py runserver

Open:

    http://127.0.0.1:8000/

The Django welcome page confirms that the project is working.


============================================================
PART 3 — REGISTER THE APP
============================================================

File:
    myproject/settings.py

Add the application to INSTALLED_APPS:

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",

        "blogapp",
    ]


============================================================
PART 4 — DATABASES AND MODELS
============================================================

A Django model describes the structure of data that we want
to store in the database.

File:
    blogapp/models.py

Use a simple Post model:

    from django.db import models


    class Post(models.Model):

        title = models.CharField(max_length=200)

        author = models.CharField(max_length=100)

        content = models.TextField()

        created_at = models.DateTimeField(auto_now_add=True)

        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.title


------------------------------------------------------------
DATABASE EXPLANATION
------------------------------------------------------------

The model above represents a database table.

The fields become columns:

    title
    author
    content
    created_at
    updated_at

CharField:
    Used for shorter text.

TextField:
    Used for longer text.

DateTimeField:
    Used for dates and times.

auto_now_add=True:
    Sets the value when the object is first created.

auto_now=True:
    Updates the value whenever the object is saved.


============================================================
PART 5 — MIGRATIONS
============================================================

After changing models, create migrations:

    python manage.py makemigrations

Apply them:

    python manage.py migrate

Simple explanation:

    makemigrations
        |
        `-- Creates instructions for changing the database

    migrate
        |
        `-- Applies those instructions to the database


============================================================
PART 6 — DJANGO ADMIN
============================================================

File:
    blogapp/admin.py

Register the model:

    from django.contrib import admin
    from .models import Post

    admin.site.register(Post)

Create an administrator:

    python manage.py createsuperuser

Start the server:

    python manage.py runserver

Open:

    http://127.0.0.1:8000/admin/

Create a few sample blog posts from the admin dashboard.


============================================================
PART 7 — URLS
============================================================

Create:

    blogapp/urls.py

Code:

    from django.urls import path
    from . import views


    urlpatterns = [
        path("", views.post_list, name="post_list"),
        path(
            "post/<int:post_id>/",
            views.post_detail,
            name="post_detail"
        ),
    ]


Connect the app URLs to the project.

File:
    myproject/urls.py

Code:

    from django.contrib import admin
    from django.urls import include, path


    urlpatterns = [
        path("admin/", admin.site.urls),
        path("", include("blogapp.urls")),
    ]


============================================================
PART 8 — VIEWS
============================================================

File:
    blogapp/views.py

Start with two simple views:

    from django.shortcuts import get_object_or_404, render

    from .models import Post


    def post_list(request):

        posts = Post.objects.all().order_by("-created_at")

        return render(
            request,
            "blogapp/post_list.html",
            {"posts": posts}
        )


    def post_detail(request, post_id):

        post = get_object_or_404(
            Post,
            id=post_id
        )

        return render(
            request,
            "blogapp/post_detail.html",
            {"post": post}
        )


------------------------------------------------------------
VIEW EXPLANATION
------------------------------------------------------------

post_list():

    Gets all posts from the database and sends them to a template.

post_detail():

    Gets one post using its ID and sends it to a template.

render():

    Connects a view to an HTML template.

get_object_or_404():

    Gets an object or returns a 404 page if it does not exist.


============================================================
PART 9 — TEMPLATES
============================================================

Create:

    blogapp/templates/blogapp/

Add:

    base.html
    post_list.html
    post_detail.html


------------------------------------------------------------
base.html
------------------------------------------------------------

Basic template:

    {% load static %}

    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>
            {% block title %}
                My Django Blog
            {% endblock %}
        </title>

        <link rel="stylesheet" href="{% static 'css/style.css' %}">
    </head>

    <body>

        <header>
            <h1>My Django Blog</h1>

            <nav>
                <a href="{% url 'post_list' %}">
                    Home
                </a>
            </nav>
        </header>

        <main>

            {% block content %}
            {% endblock %}

        </main>

    </body>

    </html>


------------------------------------------------------------
post_list.html
------------------------------------------------------------

    {% extends "blogapp/base.html" %}

    {% block title %}
        Blog Posts
    {% endblock %}

    {% block content %}

        <h2>Blog Posts</h2>

        {% for post in posts %}

            <article class="post">

                <h2>
                    <a href="{% url 'post_detail' post.id %}">
                        {{ post.title }}
                    </a>
                </h2>

                <p>
                    By {{ post.author }}
                </p>

                <p>
                    {{ post.content|truncatewords:30 }}
                </p>

                <p>
                    {{ post.created_at }}
                </p>

            </article>

        {% empty %}

            <p>No blog posts available.</p>

        {% endfor %}

    {% endblock %}


------------------------------------------------------------
post_detail.html
------------------------------------------------------------

    {% extends "blogapp/base.html" %}

    {% block title %}
        {{ post.title }}
    {% endblock %}

    {% block content %}

        <article class="post">

            <h1>{{ post.title }}</h1>

            <p>By {{ post.author }}</p>

            <p>{{ post.created_at }}</p>

            <hr>

            <p>{{ post.content }}</p>

            <a href="{% url 'post_list' %}">
                Back to Blog
            </a>

        </article>

    {% endblock %}


============================================================
PART 10 — STATIC FILES
============================================================

STATIC FILES are files that belong to the website.

Examples:

    CSS
    JavaScript
    logos
    icons

Create:

    static/
        css/
            style.css


------------------------------------------------------------
settings.py
------------------------------------------------------------

Use:

    STATIC_URL = "static/"

    STATICFILES_DIRS = [
        BASE_DIR / "static",
    ]


------------------------------------------------------------
style.css
------------------------------------------------------------

Start with simple styling:

    body {
        font-family: Arial, sans-serif;
        background: #f4f4f4;
        margin: 0;
    }

    header {
        background: #222;
        color: white;
        padding: 20px;
    }

    main {
        width: 80%;
        max-width: 900px;
        margin: 30px auto;
    }

    .post {
        background: white;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 8px;
    }

    a {
        text-decoration: none;
    }


------------------------------------------------------------
STATIC FILE FLOW
------------------------------------------------------------

Browser
    |
    v
Template
    |
    v
{% load static %}
    |
    v
static/css/style.css
    |
    v
Website styling


============================================================
PART 11 — MEDIA FILES
============================================================

MEDIA FILES are files uploaded by users.

Examples:

    Blog images
    Profile pictures
    Product images


------------------------------------------------------------
SETTINGS.PY
------------------------------------------------------------

Add:

    MEDIA_URL = "/media/"

    MEDIA_ROOT = BASE_DIR / "media"


------------------------------------------------------------
MODEL
------------------------------------------------------------

Add an image field to the Post model:

    image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True
    )


After changing the model:

    python manage.py makemigrations
    python manage.py migrate


------------------------------------------------------------
PROJECT URLS
------------------------------------------------------------

File:
    myproject/urls.py

Use:

    from django.conf import settings
    from django.conf.urls.static import static
    from django.contrib import admin
    from django.urls import include, path


    urlpatterns = [
        path("admin/", admin.site.urls),
        path("", include("blogapp.urls")),
    ]


    if settings.DEBUG:
        urlpatterns += static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT
        )


------------------------------------------------------------
MEDIA FOLDER
------------------------------------------------------------

Create:

    media/

When an image is uploaded, Django will place it under:

    media/posts/


------------------------------------------------------------
DISPLAY AN IMAGE IN A TEMPLATE
------------------------------------------------------------

Use:

    {% if post.image %}

        <img
            src="{{ post.image.url }}"
            alt="{{ post.title }}"
        >

    {% endif %}


------------------------------------------------------------
IMPORTANT DIFFERENCE
------------------------------------------------------------

STATIC:

    Files supplied by the developer.

MEDIA:

    Files uploaded by users.


============================================================
PART 12 — CHECKPOINT FOR THE MEDIA/STATIC CLASS
============================================================

Before moving to forms or CRUD, students should be able to:

    1. Explain what static files are.
    2. Explain what media files are.
    3. Create a static folder.
    4. Connect CSS using {% static %}.
    5. Configure STATIC_URL.
    6. Configure STATICFILES_DIRS.
    7. Configure MEDIA_URL.
    8. Configure MEDIA_ROOT.
    9. Add ImageField to a model.
    10. Run migrations.
    11. Upload an image through Django Admin.
    12. Display the image in a template.


============================================================
PART 13 — THE NEXT STAGE: MODEL FORMS
============================================================

Only introduce this after the database, static and media
concepts are working.

Create:

    blogapp/forms.py

Code:

    from django import forms
    from .models import Post


    class PostForm(forms.ModelForm):

        class Meta:

            model = Post

            fields = [
                "title",
                "author",
                "content",
                "image",
            ]


============================================================
PART 14 — CRUD
============================================================

CRUD means:

    C = Create
    R = Read
    U = Update
    D = Delete

The Blog will eventually have:

    post_list()       -> Read all posts
    post_detail()     -> Read one post
    post_create()     -> Create
    post_update()     -> Update
    post_delete()     -> Delete


Do not introduce all four operations until students
understand the basic form and model flow.


============================================================
DEBUGGING CHECKLIST
============================================================

If the page does not work, check these in order:

1. Is the virtual environment active?

2. Is Django installed?

3. Is blogapp inside INSTALLED_APPS?

4. Did the model change?

5. Did you run makemigrations?

6. Did you run migrate?

7. Is the URL correct?

8. Is the view name correct?

9. Does the template exist?

10. Is the template path correct?

11. Did you use {% load static %}?

12. Is STATICFILES_DIRS correct?

13. Is MEDIA_ROOT correct?

14. Is MEDIA_URL correct?

15. Did you include static() in project urls.py?

16. Does the image field exist in the model?

17. Did you run migrations after adding the image field?

18. For image forms, is enctype="multipart/form-data" present?

19. For image uploads in a view, is request.FILES being passed?


============================================================
THE CORE DJANGO FLOW
============================================================

Students should remember this:

    Browser
       |
       v
      URL
       |
       v
      View
       |
       v
     Model
       |
       v
    Database
       |
       v
      View
       |
       v
   Template
       |
       v
    Browser


The project grows one topic at a time.

Do not introduce advanced concepts until the current
concept is working correctly.

# This file intentionally contains the teaching notes and code examples
# as comments/docstrings so it can remain a valid Python file.
#
# The actual Django code belongs in the appropriate project files:
#
# models.py
# views.py
# forms.py
# urls.py
# settings.py
# admin.py
#
# HTML belongs in templates/
# CSS belongs in static/css/
#
# Keep this file as the main teaching reference and update it as
# new Django topics are introduced.


============================================================
PART 15 — DJANGO REST FRAMEWORK (DRF) AND SERIALIZERS
============================================================

This is the next stage of the Blog project.

At this point, students should already understand:

    Models
    Databases
    Migrations
    Admin
    URLs
    Views
    Templates
    Static files
    Media files

The new goal is to expose the Blog data through an API.

The basic flow is:

    Model
       |
       v
    Serializer
       |
       v
    API View
       |
       v
      URL
       |
       v
      JSON


------------------------------------------------------------
STEP 1 — INSTALL DJANGO REST FRAMEWORK
------------------------------------------------------------

Make sure the virtual environment is active.

Run:

    pip install djangorestframework

Then update requirements.txt:

    pip freeze > requirements.txt


------------------------------------------------------------
STEP 2 — ADD DRF TO INSTALLED_APPS
------------------------------------------------------------

File:

    myproject/settings.py

Add:

    "rest_framework",

Example:

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",

        "rest_framework",

        "blogapp",
    ]


------------------------------------------------------------
STEP 3 — CREATE serializers.py
------------------------------------------------------------

Inside blogapp create:

    serializers.py

Add:

    from rest_framework import serializers

    from .models import Post


    # ModelSerializer automatically creates serializer fields
    # from the fields defined in the Post model.
    class PostSerializer(serializers.ModelSerializer):

        class Meta:

            # Tell Django REST Framework which model to use.
            model = Post

            # These model fields will be included in the API.
            fields = [
                "id",
                "title",
                "author",
                "content",
                "image",
                "created_at",
                "updated_at",
            ]


------------------------------------------------------------
WHAT IS A SERIALIZER?
------------------------------------------------------------

A serializer converts Django model data into a format that
can be sent through an API.

For example:

    Django Post object
            |
            v
       PostSerializer
            |
            v
          JSON

A serializer can also validate incoming data before it is
saved to the database.

Simple idea:

    Model <----> Serializer <----> JSON


------------------------------------------------------------
STEP 4 — CREATE THE FIRST API VIEW
------------------------------------------------------------

File:

    blogapp/views.py

Keep the existing website views.

Add the DRF imports:

    from rest_framework.views import APIView
    from rest_framework.response import Response

    from .serializers import PostSerializer


Then add:

    class PostListAPIView(APIView):

        def get(self, request):

            posts = Post.objects.all().order_by("-created_at")

            serializer = PostSerializer(
                posts,
                many=True
            )

            return Response(serializer.data)


------------------------------------------------------------
UNDERSTANDING THE API VIEW
------------------------------------------------------------

This gets the posts:

    posts = Post.objects.all()

This sends the posts through the serializer:

    serializer = PostSerializer(
        posts,
        many=True
    )

many=True is used because we are serializing multiple
objects.

This returns the data:

    return Response(serializer.data)


------------------------------------------------------------
STEP 5 — ADD THE API URL
------------------------------------------------------------

File:

    blogapp/urls.py

Add:

    # API endpoint for retrieving all blog posts.
    path(
        "api/posts/",
        views.PostListAPIView.as_view(),
        name="api_posts"
    )


The complete file can look like:

    from django.urls import path

    from . import views


    urlpatterns = [

        path(
            "",
            views.post_list,
            name="post_list"
        ),

        path(
            "post/<int:post_id>/",
            views.post_detail,
            name="post_detail"
        ),

        path(
            "api/posts/",
            views.PostListAPIView.as_view(),
            name="api_posts"
        ),
    ]


------------------------------------------------------------
STEP 6 — TEST THE API
------------------------------------------------------------

Run:

    python manage.py runserver

Open:

    http://127.0.0.1:8000/api/posts/

If there are posts in the database, DRF will return them
as JSON.

Example:

    [
        {
            "id": 1,
            "title": "My First Post",
            "author": "John",
            "content": "Learning Django",
            "image": null,
            "created_at": "...",
            "updated_at": "..."
        }
    ]


------------------------------------------------------------
STEP 7 — CREATE A DETAIL API
------------------------------------------------------------

Once the list endpoint works, create an endpoint for one post.

File:

    blogapp/views.py

Make sure this import exists:

    from django.shortcuts import get_object_or_404

Add:

    class PostDetailAPIView(APIView):

        def get(self, request, post_id):

            # Find one post using the ID from the URL.
            # Return a 404 response if the post does not exist.
            post = get_object_or_404(
                Post,
                id=post_id
            )

            # Serialize one Post object.
            serializer = PostSerializer(post)

            # Return the post as JSON.
            return Response(serializer.data)


------------------------------------------------------------
STEP 8 — ADD THE DETAIL URL
------------------------------------------------------------

File:

    blogapp/urls.py

Add:

    # API endpoint for retrieving one blog post.
    path(
        "api/posts/<int:post_id>/",
        views.PostDetailAPIView.as_view(),
        name="api_post_detail"
    )


------------------------------------------------------------
STEP 9 — TEST THE DETAIL API
------------------------------------------------------------

If post ID 1 exists, open:

    http://127.0.0.1:8000/api/posts/1/

You should receive one post as JSON.


------------------------------------------------------------
STEP 10 — INTRODUCE POST REQUESTS
------------------------------------------------------------

After students understand GET, introduce POST.

GET:

    Retrieves data.

POST:

    Sends data to the server to create data.

Update the API view:

    class PostListCreateAPIView(APIView):

        def get(self, request):

            # Get all posts from the database.
            posts = Post.objects.all().order_by("-created_at")

            # Convert the list of posts into API data.
            serializer = PostSerializer(
                posts,
                many=True
            )

            return Response(serializer.data)


        def post(self, request):

            # request.data contains the JSON sent by the client.
            serializer = PostSerializer(
                data=request.data
            )

            # Validate the submitted data before saving it.
            if serializer.is_valid():

                # Create the Post object in the database.
                serializer.save()

                # HTTP 201 means the object was created successfully.
                return Response(
                    serializer.data,
                    status=201
                )

            # Return validation errors if the data is not valid.
            return Response(
                serializer.errors,
                status=400
            )


------------------------------------------------------------
STEP 11 — TEST POST WITH POSTMAN
------------------------------------------------------------

Method:

    POST

URL:

    http://127.0.0.1:8000/api/posts/

JSON body:

    {
        "title": "My API Post",
        "author": "John",
        "content": "This post was created using the API."
    }

If the data is valid:

    serializer.save()

creates the Post in the database.


------------------------------------------------------------
STEP 12 — UNDERSTAND SERIALIZER VALIDATION
------------------------------------------------------------

The serializer checks incoming data.

For example, if title is required but missing:

    {
        "title": [
            "This field is required."
        ]
    }

This gives the API a consistent way to validate data.


------------------------------------------------------------
STEP 13 — ADD CRUD OPERATIONS GRADUALLY
------------------------------------------------------------

Once GET and POST are understood, introduce:

    GET
        Read

    POST
        Create

    PUT
        Update the object

    PATCH
        Update part of the object

    DELETE
        Delete the object


The eventual API can have:

    GET     /api/posts/
        List posts

    POST    /api/posts/
        Create post

    GET     /api/posts/1/
        Get one post

    PUT     /api/posts/1/
        Update post

    PATCH   /api/posts/1/
        Partially update post

    DELETE  /api/posts/1/
        Delete post


Do not teach all of these in the first DRF lesson.


------------------------------------------------------------
DRF CHECKPOINT
------------------------------------------------------------

Before moving to more advanced DRF topics, students should
be able to:

    1. Explain what an API is.
    2. Explain what JSON is.
    3. Install Django REST Framework.
    4. Add rest_framework to INSTALLED_APPS.
    5. Explain the purpose of a serializer.
    6. Create a ModelSerializer.
    7. Create a simple APIView.
    8. Create a GET endpoint.
    9. Return serialized data.
    10. Test an endpoint in a browser.
    11. Test an endpoint with Postman.
    12. Explain GET and POST.
    13. Create a database record through POST.
    14. Understand serializer validation.


============================================================
RECOMMENDED DRF PROGRESSION
============================================================

Teach the DRF section one topic at a time.

    Topic 1
        What is an API?

    Topic 2
        Install DRF

    Topic 3
        Serializers

    Topic 4
        APIView

    Topic 5
        GET

    Topic 6
        POST

    Topic 7
        Serializer validation

    Topic 8
        Detail endpoints

    Topic 9
        PUT and PATCH

    Topic 10
        DELETE

    Topic 11
        Generic API views

    Topic 12
        ViewSets

    Topic 13
        Routers

    Topic 14
        Authentication

    Topic 15
        Permissions

    Topic 16
        Pagination

    Topic 17
        Filtering and searching

    Topic 18
        Connecting a frontend or mobile application


============================================================
BLOG PROJECT AS THE SINGLE PRACTICAL PROJECT
============================================================

The Blog remains the same project.

Each topic adds a new capability:

    Models
        -> Store Blog data

    Templates
        -> Display Blog data

    Static files
        -> Style the Blog

    Media files
        -> Add Blog images

    DRF
        -> Expose Blog data through an API

    Authentication
        -> Control API access

    Permissions
        -> Control what users can do

    Frontend integration
        -> Consume the Blog API


============================================================
CURRENT PROJECT CHECKPOINT
============================================================

Completed:

    [x] Virtual environment
    [x] Django installation
    [x] Project and app
    [x] Models
    [x] Migrations
    [x] Django Admin
    [x] URLs
    [x] Views
    [x] Templates
    [x] Static files
    [x] Media files

Current scheme topic:

    [x] Django REST Framework
    [x] Serializers
    [x] Basic APIView
    [x] GET endpoint
    [x] Detail endpoint
    [x] Introduction to POST

Coming next:

    [ ] PUT
    [ ] PATCH
    [ ] DELETE
    [ ] Generic API Views
    [ ] ViewSets
    [ ] Routers
    [ ] Authentication
    [ ] Permissions
    [ ] Pagination
    [ ] Filtering
    [ ] Frontend/API integration


============================================================
CORE API FLOW
============================================================

For reading data:

    Client
       |
       v
      URL
       |
       v
    API View
       |
       v
      Model
       |
       v
    Database
       |
       v
    Serializer
       |
       v
      JSON
       |
       v
    Client


For creating data:

    Client
       |
       v
      JSON
       |
       v
    API View
       |
       v
    Serializer
       |
       v
    Validation
       |
       v
      Model
       |
       v
    Database


The same Blog project can now support both normal Django
HTML pages and API clients such as React, React Native,
Postman, or another application.


============================================================
HOW TO USE THIS GUIDE IN VS CODE
============================================================

The examples in this guide are written so you can work directly
inside the Django project.

Do not paste the whole guide into views.py or serializers.py.

Use the filename headings to know where each code block belongs.

For example:

    blogapp/models.py
        -> Put model code here.

    blogapp/serializers.py
        -> Put serializer code here.

    blogapp/views.py
        -> Put API view code here.

    blogapp/urls.py
        -> Put API URL code here.

    myproject/settings.py
        -> Put DRF configuration here.

The comments inside the code explain the purpose of important lines.
Students can read the comments while you explain the code.


------------------------------------------------------------
VS CODE WORKFLOW
------------------------------------------------------------

For each new topic:

    1. Open the correct file in VS Code.

    2. Add only the code needed for that lesson.

    3. Read the comments with the students.

    4. Save the file.

    5. Run the required command.

    6. Test the feature.

    7. Fix any errors before moving to the next topic.

For DRF, the first checkpoint should be:

    settings.py
        |
        v
    serializers.py
        |
        v
    views.py
        |
        v
    urls.py
        |
        v
    Browser / Postman
        |
        v
    JSON response


============================================================
DEBUGGING CHECKLIST FOR DRF
============================================================

If the API does not work, check:

    1. Is the virtual environment active?

    2. Is djangorestframework installed?

    3. Is "rest_framework" in INSTALLED_APPS?

    4. Does serializers.py exist?

    5. Is Post imported correctly?

    6. Does PostSerializer use the correct model?

    7. Are the serializer fields correct?

    8. Is the API view imported correctly?

    9. Does the URL point to the correct view?

    10. Did you use .as_view() with APIView?

    11. Does the requested Post ID exist?

    12. Are there records in the database?

    13. For POST, is the request body valid JSON?

    14. Are the required fields included?

    15. Is serializer.is_valid() being checked?

    16. Is serializer.save() being called after validation?



"""

# This file is a teaching reference.
