# ============================================================
# 1. STATIC FILES VS MEDIA FILES
# ============================================================

# STATIC FILES:
# Files supplied by the developer.
# Examples: CSS, JavaScript, logos, developer-created images.
#
# MEDIA FILES:
# Files uploaded by a user or administrator.
# Examples: blog pictures, profile pictures, documents.
#
# SIMPLE RULE:
# STATIC = developer supplies it.
# MEDIA  = user/admin uploads it.


# ============================================================
# 2. STATIC FILES - PROJECT STRUCTURE
# ============================================================

# At the project root create:
#
# blog/
# |-- myapp/
# |-- myproject/
# |-- static/
# |   `-- css/
# |       `-- style.css
# |-- manage.py
# `-- venv/


# ============================================================
# 3. STATIC FILES - settings.py
# ============================================================

# Open: myproject/settings.py
#
# Django normally already has:
#
# STATIC_URL = "static/"
#
# For a project-level static folder, add:
#
# STATICFILES_DIRS = [
#     BASE_DIR / "static",
# ]
#
# EXPLANATION:
# STATIC_URL tells Django the URL prefix for static files.
# STATICFILES_DIRS tells Django where the project's static folder is.
#
# COMMON ERROR:
# Do not write the following inside models.py or views.py.
# These settings belong in myproject/settings.py.


# ============================================================
# 4. STATIC CSS - style.css
# ============================================================

# Create:
#     static/css/style.css
#
# Example CSS:
#
# body {
#     font-family: Arial, sans-serif;
#     background-color: #f4f4f4;
#     margin: 0;
# }
#
# .post {
#     background-color: white;
#     padding: 20px;
#     margin-bottom: 20px;
# }
#
# .post-image {
#     width: 100%;
#     max-width: 600px;
#     height: auto;
# }
#
# IMPORTANT:
# This is CSS, NOT Python.
# Keep it in static/css/style.css.
# Do not paste CSS into a .py file when running the project.


# ============================================================
# 5. LOAD STATIC FILES IN HTML TEMPLATE
# ============================================================

# Open your HTML template, for example:
#     templates/myapp/base.html
#
# At the top of the HTML file:
#
# {% load static %}
#
# Inside <head>:
#
# <link rel="stylesheet" href="{% static 'css/style.css' %}">
#
# IMPORTANT:
# The lines above are Django Template Language and HTML.
# They are NOT Python.
# That is why they are comments in this guide.py file.
# Put them in the .html template in your real project.


# ============================================================
# 6. INSTALL PILLOW
# ============================================================

# Make sure the virtual environment is active.
#
# Linux/Mint:
#     source venv/bin/activate
#
# Install Pillow:
#     pip install pillow
#
# Update requirements:
#     pip freeze > requirements.txt
#
# WHY PILLOW?
# Django's ImageField uses Pillow to work with image files.
#
# COMMON ERROR:
# "Cannot use ImageField because Pillow is not installed"
# FIX:
#     pip install pillow


# ============================================================
# 7. ADD IMAGEFIELD TO models.py
# ============================================================

# Open: myapp/models.py
#
# Keep your existing Post model and add this field:
#
# from django.db import models
#
# class Post(models.Model):
#
#     # Blog post title.
#     title = models.CharField(max_length=200)
#
#     # Name of the author.
#     author = models.CharField(max_length=100)
#
#     # Main blog content.
#     content = models.TextField()
#
#     # Optional image for the blog post.
#     # upload_to="posts/" means uploads go into media/posts/.
#     image = models.ImageField(
#         upload_to="posts/",
#         blank=True,
#         null=True
#     )
#
#     # Automatically stores the creation date/time.
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         # Show the title in Django Admin.
#         return self.title
#
# IMPORTANT:
# Do not create a second Post class if you already have one.
# Add the image field to your existing Post model.


# ============================================================
# 8. MIGRATIONS
# ============================================================

# Because the model changed, update the database.
#
# Terminal:
#     python manage.py makemigrations
#     python manage.py migrate
#
# EXPLANATION:
# makemigrations = creates migration instructions.
# migrate       = applies those instructions to the database.
#
# COMMON ERROR:
# "no such column: ... image"
# Usually means the model changed but migrations were not applied.
# FIX:
#     python manage.py makemigrations
#     python manage.py migrate


