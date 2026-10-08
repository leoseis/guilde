"""
DJANGO BLOG API
FILTERING, SEARCHING, ORDERING & PAGINATION
============================================

PRACTICAL IMPLEMENTATION GUIDE

This guide is for the existing Blog project.

Current API:
    GET  /api/posts/
    POST /api/posts/
    GET  /api/posts/<id>/

We are now adding:
    1. Filtering
    2. Searching
    3. Ordering
    4. Pagination

The goal is to implement each feature gradually and test it
before moving to the next one.
"""

# ================================================================
# STEP 1 — UNDERSTAND THE FOUR FEATURES
# ================================================================

"""
Imagine the Blog database has 100 posts.

Instead of returning all 100 posts every time:

    GET /api/posts/

we want the client to control the results.

FILTERING
---------
"Give me posts written by John."

    /api/posts/?author=John


SEARCHING
---------
"Find posts containing the word Django."

    /api/posts/?search=django


ORDERING
--------
"Show the newest posts first."

    /api/posts/?ordering=-created_at


PAGINATION
----------
"Give me only 5 posts at a time."

    /api/posts/?page=2


Easy way to remember:

    FILTER  = narrow the results
    SEARCH  = find text
    ORDER   = arrange results
    PAGE    = split results
"""


# ================================================================
# STEP 2 — INSTALL django-filter
# ================================================================

"""
Open the terminal while the virtual environment is activated.

Run:

    pip install django-filter

Then update requirements.txt:

    pip freeze > requirements.txt

Do not put these commands inside views.py.
They are terminal commands.
"""


# ================================================================
# STEP 3 — ADD django-filter TO settings.py
# ================================================================

"""
Open:

    myproject/settings.py

Find INSTALLED_APPS.

Add:

    "django_filters",

Example:

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",

        "rest_framework",
        "django_filters",

        "myapp",
    ]

The important part is:

    "django_filters"

"""


# ================================================================
# STEP 4 — CONFIGURE PAGINATION
# ================================================================

"""
Still in:

    myproject/settings.py

Find your REST_FRAMEWORK setting.

If you already have REST_FRAMEWORK because of JWT,
DO NOT create a second REST_FRAMEWORK dictionary.

Add the pagination setting to the existing dictionary.

Example:

    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ),

        "DEFAULT_PAGINATION_CLASS":
            "rest_framework.pagination.PageNumberPagination",

        "PAGE_SIZE": 5,
    }

The important setting is:

    "PAGE_SIZE": 5

It means DRF will normally return 5 posts per page.

For example, if there are 12 posts:

    Page 1 -> 5 posts
    Page 2 -> 5 posts
    Page 3 -> 2 posts
"""


# ================================================================
# STEP 5 — WHY WE WILL USE GENERIC VIEWS
# ================================================================

"""
Earlier we wrote our API manually using APIView:

    class PostListCreateAPIView(APIView):

        def get(self, request):
            ...

        def post(self, request):
            ...

That was useful for learning.

Now we want filtering, searching, ordering and pagination.

DRF's generic view can handle the basic GET and POST operations
for us.

We will use:

    generics.ListCreateAPIView

It provides:

    GET
        List objects.

    POST
        Create an object.

This allows us to concentrate on the new features.
"""


# ================================================================
# STEP 6 — UPDATE views.py IMPORTS
# ================================================================

"""
Open:

    myapp/views.py

Add these imports:

    from rest_framework import generics

    from django_filters.rest_framework import DjangoFilterBackend

    from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )

Keep your existing imports for Post and PostSerializer:

    from .models import Post
    from .serializers import PostSerializer
"""


# ================================================================
# STEP 7 — CREATE THE NEW LIST/CREATE VIEW
# ================================================================

