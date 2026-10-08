# 1. First install DRF

# Your terminal already shows:

# (venv)

# So your virtual environment is active.

# Run:

# pip install djangorestframework

# Then:

# pip freeze > requirements.txt
# 2. Add DRF to settings.py

# Open:

# myproject/settings.py

Find:

INSTALLED_APPS = [

Add:

"rest_framework",

For example:

INSTALLED_APPS = [

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Django REST Framework
    "rest_framework",

    # Our blog application
    "myapp",
]

If myapp is already there, don't add it twice.

3. Check your model first

Before creating a serializer, we need a model.

Open:

myapp/models.py

If you haven't created your Blog model yet, use:

from django.db import models


class Post(models.Model):

    # The title of the blog post
    title = models.CharField(max_length=200)

    # The person who wrote the post
    author = models.CharField(max_length=100)

    # The main content of the post
    content = models.TextField()

    # Automatically records when the post was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Show the title when viewing the object in Admin
        return self.title

Then run:

python manage.py makemigrations

and:

python manage.py migrate

If your Post model already exists, don't recreate it. We will use the model you already have.

4. Create serializers.py

Inside myapp, create:

myapp/
├── admin.py
├── apps.py
├── models.py
├── serializers.py   ← NEW
├── urls.py
└── views.py

Open:

myapp/serializers.py

Put:

from rest_framework import serializers

from .models import Post


# This serializer converts Post objects into JSON data.
class PostSerializer(serializers.ModelSerializer):

    class Meta:

        # Tell DRF which model we are working with.
        model = Post

        # These are the fields we want to expose through the API.
        fields = [
            "id",
            "title",
            "author",
            "content",
            "created_at",
        ]

This is your first serializer.

5. What did the serializer do?

Your database contains something like:

Post
-------------------------
id       1
title    My First Post
author   John
content  Hello Django

The serializer converts that into something an API can send:

{
    "id": 1,
    "title": "My First Post",
    "author": "John",
    "content": "Hello Django",
    "created_at": "2026-09-28T14:30:00Z"
}

So we have 

DATABASE
    ↓
MODEL
    ↓
SERIALIZER
    ↓
JSON
    ↓
CLIENT

That's the main concept for this lesson.

6. Create your first API view

Now open:

myapp/views.py

Don't remove your existing home() yet.

We can have both normal Django and DRF views.

Use:

from django.shortcuts import render

from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


# Normal Django view
def home(request):

    return HttpResponse(
        "Hello world my django is working"
    )


# DRF API view
class PostListAPIView(APIView):

    def get(self, request):

        # Get all blog posts from the database.
        posts = Post.objects.all()

        # Convert the Django objects into JSON-ready data.
        # many=True is required because we have multiple posts.
        serializer = PostSerializer(
            posts,
            many=True
        )

        # Send the serialized data back to the client.
        return Response(serializer.data)

Notice that we're not replacing Django views.

We're adding an API view.

7. Connect the API to a URL

Open:

myapp/urls.py

If you don't have anything important there yet:

from django.urls import path

from . import views


urlpatterns = [

    # Normal Django page
    path(
        "",
        views.home,
        name="home"
    ),

    # Blog API
    path(
        "api/posts/",
        views.PostListAPIView.as_view(),
        name="api_posts"
    ),
]

The important part is:

views.PostListAPIView.as_view()

Because PostListAPIView is a class-based DRF view.

8. Make sure the project knows about myapp.urls

Open:

myproject/urls.py

Use:

from django.contrib import admin

from django.urls import path, include


urlpatterns = [

    # Django Admin
    path(
        "admin/",
        admin.site.urls
    ),

    # URLs from our blog application
    path(
        "",
        include("myapp.urls")
    ),
]
9. Run the server
python manage.py runserver

First test:

http://127.0.0.1:8000/

You should still get:

Hello world my django is working

That proves we haven't broken your original Django view.

Now test:

http://127.0.0.1:8000/api/posts/

If you already have posts in your database, you should see something similar to:

[
    {
        "id": 1,
        "title": "My First Post",
        "author": "Leonard",
        "content": "Learning Django",
        "created_at": "2026-09-28T..."
    }
]

# That is your first Django REST API
















"""
DJANGO BLOG API — GET DETAIL + POST

This is a continuation of the same Blog project.

Already working:
    GET /api/posts/

We are adding:
    GET /api/posts/<id>/
    POST /api/posts/

Keep these responsibilities separate:

    models.py       -> database models
    serializers.py  -> serializers and validation
    views.py        -> API logic
    urls.py         -> URL routes
"""

# ================================================================
# 1. GET ONE BLOG POST
# ================================================================

"""
Goal:

    GET /api/posts/1/

This should return only the post whose ID is 1.

We use get_object_or_404() so that a missing post produces a
normal 404 response instead of an unhandled error.
"""

# ----------------------------------------------------------------
# myapp/views.py
# ----------------------------------------------------------------

# Add this import near the top of views.py:
from django.shortcuts import get_object_or_404

# These imports should already exist in your views.py:
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


class PostDetailAPIView(APIView):
    """
    API view for retrieving one blog post.
    """

    def get(self, request, post_id):
        # Find the post using the ID supplied in the URL.
        post = get_object_or_404(
            Post,
            id=post_id
        )

        # We are serializing ONE object,
        # so we do not use many=True.
        serializer = PostSerializer(post)

        # Return the post as JSON.
        return Response(serializer.data)


# ================================================================
# 2. ADD THE DETAIL URL
# ================================================================

"""
Open:

    myapp/urls.py

Add this inside the existing urlpatterns list:

    path(
        "api/posts/<int:post_id>/",
        views.PostDetailAPIView.as_view(),
        name="api_post_detail"
    )

IMPORTANT:
Do not create another urlpatterns list.
Add the route to the one you already have.
"""

# ----------------------------------------------------------------
# myapp/urls.py
# ----------------------------------------------------------------

# Example:
#
# urlpatterns = [
#
#     path(
#         "",
#         views.home,
#         name="home"
#     ),
#
#     path(
#         "api/posts/",
#         views.PostListAPIView.as_view(),
#         name="api_posts"
#     ),
#
#     path(
#         "api/posts/<int:post_id>/",
#         views.PostDetailAPIView.as_view(),
#         name="api_post_detail"
#     ),
# ]


# ================================================================
# 3. TEST GET DETAIL
# ================================================================

"""
Start the server:

    python manage.py runserver

Then open:

    http://127.0.0.1:8000/api/posts/1/

Use an ID that actually exists in your database.

If post 1 exists, you should receive one JSON object.

If it does not exist, you should receive:

    404 Not Found

That 404 is expected behaviour.
"""

# ================================================================
# 4. ADD POST — CREATE A NEW BLOG POST
# ================================================================

"""
We now want the same:

    /api/posts/

endpoint to support two operations:

    GET
        Get all posts.

    POST
        Create a new post.

The flow for POST is:

    Client
       |
       v
    request.data
       |
       v
    Serializer
       |
       v
    Validation
       |
       v
    serializer.save()
       |
       v
    Database
       |
       v
    Response
"""

# ----------------------------------------------------------------
# myapp/views.py
# ----------------------------------------------------------------

class PostListCreateAPIView(APIView):
    """
    API view for listing and creating blog posts.
    """

    def get(self, request):
        # Get all posts from the database.
        posts = Post.objects.all()

        # We have multiple objects, so use many=True.
        serializer = PostSerializer(
            posts,
            many=True
        )

        # Return all posts as JSON.
        return Response(serializer.data)

    def post(self, request):
        # request.data contains the data sent by the client.
        serializer = PostSerializer(
            data=request.data
        )

        # Check whether the submitted data is valid.
        if serializer.is_valid():

            # Save the validated data to the database.
            serializer.save()

            # HTTP 201 means "Created".
            return Response(
                serializer.data,
                status=201
            )

        # If validation fails, return the errors.
        # HTTP 400 means "Bad Request".
        return Response(
            serializer.errors,
            status=400
        )


# ================================================================
# 5. UPDATE THE LIST URL
# ================================================================

"""
In myapp/urls.py, find the existing route:

    path(
        "api/posts/",
        views.PostListAPIView.as_view(),
        name="api_posts"
    )

Change it to:

    path(
        "api/posts/",
        views.PostListCreateAPIView.as_view(),
        name="api_posts"
    )

Now:

    GET  /api/posts/
        -> gets all posts

    POST /api/posts/
        -> creates a new post
"""

# ----------------------------------------------------------------
# myapp/urls.py
# ----------------------------------------------------------------

# Example final urlpatterns:
#
# urlpatterns = [
#
#     path(
#         "",
#         views.home,
#         name="home"
#     ),
#
#     path(
#         "api/posts/",
#         views.PostListCreateAPIView.as_view(),
#         name="api_posts"
#     ),
#
#     path(
#         "api/posts/<int:post_id>/",
#         views.PostDetailAPIView.as_view(),
#         name="api_post_detail"
#     ),
# ]


# ================================================================
# 6. TEST POST
# ================================================================

"""
Use Postman, Thunder Client, Insomnia, or another API client.

METHOD:

    POST

URL:

    http://127.0.0.1:8000/api/posts/

Choose:

    Body
    -> raw
    -> JSON

Send:

    {
        "title": "My Second Blog Post",
        "author": "John",
        "content": "I created this post through the API."
    }

If successful, the API should return the newly created post.

The ID and created_at value will depend on your database.
"""

# ================================================================
# 7. UNDERSTANDING serializer.is_valid()
# ================================================================

"""
The serializer does more than convert data.

It also validates the data.

For example, if required fields are missing:

    {
        "title": "Incomplete Post"
    }

then:

    serializer.is_valid()

will normally return False.

This part of the code handles that safely:

    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=400)

Remember:

    is_valid() == True
        -> save the data

    is_valid() == False
        -> return validation errors
"""

# ================================================================
# 8. COMMON BEGINNER ERRORS
# ================================================================

"""
ERROR 1:
    NameError: get_object_or_404 is not defined

Fix:
    from django.shortcuts import get_object_or_404


ERROR 2:
    /api/posts/1/ returns 404

Possible reason:
    There is no post with ID 1.

Check:
    /api/posts/

Then use an ID that actually exists.


ERROR 3:
    A single post is returned as a list.

Check the serializer.

For ONE object:

    PostSerializer(post)

For MULTIPLE objects:

    PostSerializer(posts, many=True)


ERROR 4:
    POST returns 400 Bad Request.

This normally means the submitted data failed validation.

Read the response body. DRF normally tells you which field
has the problem.


ERROR 5:
    POST does not create a post.

Check that the URL is using:

    views.PostListCreateAPIView.as_view()

and not the old:

    views.PostListAPIView.as_view()


ERROR 6:
    ImportError involving PostSerializer.

Make sure serializers.py contains the serializer itself.

Correct separation:

    serializers.py
        -> PostSerializer

    views.py
        -> imports PostSerializer

Do NOT put this inside serializers.py:

    from .serializers import PostSerializer

That would create a circular import.


ERROR 7:
    The API URL returns Django's 404 page.

Check that myproject/urls.py includes:

    path("", include("myapp.urls"))

Also check the route inside myapp/urls.py.
"""


# ================================================================
# 9. CLASS PRACTICE
# ================================================================

"""
EXERCISE 1
----------

Create a new blog post using POST.

Use:

    title
    author
    content

Then use:

    GET /api/posts/

to confirm that it was created.


EXERCISE 2
----------

Copy the ID of the new post.

Use:

    GET /api/posts/<id>/

to retrieve only that post.


EXERCISE 3
----------

Try:

    GET /api/posts/9999/

Observe the response.

Question:

    Why did the API return 404?


EXERCISE 4
----------

Send incomplete POST data.

Example:

    {
        "title": "Incomplete Post"
    }

Observe the validation errors.

Question:

    Which required fields are missing?
"""


# ================================================================
# 10. QUICK REFERENCE
# ================================================================

"""
CURRENT API

GET ALL POSTS

    GET /api/posts/


GET ONE POST

    GET /api/posts/1/


CREATE POST

    POST /api/posts/


HTTP METHODS WE HAVE LEARNED

    GET
        Read data

    POST
        Create data


DATA FLOW — GET

    Database
        |
        v
      Model
        |
        v
    Serializer
        |
        v
       JSON
        |
        v
      Client


DATA FLOW — POST

      Client
        |
        v
       JSON
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
        |
        v
     Response


NEXT TOPICS — WE WILL ADD THESE LATER

    PUT
        Update the entire object.

    PATCH
        Update part of an object.

    DELETE
        Delete an object.

After that, we can move to:

    Generic Views
    ViewSets
    Routers
"""