# ============================================================
# 9. MEDIA SETTINGS - settings.py
# ============================================================

# Open: myproject/settings.py
#
# Add:
#
# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"
#
# EXPLANATION:
# MEDIA_URL is the URL prefix used by the browser.
# MEDIA_ROOT is the physical folder where uploaded files are stored.
#
# Example flow:
#     Image upload
#         -> ImageField
#         -> MEDIA_ROOT
#         -> media/posts/


# ============================================================
# 10. SERVE MEDIA DURING DEVELOPMENT - project urls.py
# ============================================================

# Open the PROJECT urls.py:
#     myproject/urls.py
#
# Do NOT confuse this with:
#     myapp/urls.py
#
# Use:
#
# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib import admin
# from django.urls import include, path
#
# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("", include("myapp.urls")),
# ]
#
# # Serve uploaded media during development.
# if settings.DEBUG:
#     urlpatterns += static(
#         settings.MEDIA_URL,
#         document_root=settings.MEDIA_ROOT
#     )
#
# IMPORTANT:
# This is for development with DEBUG=True.
# Production deployments normally use a proper media/static serving setup.
#
# COMMON ERROR:
# Image uploads successfully but opening the image gives 404.
# Check MEDIA_URL, MEDIA_ROOT, and the static(...) configuration above.


# ============================================================
# 11. ADMIN REGISTRATION
# ============================================================

# Open: myapp/admin.py
#
# Use:
#
# from django.contrib import admin
# from .models import Post
#
# # Register the actual model class, not a string.
# admin.site.register(Post)
#
# WRONG:
# admin.site.register("Post")
#
# CORRECT:
# admin.site.register(Post)
#
# The Post model should now appear in Django Admin.


# ============================================================
# 12. UPLOAD AN IMAGE THROUGH ADMIN
# ============================================================

# Run:
#     python manage.py runserver
#
# Open:
#     http://127.0.0.1:8000/admin/
#
# Create/edit a Post.
# Choose an image.
# Save.
#
# Django should create something similar to:
#
# media/
# `-- posts/
#     `-- django.jpg
#
# NOTE:
# The exact filename will depend on the image you upload.


# ============================================================
# 13. DISPLAY THE IMAGE IN AN HTML TEMPLATE
# ============================================================

# Open your post template, for example:
#     templates/myapp/post_list.html
#
# Inside your post loop:
#
# {% for post in posts %}
#     <article class="post">
#         <h2>{{ post.title }}</h2>
#         <p>By {{ post.author }}</p>
#
#         {% if post.image %}
#             <img
#                 src="{{ post.image.url }}"
#                 alt="{{ post.title }}"
#                 class="post-image"
#             >
#         {% endif %}
#
#         <p>{{ post.content }}</p>
#     </article>
# {% endfor %}
#
# WHY {% if post.image %}?
# It prevents the template from trying to display an image when
# the post does not have one.
#
# WHY {{ post.image.url }}?
# It gives the browser the URL of the uploaded image.
#
# IMPORTANT:
# This code belongs in an .html file, not in models.py or views.py.


# ============================================================
# 14. ADD IMAGE TO THE DRF SERIALIZER
# ============================================================

# Open: myapp/serializers.py
#
# Your serializer can include the image:
#
# from rest_framework import serializers
# from .models import Post
#
# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         # Tell DRF which model to serialize.
#         model = Post
#
#         # Include image in the API response.
#         fields = [
#             "id",
#             "title",
#             "author",
#             "content",
#             "image",
#             "created_at",
#         ]
#
# IMPORTANT:
# Do NOT import PostSerializer inside serializers.py.
#
# WRONG inside serializers.py:
#     from .serializers import PostSerializer
#
# That causes a circular import.
#
# The correct relationship is:
#     models.py -> serializers.py -> views.py -> urls.py


# ============================================================
# 15. WHAT THE API CAN RETURN
# ============================================================

# After an image exists, the API may return data similar to:
#
# {
#     "id": 1,
#     "title": "Learning Django",
#     "author": "John",
#     "content": "My first Django post.",
#     "image": "http://127.0.0.1:8000/media/posts/django.jpg",
#     "created_at": "2026-09-29T..."
# }
#
# This is JSON data returned by DRF.
#
# IMPORTANT:
# The exact URL can differ depending on your project and environment.