"""
Replace the old PostListCreateAPIView with this version:

    class PostListCreateAPIView(generics.ListCreateAPIView):

        queryset = Post.objects.all()

        serializer_class = PostSerializer

        filter_backends = [
            DjangoFilterBackend,
            SearchFilter,
            OrderingFilter,
        ]

        filterset_fields = [
            "author",
        ]

        search_fields = [
            "title",
            "content",
            "author",
        ]

        ordering_fields = [
            "title",
            "created_at",
        ]

        ordering = [
            "-created_at",
        ]

Do not type all of this at once in class.

Build it gradually and test after each section.
"""


# ================================================================
# STEP 8 — UNDERSTAND queryset
# ================================================================

"""
This:

    queryset = Post.objects.all()

means:

    "This API works with Post objects."

Django gets the Post records from the database.

Simple flow:

    Database
        |
        v
    Post.objects.all()
        |
        v
    queryset
"""


# ================================================================
# STEP 9 — UNDERSTAND serializer_class
# ================================================================

"""
This:

    serializer_class = PostSerializer

tells DRF:

    "Use PostSerializer when converting Post objects
     into API data and when validating incoming data."

We already learned this in the earlier Blog API lesson.
"""


# ================================================================
# STEP 10 — ENABLE THE THREE FEATURES
# ================================================================

"""
This:

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

activates:

    DjangoFilterBackend
        -> filtering

    SearchFilter
        -> searching

    OrderingFilter
        -> ordering
"""


# ================================================================
# STEP 11 — FILTERING
# ================================================================

"""
Add:

    filterset_fields = [
        "author",
    ]

This says:

    "Allow the client to filter using the author field."

If the database contains:

    John
    John
    Mary
    Peter

the client can request:

    GET /api/posts/?author=John

and receive John's posts.

IMPORTANT:
-----------
The field name must match your Post model.

If your model has:

    author = models.CharField(...)

then:

    filterset_fields = ["author"]

is correct.

If your model uses:

    author = models.ForeignKey(User, ...)

then the filtering setup is different and you may use:

    filterset_fields = ["author"]

or a specific related field such as:

    filterset_fields = ["author__username"]

depending on what you want to filter by.
"""


# ================================================================
# STEP 12 — TEST FILTERING
# ================================================================

"""
Start the server:

    python manage.py runserver

Test:

    http://127.0.0.1:8000/api/posts/?author=John

If it works, only John's posts should appear.

If you get all posts, check:

    1. django_filters is installed.
    2. django_filters is in INSTALLED_APPS.
    3. DjangoFilterBackend is in filter_backends.
    4. "author" matches your model field.
"""


# ================================================================
# STEP 13 — SEARCHING
# ================================================================

"""
Add:

    search_fields = [
        "title",
        "content",
        "author",
    ]

This tells DRF which fields can be searched.

Now:

    GET /api/posts/?search=django

can search:

    title
    content
    author

The search term is supplied after:

    ?search=
"""


# ================================================================
# STEP 14 — TEST SEARCHING
# ================================================================

"""
Try:

    http://127.0.0.1:8000/api/posts/?search=django

If a post contains Django in its title or content,
it can be included in the results.

Example:

    title:
        Learning Django REST Framework

Searching:

    ?search=django

can find it.
"""


# ================================================================
# STEP 15 — ORDERING
# ================================================================

"""
Add:

    ordering_fields = [
        "title",
        "created_at",
    ]

This tells DRF which fields clients are allowed to use
for ordering.

Example:

    /api/posts/?ordering=title

means:

    Sort by title in ascending order.


Example:

    /api/posts/?ordering=-title

means:

    Sort by title in descending order.


Example:

    /api/posts/?ordering=-created_at

means:

    Show the newest posts first.

IMPORTANT:
-----------
A minus sign means descending order.

    created_at
        ascending

    -created_at
        descending
"""


# ================================================================
# STEP 16 — DEFAULT ORDERING
# ================================================================

"""
Add:

    ordering = [
        "-created_at",
    ]

This is the default ordering.

So if the client simply requests:

    /api/posts/

the newest posts will normally appear first.

The client can still override it:

    /api/posts/?ordering=title
"""


