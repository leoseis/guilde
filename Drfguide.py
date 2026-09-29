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

So explain it to your students as:

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

That is your first Django REST API.