# ============================================================
# 16. MEDIA WITH DRF POST REQUESTS - LATER LESSON
# ============================================================

# For the first media lesson, use Django Admin to upload the image.
# This keeps the concept simple.
#
# Later, when teaching POST requests with images, introduce:
#     multipart/form-data
#
# In Postman:
#     Body -> form-data
#
# Fields:
#     title       Text
#     author      Text
#     content     Text
#     image       File
#
# Do not mix this into the first media explanation if students are
# still learning basic models and serializers.


# ============================================================
# 17. STATIC VS MEDIA - QUICK MEMORY TABLE
# ============================================================

# STATIC:
#     Created by developer
#     CSS
#     JavaScript
#     Developer-created logo
#     Example path: static/css/style.css
#
# MEDIA:
#     Uploaded by user/admin
#     Blog pictures
#     Profile pictures
#     Documents
#     Example path: media/posts/django.jpg


# ============================================================
# 18. COMMON ERRORS CHECKLIST
# ============================================================

# ERROR 1: Pillow is missing.
# FIX:
#     pip install pillow
#
# ERROR 2: Image field does not appear in Admin.
# CHECK:
#     - ImageField is in the existing Post model.
#     - python manage.py makemigrations
#     - python manage.py migrate
#     - Post is registered in admin.py.
#
# ERROR 3: Image uploads but gives 404 in browser.
# CHECK:
#     - MEDIA_URL = "/media/"
#     - MEDIA_ROOT = BASE_DIR / "media"
#     - project urls.py has the DEBUG/static(...) configuration.
#
# ERROR 4: CSS gives 404.
# CHECK:
#     - static/css/style.css exists.
#     - STATICFILES_DIRS points to BASE_DIR / "static".
#     - Template contains {% load static %}.
#     - Template uses {% static 'css/style.css' %}.
#
# ERROR 5: Circular import involving PostSerializer.
# WRONG:
#     from .serializers import PostSerializer
#     inside serializers.py
#
# CORRECT:
#     views.py imports PostSerializer.
#     serializers.py imports Post.
#     models.py defines Post.
#
# ERROR 6: Django says PostListAPIView does not exist.
# CHECK:
#     - PostListAPIView is defined in myapp/views.py.
#     - urls.py uses views.PostListAPIView.as_view().
#     - views.py imports APIView, Response, Post, and PostSerializer.


# ============================================================
# 19. COMPLETE MEDIA FLOW
# ============================================================

# ADMIN/USER
#     |
#     v
# UPLOAD IMAGE
#     |
#     v
# Post.image (ImageField)
#     |
#     v
# MEDIA_ROOT
#     |
#     v
# media/posts/image.jpg
#     |
#     v
# post.image.url
#     |
#     v
# BROWSER


# ============================================================
# 20. COMPLETE STATIC FLOW
# ============================================================

# DEVELOPER
#     |
#     v
# static/css/style.css
#     |
#     v
# settings.py
#     |
#     v
# {% load static %}
#     |
#     v
# {% static 'css/style.css' %}
#     |
#     v
# BROWSER


# ============================================================
# 21. PROJECT PROGRESSION
# ============================================================

# Your single Blog project can now teach topics gradually:
#
# 1. Virtual environment
# 2. Django installation
# 3. Project and app creation
# 4. URLs and views
# 5. Templates
# 6. Models
# 7. Migrations
# 8. Django Admin
# 9. Static files
# 10. Media files
# 11. DRF installation
# 12. Serializers
# 13. GET API
# 14. POST API
# 15. PUT/PATCH
# 16. DELETE
# 17. Generic views
# 18. ViewSets
# 19. Routers
# 20. Authentication and permissions


# ============================================================
# FINAL TEACHING RULE
# ============================================================

# If the developer creates it -> STATIC.
# If the user/admin uploads it -> MEDIA.
#
# Keep the same Blog project and add one concept at a time.
# That way students see how the pieces connect without having
# to build a completely different project for every topic.


if __name__ == "__main__":
    # This file is a teaching reference, not the Django server.
    print("Django Blog Static and Media teaching guide")