# ================================================================
# STEP 17 — PAGINATION
# ================================================================

"""
Pagination is already configured in settings.py:

    "DEFAULT_PAGINATION_CLASS":
        "rest_framework.pagination.PageNumberPagination",

    "PAGE_SIZE": 5,

Now:

    GET /api/posts/

does not have to return every post.

If there are 20 posts:

    /api/posts/?page=1
    /api/posts/?page=2
    /api/posts/?page=3
    /api/posts/?page=4

Each page contains up to 5 posts.
"""


# ================================================================
# STEP 18 — UNDERSTAND A PAGINATED RESPONSE
# ================================================================

"""
Instead of receiving only a list:

    [
        {...},
        {...}
    ]

you will normally receive something like:

    {
        "count": 20,
        "next": "...",
        "previous": null,
        "results": [
            {...},
            {...}
        ]
    }

count
-----
Total number of matching posts.

next
----
Link to the next page.

previous
--------
Link to the previous page.

results
-------
The posts on the current page.
"""


# ================================================================
# STEP 19 — urls.py
# ================================================================

"""
Good news:

You do NOT need a new URL for filtering, searching,
ordering or pagination.

Keep your existing route:

    path(
        "api/posts/",
        views.PostListCreateAPIView.as_view(),
        name="api_posts"
    )

The query parameters control the results.

Examples:

    /api/posts/

    /api/posts/?author=John

    /api/posts/?search=django

    /api/posts/?ordering=-created_at

    /api/posts/?page=2
"""


# ================================================================
# STEP 20 — COMBINING FEATURES
# ================================================================

"""
Query parameters can be combined.

Example:

    /api/posts/?author=John&search=django

Meaning:

    "Find posts by John that match Django."


Another:

    /api/posts/?search=django&ordering=-created_at

Meaning:

    "Search for Django and show newest matching posts first."


All together:

    /api/posts/?author=John&search=django&ordering=-created_at&page=2

Meaning:

    1. Filter by author.
    2. Search for Django.
    3. Order newest first.
    4. Return page 2.

Multiple query parameters are joined with:

    &
"""


# ================================================================
# STEP 21 — CREATE TEST DATA
# ================================================================

"""
Filtering and searching are easier to understand when you have
several posts.

Create at least 5 posts.

Example:

    Post 1
        title = Django Introduction
        author = John

    Post 2
        title = React and Django
        author = Mary

    Post 3
        title = Django REST Framework
        author = John

    Post 4
        title = Python Basics
        author = Peter

    Post 5
        title = Building APIs
        author = Mary

You can create them through Django Admin or your POST endpoint.
"""


# ================================================================
# STEP 22 — CLASSROOM TESTING ORDER
# ================================================================

"""
Do not teach all four features at the same time.

Use this order:

TEST 1 — Normal list

    GET /api/posts/


TEST 2 — Filtering

    GET /api/posts/?author=John


TEST 3 — Searching

    GET /api/posts/?search=django


TEST 4 — Ordering

    GET /api/posts/?ordering=-created_at


TEST 5 — Pagination

    GET /api/posts/?page=2


TEST 6 — Combine them

    GET /api/posts/?search=django&ordering=-created_at
"""


# ================================================================
# STEP 23 — COMMON ERRORS
# ================================================================

"""
ERROR 1
-------
ModuleNotFoundError:
No module named 'django_filters'

FIX:

    pip install django-filter


ERROR 2
-------
You installed django-filter but Django still cannot use it.

CHECK settings.py:

    "django_filters"

must be inside:

    INSTALLED_APPS


ERROR 3
-------
Filtering does not work.

CHECK:

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

and:

    filterset_fields = [
        "author",
    ]


ERROR 4
-------
Search does not work.

CHECK:

    search_fields = [
        "title",
        "content",
        "author",
    ]


ERROR 5
-------
Ordering does not work.

Check that the requested field is included:

    ordering_fields = [
        "title",
        "created_at",
    ]

Then use exactly:

    ?ordering=title

or:

    ?ordering=-created_at


ERROR 6
-------
Pagination does not appear.

Check settings.py:

    "DEFAULT_PAGINATION_CLASS":
        "rest_framework.pagination.PageNumberPagination",

    "PAGE_SIZE": 5,


ERROR 7
-------
You have two REST_FRAMEWORK dictionaries.

Do NOT do this:

    REST_FRAMEWORK = {
        ...
    }

    REST_FRAMEWORK = {
        ...
    }

Put all DRF settings into one REST_FRAMEWORK dictionary.


ERROR 8
-------
The view still uses APIView.

For this lesson, change the list/create view to:

    generics.ListCreateAPIView

"""


# ================================================================
# STEP 24 — FINAL views.py VERSION
# ================================================================

"""
After teaching the individual parts, the important final view
should look like this:

    from rest_framework import generics
    from django_filters.rest_framework import DjangoFilterBackend
    from rest_framework.filters import SearchFilter, OrderingFilter

    from .models import Post
    from .serializers import PostSerializer


    class PostListCreateAPIView(generics.ListCreateAPIView):

        queryset = Post.objects.all()

        serializer_class = PostSerializer

        filter_backends = [
            DjangoFilterBackend,
            SearchFilter,
            OrderingFilter,
        ]

        filterset_fields = [
            "author",
        ]

        search_fields = [
            "title",
            "content",
            "author",
        ]

        ordering_fields = [
            "title",
            "created_at",
        ]

        ordering = [
            "-created_at",
        ]

Notice that GET and POST methods are no longer written manually.

ListCreateAPIView handles the basic GET and POST behaviour.
"""


# ================================================================
# STEP 25 — WHAT THE STUDENTS SHOULD UNDERSTAND
# ================================================================

"""
FILTERING
---------
Narrow results based on a field.

    ?author=John


SEARCHING
---------
Find text in configured fields.

    ?search=django


ORDERING
--------
Arrange the results.

    ?ordering=-created_at


PAGINATION
----------
Split a large result into pages.

    ?page=2


QUERY PARAMETER
---------------
The value after ? in a URL.

Example:

    /api/posts/?search=django

    search = parameter name
    django = parameter value


FINAL MEMORY TRICK
------------------

    FILTER  = narrow
    SEARCH  = find
    ORDER   = arrange
    PAGE    = split
"""


# ================================================================
# CLASS EXERCISE
# ================================================================

"""
EXERCISE 1
----------
Create 5 or more blog posts using at least two authors.


EXERCISE 2
----------
Return only posts written by John.

    /api/posts/?author=John


EXERCISE 3
----------
Search for the word Django.

    /api/posts/?search=django


EXERCISE 4
----------
Show the newest posts first.

    /api/posts/?ordering=-created_at


EXERCISE 5
----------
Open page 2.

    /api/posts/?page=2


EXERCISE 6
----------
Combine search and ordering.

    /api/posts/?search=django&ordering=-created_at


EXERCISE 7
----------
Explain to the class the difference between:

    filtering
    searching
    ordering
    pagination
"""


# ================================================================
# FINAL API REFERENCE
# ================================================================

"""
FILTER:
    GET /api/posts/?author=John

SEARCH:
    GET /api/posts/?search=django

ORDER:
    GET /api/posts/?ordering=-created_at

PAGE:
    GET /api/posts/?page=2

COMBINE:
    GET /api/posts/?author=John&search=django&ordering=-created_at&page=2


MAIN IDEA:

    Client
       |
       | query parameters
       v
    Blog API
       |
       +--> Filter
       |
       +--> Search
       |
       +--> Order
       |
       +--> Paginate
       |
       v
    Useful results
"""

# This file is intentionally a valid Python teaching file.
# The examples are inside a documentation string so VS Code will
# not treat Django settings, URLs, or terminal commands as Python.
