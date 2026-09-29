"""
================================================================================
 BACKEND DEVELOPER TEACHING GUIDE  —  Python OOP + Django + DRF + System Design
================================================================================
SOURCE: github.com/victorchukwuemeka/digitafort  ->  backend/course/
Built directly from the real files in that folder (not invented).
This is a REFERENCE FILE, not a script to run. Keep it open in VS Code
while teaching and scroll/search (Ctrl+F) for the topic you need.

HOW THIS FILE IS ORGANIZED
    Each topic below follows the same simplified structure:
    TOPIC | SIMPLE EXPLANATION | WHY IT MATTERS | CODE EXAMPLE |
    HOW TO TEACH IT | COMMON MISTAKES | QUICK EXERCISE

    Search tags used in this file (Ctrl+F these):
    #M0  = Module 0: Python OOP
    #M1A = Module 1: Foundations
    #M1B = Module 1: Deep Dive (Auth, Middleware, etc.)
    #M1C = Module 1: DRF / APIs
    #M1D = Module 1: Testing & Performance
    #M2  = Module 2: System Design & Architecture

NOTE ON SCOPE: The repo's outline file also lists future modules —
"Web Hosting / Nginx / Apache2", "Distributed Systems", "CI Pipelines" —
but at the time of writing, NO lesson files exist yet for those. Only
titles appear in backend_course_outline.md. Do not teach these as if
content exists; tell students they are "coming soon" in the course repo.
================================================================================
"""

# ==============================================================================
# COURSE ROADMAP (order to teach, exactly as the repo's README lays it out)
# ==============================================================================
ROADMAP = """
Module 0 - Python Classes (OOP)                 00_python_classes/
Module 1 - Foundations (Web + Django)            01_fundamentals/
Module 1 - Deep Dive (Auth/Middleware/Users)     02_deep_dive/
Module 1 - DRF & APIs                            03_drf_apis/
Module 1 - Testing & Performance                 04_testing_performance/
Module 2 - System Design & Architecture          05_expert_topics/
"""


# ##############################################################################
# #M0   MODULE 0 — PYTHON CLASSES (OOP)     [source: 00_python_classes/README.md]
# ##############################################################################
"""
This is ONE long deep-dive guide in the repo (2000+ lines), covering OOP from
basics to advanced. Teach it as several short lessons, not one sitting.
"""

# ------------------------------------------------------------------------------
# TOPIC: Classes, Objects, and __init__  (repo section 1-2)
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    A class is a blueprint. An object is a real "thing" built from that
    blueprint. __init__ is the special method that runs automatically the
    moment you create a new object, and it's where you set up its starting
    data (its "state").

WHY IT MATTERS:
    Everything in Django is a class: Models, Views, Forms, Serializers.
    If students don't understand classes and __init__, Django will feel
    like magic instead of logic.

HOW TO TEACH IT:
    1. Draw a "Car" blueprint on the board (class) vs 3 actual cars (objects).
    2. Show that each object has its OWN data (instance variables) but can
       share behaviour (methods) defined once in the class.
    3. Introduce 'self' as "the specific object currently being used."
    4. Show class variables (shared by ALL objects) vs instance variables
       (unique per object) — this is a classic beginner confusion point.

COMMON MISTAKES:
    - Forgetting 'self' as the first parameter of every method.
    - Using a mutable default argument (e.g. def __init__(self, items=[])) —
      this list is SHARED across every object made without passing items!
      Fix: use None as default, then `items = items or []` inside.
    - Confusing class variables with instance variables and accidentally
      sharing data between objects.

QUICK EXERCISE:
    Ask students to write a `Book` class with title, author, and a method
    `describe()` that prints "TITLE by AUTHOR".
"""

class Book:
    # Code example for teaching
    def __init__(self, title, author):
        self.title = title      # instance variable (unique per object)
        self.author = author

    def describe(self):
        return f"{self.title} by {self.author}"

# demo:
# b1 = Book("Things Fall Apart", "Chinua Achebe")
# print(b1.describe())


# ------------------------------------------------------------------------------
# TOPIC: Inheritance, super(), and MRO  (repo section 3)
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    Inheritance lets one class (child) reuse the code of another class
    (parent). super() lets the child call the parent's version of a method
    instead of rewriting it. MRO (Method Resolution Order) is simply the
    ORDER Python checks classes when multiple inheritance is involved.

WHY IT MATTERS:
    Django's ClassBasedViews, Models, and DRF Serializers are ALL built on
    inheritance. Understanding `super().__init__()` is required to safely
    extend Django's built-in classes (e.g. custom User models, CBVs).

HOW TO TEACH IT:
    1. Start with a simple Animal -> Dog example (is-a relationship).
    2. Show what breaks if you forget to call super().__init__().
    3. Briefly mention MRO only as "the order Python looks things up" — no
       need to go deep for beginners.

COMMON MISTAKES:
    - Using inheritance when composition fits better (e.g. "Stack IS-A List"
      is wrong; "Stack HAS-A List" is correct — the repo explicitly warns
      about this).
    - Forgetting super().__init__() and losing the parent's setup logic.

QUICK EXERCISE:
    Create an `Animal` class with a `speak()` method, then a `Dog` class
    that inherits from it and overrides `speak()`.
"""

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"


# ------------------------------------------------------------------------------
# TOPIC: Encapsulation & @property  (repo section 4)
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    Encapsulation means protecting an object's internal data so it can only
    be changed in controlled ways. Python uses a naming convention
    (underscore prefix) rather than true "private" variables. @property lets
    you run validation logic when a value is read or set, while still
    looking like a normal attribute.

WHY IT MATTERS:
    In Django models and serializers you often need "computed" or
    "validated" fields — @property is the clean Pythonic way to do that.

CODE EXAMPLE:
"""

class Account:
    def __init__(self, balance):
        self._balance = balance   # "_" = convention for "don't touch directly"

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value

"""
COMMON MISTAKES:
    - Thinking a leading underscore truly blocks access (it doesn't — it's
      a convention only; Python still allows a.__dict__['_balance']).
QUICK EXERCISE:
    Add a @property called 'is_overdrawn' to Account that returns True if
    balance < 0.
"""


# ------------------------------------------------------------------------------
# TOPIC: Dunder Methods (__str__, __repr__, __eq__)  (repo section 5)
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    "Dunder" = Double UNDERscore. These are special methods Python calls
    automatically. __str__ controls what print(obj) shows. __eq__ controls
    what happens when you compare two objects with ==.

WHY IT MATTERS:
    Every Django model should define __str__ — it's what shows up in the
    Django admin list and in the shell, instead of an unhelpful
    "<Post object (1)>".

CODE EXAMPLE:
    class Post(models.Model):
        title = models.CharField(max_length=200)
        def __str__(self):
            return self.title      # <-- this is exactly what the repo's
                                    #     Django models lesson teaches too!

COMMON MISTAKES:
    - Skipping __str__ on Django models (admin panel becomes unreadable).
QUICK EXERCISE:
    Add __str__ and __eq__ to the Book class from earlier.
"""


# ------------------------------------------------------------------------------
# TOPIC: Composition, Classmethods/Staticmethods, Dataclasses  (repo sec 6-8)
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION (keep this light for beginners — repo goes very deep):
    - Composition: build a class using OTHER objects inside it ("HAS-A"),
      instead of inheriting from them.
    - @classmethod: an alternate constructor (e.g. Post.from_json(data)).
    - @staticmethod: a plain utility function that lives inside a class for
      organization, but doesn't touch the object at all.
    - @dataclass: auto-generates __init__, __repr__, __eq__ for simple
      "data holder" classes — saves boilerplate.

WHY IT MATTERS:
    classmethod factories are commonly used in Django-adjacent code for
    "create from external data" patterns.

CODE EXAMPLE:
"""

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["price"])

    @staticmethod
    def apply_discount(price, percent):
        return price - (price * percent / 100)

"""
QUICK EXERCISE:
    Add a classmethod `Product.free_sample(name)` that returns a Product
    with price=0.
"""

# NOTE: The repo also covers __slots__, Abstract Base Classes, Protocols,
# and Descriptors (advanced Python typing/interface topics). These are
# GOOD TO KNOW but usually too advanced for a first pass with beginners —
# introduce them only once students are comfortable with everything above.


# ##############################################################################
# #M1A  MODULE 1 — FOUNDATIONS: WEB & DJANGO CORE   [01_fundamentals/]
# ##############################################################################

# ------------------------------------------------------------------------------
# TOPIC: Web Fundamentals & Django Core (Client-Server, HTTP, REST, MVT)
# file: 01_intro_django.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    - Client-Server model: a CLIENT (browser/app) asks for something, a
      SERVER answers. The internet runs on this back-and-forth.
    - HTTP: the "language" clients and servers speak. A request has a
      METHOD (GET, POST, PUT, PATCH, DELETE), a URL, headers, and maybe a
      body. A response has a STATUS CODE (200 OK, 404 Not Found...).
    - REST: a set of rules for organizing that communication around
      "resources" (e.g. /api/posts/123).
    - Django's MVT pattern: Model (data) -> View (logic) -> Template (HTML).

WHY IT MATTERS:
    This is the mental model for EVERYTHING that follows in the course.
    Every Django feature is really just "handle an HTTP request, talk to
    the Model, return a response."

HOW TO TEACH IT:
    1. Draw the request/response cycle on the whiteboard first — no code.
    2. Show a real request in the browser's Network tab (F12) so it's not
       abstract.
    3. List the 5 REST verbs and map each to a plain-English action:
       GET=read, POST=create, PUT=replace, PATCH=update-part, DELETE=remove.
    4. Walk through the MVT request flow diagram (urls.py -> view -> model
       -> template -> response).

CODE EXAMPLE (project setup commands, exact as in repo):
    pip install Django
    django-admin startproject auth_project
    cd auth_project
    python manage.py startapp blog
    # then add 'blog' to INSTALLED_APPS in settings.py

COMMON MISTAKES:
    - Forgetting to add the new app to INSTALLED_APPS.
    - Confusing PUT (replace whole resource) with PATCH (partial update).
    - Thinking HTTP "remembers" previous requests — it's stateless!

QUESTIONS STUDENTS MAY ASK:
    Q: "Why does the server 'forget' me between requests (stateless)?"
    A: HTTP itself has no memory. Django re-identifies you each time using
       a session cookie stored in your browser.

QUICK EXERCISE:
    Ask students to open browser DevTools -> Network tab, visit any
    website, and identify one GET request's status code and headers.
"""


# ------------------------------------------------------------------------------
# TOPIC: Setting Up Your Development Environment
# file: 02_setup_environment.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    A virtual environment ("venv") is an isolated Python workspace per
    project, so one project's packages don't clash with another's.

WHY IT MATTERS:
    Without venvs, installing Django for Project A can silently break
    Project B if they need different versions.

TERMINAL COMMANDS (Linux, exact as repo + adjusted for your OS):
    python3 --version                 # check Python installed
    python3 -m venv venv              # create virtual environment
    source venv/bin/activate          # activate it (Linux/Mac)
    pip install Django~=4.0           # install Django inside the venv

COMMON MISTAKES:
    - Installing packages globally (forgetting to activate venv first) —
      terminal prompt should show "(venv)" when active.
    - Committing the venv folder to Git (it should be in .gitignore).

QUICK EXERCISE:
    Have each student create a venv, activate it, and run
    `pip install Django` then `python -m django --version` to confirm.
"""


# ------------------------------------------------------------------------------
# TOPIC: Project Structure & Apps
# file: 03_project_structure_apps.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    A Django PROJECT is the whole website. An APP is one reusable feature
    inside it (e.g. "blog", "accounts", "payments"). One project can have
    many apps.

WHY IT MATTERS:
    Keeps large codebases organized. Beginners often try to cram
    everything into one app — teach them to think in small, focused apps.

TERMINAL COMMANDS:
    django-admin startproject myproject
    cd myproject
    python manage.py startapp blog

HOW TO TEACH IT:
    Open the generated folder tree in VS Code and explain each file live:
    manage.py, settings.py, urls.py, wsgi.py/asgi.py, and the app's own
    models.py / views.py / admin.py / urls.py / migrations/.

COMMON MISTAKES:
    - Forgetting to register the app in INSTALLED_APPS (settings.py).
    - Putting all logic in one giant app instead of splitting by feature.
"""


# ------------------------------------------------------------------------------
# TOPIC: Models & Databases (ORM, Migrations, CRUD)
# file: 04_models_databases.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    A Model is a Python class that represents a database table. Each class
    attribute is a column. Django's ORM (Object-Relational Mapper) lets you
    talk to the database using Python instead of raw SQL.

WHY IT MATTERS:
    This is the "M" in MVT and the foundation of every Django app that
    stores data.

CODE EXAMPLE:
    from django.db import models
    from django.contrib.auth.models import User

    class Post(models.Model):
        title = models.CharField(max_length=200)
        content = models.TextField()
        author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

        def __str__(self):
            return self.title

TERMINAL COMMANDS (the migration system):
    python manage.py makemigrations   # generate migration files from models
    python manage.py migrate          # apply them to the actual database

CRUD IN THE ORM (teach these 5 lines as a mini cheat-sheet):
    Post.objects.create(title="Hello", content="World")     # Create
    Post.objects.all()                                       # Read all
    Post.objects.filter(title__contains="Hello")             # Read filtered
    post.title = "New Title"; post.save()                    # Update
    post.delete()                                             # Delete

COMMON MISTAKES:
    - Editing models.py and forgetting to run makemigrations + migrate.
    - Forgetting `on_delete=models.CASCADE` on ForeignKey (it's required).
    - Confusing CharField (needs max_length) with TextField (no limit).

QUICK EXERCISE:
    Create a `Comment` model with `post` (ForeignKey to Post), `body`
    (TextField), and `created_at` (DateTimeField, auto_now_add=True).
"""


# ------------------------------------------------------------------------------
# TOPIC: Django Admin
# file: 05_django_admin.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    Django Admin is a free, automatic content-management dashboard built
    from your models. No frontend code needed.

WHY IT MATTERS:
    Great for teaching CRUD visually before students write their own views
    -- and useful in real projects for staff to manage data.

TERMINAL COMMANDS:
    python manage.py createsuperuser
    python manage.py runserver
    # then visit http://127.0.0.1:8000/admin/

CODE EXAMPLE:
    # blog/admin.py
    from django.contrib import admin
    from .models import Post

    @admin.register(Post)
    class PostAdmin(admin.ModelAdmin):
        list_display = ('title', 'created_at')
        list_filter = ('created_at',)
        search_fields = ('title', 'content')

COMMON MISTAKES:
    - Forgetting to register a model in admin.py -> it never appears.
    - Confusing `admin.site.register(Post)` (simple) with a custom
      ModelAdmin class (more control) -- both work, just different needs.

QUICK EXERCISE:
    Register the Comment model in admin.py and add list_display for
    ('post', 'created_at').
"""


# ------------------------------------------------------------------------------
# TOPIC: Views, URLs & Templates (MVT in action)
# file: 06_views_urls_templates.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    View = Python function/class that decides WHAT data to show.
    Template = HTML file that decides HOW to display it.
    URLs = the map that connects a web address to the right view.

WHY IT MATTERS:
    This is the first time students build something they can literally
    see in the browser — always a big confidence boost.

CODE EXAMPLE (function-based view -> template -> urls, exact repo flow):

    # blog/views.py
    from django.shortcuts import render
    from .models import Post

    def post_list_view(request):
        posts = Post.objects.all()
        return render(request, 'blog/post_list.html', {'posts_list': posts})

    <!-- blog/templates/blog/post_list.html -->
    <h1>Latest Posts</h1>
    <ul>
        {% for post in posts_list %}
            <li>{{ post.title }} - {{ post.created_at }}</li>
        {% empty %}
            <li>No posts yet.</li>
        {% endfor %}
    </ul>

    # blog/urls.py
    from django.urls import path
    from .views import post_list_view
    urlpatterns = [ path('', post_list_view, name='post_list') ]

    # project urls.py
    from django.urls import path, include
    urlpatterns = [ path('blog/', include('blog.urls')) ]

HOW TO TEACH IT (step order matters -- teach in this exact order):
    1. Write the view first (fetch data).
    2. Write the template (display data) — mention {{ }} vs {% %}.
    3. Wire up app-level urls.py, then include it in the project urls.py.
    4. Run the server and visit the page together.

COMMON MISTAKES:
    - Template not found errors -> usually a wrong folder path
      (should be app/templates/app/template.html).
    - Forgetting `include()` when linking app urls into the project urls.
    - Mixing up {{ variable }} (output) with {% tag %} (logic).

QUICK EXERCISE:
    Build a `post_detail_view(request, pk)` that shows ONE post using
    `get_object_or_404(Post, pk=pk)`.
"""


# ##############################################################################
# #M1B  MODULE 1 — DEEP DIVE: FORMS, AUTH, MIDDLEWARE   [02_deep_dive/]
# ##############################################################################

# ------------------------------------------------------------------------------
# TOPIC: Forms & Validation
# file: 01_forms_validation.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    Django Forms handle generating HTML input fields, validating user
    input, and protecting against attacks (CSRF) -- all in one system.
    A ModelForm is a form auto-built from a Model.

WHY IT MATTERS:
    Any app that accepts user input (signup, comments, contact forms)
    needs this. It's also the direct ancestor of DRF Serializers later.

CODE EXAMPLE:
    # blog/forms.py
    from django import forms
    from .models import Post

    class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = ['title', 'content']

        def clean_title(self):
            title = self.cleaned_data.get('title')
            if "Bad Word" in title:
                raise forms.ValidationError("Please choose a better title!")
            return title

    # blog/views.py
    def create_post_view(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('post_list')
        else:
            form = PostForm()
        return render(request, 'blog/create_post.html', {'form': form})

    <!-- template -->
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Create Post</button>
    </form>

COMMON MISTAKES:
    - Forgetting {% csrf_token %} -> Django will reject the POST (403).
    - Forgetting to check `request.method == 'POST'` -> form re-submits
      accidentally on every page load.
    - Naming a custom validator wrong -- must be `clean_<fieldname>`.

QUICK EXERCISE:
    Add a `clean_content()` method that rejects posts under 10 characters.
"""


# ------------------------------------------------------------------------------
# TOPIC: Class-Based Views (CBVs)
# file: 02_class_based_views.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    Instead of writing a function for every CRUD action, Django gives you
    ready-made CLASSES (ListView, DetailView, CreateView, UpdateView,
    DeleteView) that already know how to do the common work.

WHY IT MATTERS:
    CBVs are the "professional" standard for larger Django projects --
    less repeated code (DRY), easy to extend by overriding methods.

CODE EXAMPLE:
    from django.views.generic import ListView, DetailView, CreateView
    from .models import Post

    class PostListView(ListView):
        model = Post
        template_name = 'blog/post_list.html'
        context_object_name = 'posts'

        def get_queryset(self):
            return Post.objects.filter(is_published=True).order_by('-created_at')

    # urls.py -- NOTE: must call .as_view()
    path('', PostListView.as_view(), name='post_list')

COMMON MISTAKES:
    - Forgetting `.as_view()` in urls.py (a very common first-time error).
    - Not knowing which attribute to override (model vs queryset vs
      get_queryset) -- teach: use `model` for the simple case, override
      `get_queryset()` only when you need custom filtering.

QUICK EXERCISE:
    Convert the `post_detail_view` function from earlier into a
    `PostDetailView(DetailView)` class.
"""


# ------------------------------------------------------------------------------
# TOPIC: Authentication vs Authorization
# files: 03_auth_authorization.md, 04_auth_in_depth.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    Authentication = "Who are you?" (logging in).
    Authorization  = "What are you allowed to do?" (permissions).
    Authentication must happen BEFORE authorization can make sense.

WHY IT MATTERS:
    Almost every real app needs to answer both questions -- e.g. "is this
    user logged in?" and "can THIS user edit THIS post?"

THE 3 PILLARS OF DJANGO AUTHORIZATION (teach as a simple list):
    1. User flags: is_staff (admin site access), is_superuser (all perms).
    2. Permissions: fine-grained rules like 'blog.add_post',
       auto-created for every model (add/change/delete/view).
    3. Groups: bundle permissions together, then assign users to a group
       instead of managing permissions one by one.

CODE EXAMPLE (authentication flow):
    from django.contrib.auth import authenticate, login, logout

    def login_view(request):
        user = authenticate(request, username=..., password=...)
        if user is not None:
            login(request, user)   # creates the session

CODE EXAMPLE (protecting views):
    from django.contrib.auth.decorators import login_required, permission_required

    @login_required
    @permission_required('blog.add_post', raise_exception=True)
    def create_post_view(request):
        ...

    # class-based equivalent:
    from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
    class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
        permission_required = 'blog.add_post'

CODE EXAMPLE (object-level check -- "is THIS post yours?"):
    def edit_own_post(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return HttpResponseForbidden("Not your post.")
        ...

COMMON MISTAKES:
    - Confusing is_staff (admin access) with is_superuser (all permissions).
    - Thinking `has_perm()` checks object ownership -- it doesn't! Broad
      permissions and object-level checks are DIFFERENT tools (teach both).
    - Putting @permission_required BEFORE @login_required (order matters;
      login_required should generally come first).

QUESTIONS STUDENTS MAY ASK:
    Q: "What's the difference between a permission and a group?"
    A: A permission is one specific rule. A group is a labelled bundle of
       permissions you can hand to many users at once.

QUICK EXERCISE:
    Write a view `delete_own_comment(request, pk)` that only lets a user
    delete a Comment if `comment.author == request.user`.
"""


# ------------------------------------------------------------------------------
# TOPIC: Middleware (Intro + Practical)
# files: 05_middleware_intro.md, 06_middleware_practical.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    Middleware is code that runs on EVERY request/response, before it
    reaches your view and after it leaves. Think of it as security
    checkpoints a request must pass through, in order.

WHY IT MATTERS:
    Perfect for site-wide rules (e.g. "must be logged in for the whole
    site") that would be repetitive to add to every single view.

WHEN TO USE MIDDLEWARE VS NOT (important teaching table):
    USE for:      global rules, URL-prefix rules (e.g. all /staff/ URLs)
    DON'T use for: object-level checks (e.g. "is this post yours"),
                   heavy database queries, view-specific logic

CODE EXAMPLE (skeleton every middleware follows):
    class MyAuthMiddleware:
        def __init__(self, get_response):
            self.get_response = get_response   # one-time setup

        def __call__(self, request):
            # ... code BEFORE the view runs ...
            response = self.get_response(request)
            # ... code AFTER the view runs ...
            return response

    # settings.py -- ORDER MATTERS!
    MIDDLEWARE = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',  # must be
                                                                     # before yours
        'yourapp.middleware.MyAuthMiddleware',
    ]

CODE EXAMPLE (role-based URL restriction):
    class StaffOnlyMiddleware:
        def __init__(self, get_response):
            self.get_response = get_response

        def __call__(self, request):
            if request.path.startswith('/staff/') and not request.user.is_staff:
                return HttpResponseForbidden("Staff only.")
            return self.get_response(request)

COMMON MISTAKES:
    - Placing custom middleware BEFORE AuthenticationMiddleware ->
      request.user won't exist yet -> crashes.
    - Forgetting to exclude login/signup pages from a "must be logged in"
      middleware -> infinite redirect loop!
    - Doing heavy DB queries in middleware -> slows down EVERY request.

QUICK EXERCISE:
    Write (on paper/whiteboard, not full code) the pseudocode for a
    middleware that blocks any request to '/api/' if there's no
    Authorization header.
"""


# ------------------------------------------------------------------------------
# TOPIC: Custom User Models
# file: 07_custom_user_models.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    Django's built-in User model is basic. A Custom User Model lets you
    add your own fields (bio, profile picture, etc.) or change login
    behaviour (e.g. login with email instead of username).

WHY IT MATTERS:
    THE GOLDEN RULE (repo emphasizes this strongly): set this up BEFORE
    your first migration. Changing it after you have real data is very
    difficult -- so every serious Django project starts this way.

CODE EXAMPLE:
    # users/models.py
    from django.contrib.auth.models import AbstractUser
    from django.db import models

    class CustomUser(AbstractUser):
        bio = models.TextField(blank=True)
        is_premium = models.BooleanField(default=False)

    # settings.py
    AUTH_USER_MODEL = 'users.CustomUser'

    # ANYWHERE else you reference the user model, do NOT import CustomUser
    # directly -- use this instead:
    from django.conf import settings
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

COMMON MISTAKES:
    - Adding a custom user model AFTER already running migrations (very
      hard to fix -- almost always means starting the DB over).
    - Hardcoding `from django.contrib.auth.models import User` in other
      apps instead of settings.AUTH_USER_MODEL / get_user_model().

QUICK EXERCISE:
    Add a `phone_number` field to CustomUser and explain out loud (to a
    partner) which file needs to change and in what order.
"""


# ------------------------------------------------------------------------------
# TOPIC: Static & Media Files
# file: 08_static_media_files.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    STATIC files = CSS/JS/images YOU (the developer) ship with the app.
    MEDIA files = files YOUR USERS upload (e.g. profile pictures).

WHY IT MATTERS:
    Every real app needs at least one of these; media files especially
    need special handling because they're not part of your source code.

CODE EXAMPLE:
    # settings.py
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [BASE_DIR / 'static']
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

    <!-- template -->
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">

    # project urls.py (dev only!)
    from django.conf import settings
    from django.conf.urls.static import static
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # model field for uploads
    thumbnail = models.ImageField(upload_to='post_thumbnails/', blank=True, null=True)

COMMON MISTAKES:
    - Forgetting `{% load static %}` at the top of the template.
    - Expecting the dev media-serving trick to work in production (it
      doesn't -- production needs a real web server or cloud storage).

QUICK EXERCISE:
    Add an ImageField called `avatar` to CustomUser and display it in a
    template using {{ user.avatar.url }}.
"""


# ##############################################################################
# #M1C  MODULE 1 — DRF & APIs   [03_drf_apis/]
# ##############################################################################

# ------------------------------------------------------------------------------
# TOPIC: Intro to DRF & Serializers
# file: 01_intro_drf_serializers.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    An API lets different software talk to each other (e.g. your Django
    backend <-> a React frontend or mobile app). DRF (Django REST
    Framework) is the standard toolkit for building APIs in Django.
    A Serializer converts a Model object into JSON (and back again).

WHY IT MATTERS:
    Modern apps are rarely "just HTML pages" anymore -- most products need
    an API for a mobile app or JS frontend. DRF is industry-standard.

TERMINAL COMMANDS:
    pip install djangorestframework
    # then add 'rest_framework' to INSTALLED_APPS

CODE EXAMPLE:
    # blog/serializers.py
    from rest_framework import serializers
    from .models import Post

    class PostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ['id', 'title', 'content', 'created_at']

    # blog/views.py
    from rest_framework import generics
    class PostListAPIView(generics.ListCreateAPIView):
        queryset = Post.objects.all()
        serializer_class = PostSerializer

COMMON MISTAKES:
    - Forgetting to add 'rest_framework' to INSTALLED_APPS.
    - Listing a field in `fields` that doesn't exist on the model.

QUICK EXERCISE:
    Write a CommentSerializer with fields ['id', 'post', 'body', 'created_at'].
"""


# ------------------------------------------------------------------------------
# TOPIC: ViewSets & Routers
# file: 02_viewsets_routers.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    A ViewSet bundles List/Create/Retrieve/Update/Delete into ONE class.
    A Router then AUTO-GENERATES all the URL patterns for that ViewSet, so
    you don't hand-write 5 separate url paths.

WHY IT MATTERS:
    This is the fastest, most standard way to build a full CRUD API in
    Django -- a handful of lines instead of dozens.

CODE EXAMPLE:
    # blog/views.py
    from rest_framework import viewsets
    class PostViewSet(viewsets.ModelViewSet):
        queryset = Post.objects.all()
        serializer_class = PostSerializer

    # blog/urls.py
    from rest_framework.routers import DefaultRouter
    router = DefaultRouter()
    router.register('posts', PostViewSet, basename='post')
    urlpatterns = router.urls

COMMON MISTAKES:
    - Using APIView/generics AND ViewSets inconsistently across a project
      -- pick ViewSets+Routers for standard CRUD, and APIView only for
      truly custom endpoints.

QUICK EXERCISE:
    Register a CommentViewSet with the router at 'comments'.
"""


# ------------------------------------------------------------------------------
# TOPIC: JWT & Token Authentication
# file: 03_jwt_token_auth.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    Browsers use SESSION login. APIs (used by mobile apps / JS frontends)
    usually use TOKEN or JWT login instead. JWT = JSON Web Token: a
    self-contained "ID card" the client sends with every request, made of
    a short-lived ACCESS token and a longer-lived REFRESH token.

WHY IT MATTERS:
    Any API meant for a mobile app or single-page app needs this instead
    of session cookies.

TERMINAL COMMANDS:
    pip install djangorestframework-simplejwt

CODE EXAMPLE:
    # settings.py
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        )
    }

    # project urls.py
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
    urlpatterns += [
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]

    # protecting a viewset
    from rest_framework.permissions import IsAuthenticated
    class PostViewSet(viewsets.ModelViewSet):
        permission_classes = [IsAuthenticated]

COMMON MISTAKES:
    - Confusing the ACCESS token (short-lived, sent with every request)
      with the REFRESH token (long-lived, only used to get a new access
      token).
    - Forgetting to set `permission_classes` -> endpoint stays public.

QUICK EXERCISE:
    Using Postman or curl, POST username/password to /api/token/ and show
    students the returned access + refresh tokens.
"""


# ------------------------------------------------------------------------------
# TOPIC: Filtering, Searching & Pagination
# file: 04_filtering_searching_pagination.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    Pagination = split big result lists into pages.
    Filtering = let clients narrow results (?author_id=3).
    Searching/Ordering = let clients search text fields or sort results.

WHY IT MATTERS:
    Once an API has thousands of rows, returning everything at once is
    slow and wasteful -- these tools are essential for real-world APIs.

CODE EXAMPLE:
    # settings.py (global pagination)
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10,
    }

    # search + ordering on a viewset
    from rest_framework import filters
    class PostViewSet(viewsets.ModelViewSet):
        filter_backends = [filters.SearchFilter, filters.OrderingFilter]
        search_fields = ['title', 'content']
        ordering_fields = ['created_at', 'title']

    # advanced filtering (needs: pip install django-filter)
    filterset_fields = ['author', 'category']

COMMON MISTAKES:
    - Forgetting PAGE_SIZE -> API returns everything at once anyway.
    - Confusing search_fields (text search) with filterset_fields (exact
      match filters).

QUICK EXERCISE:
    Add search_fields to the CommentViewSet so ?search=hello works.
"""


# ##############################################################################
# #M1D  MODULE 1 — TESTING & PERFORMANCE   [04_testing_performance/]
# ##############################################################################

# ------------------------------------------------------------------------------
# TOPIC: Automated Testing
# file: 01_automated_testing.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    Automated tests are small pieces of code that check your OWN code
    works correctly, automatically, every time you run them.

WHY IT MATTERS:
    Lets you change code confidently without breaking things -- and is
    considered a mark of professional-quality software.

TERMINAL COMMANDS:
    python manage.py test

CODE EXAMPLE (unit test):
    from django.test import TestCase
    from .models import Post

    class PostModelTest(TestCase):
        def test_string_representation(self):
            post = Post.objects.create(title="My Post", content="Hello!")
            self.assertEqual(str(post), "My Post")

CODE EXAMPLE (integration test -- testing a view):
    from django.urls import reverse
    class PostViewTest(TestCase):
        def test_post_list_view(self):
            response = self.client.get(reverse('post_list'))
            self.assertEqual(response.status_code, 200)

COMMON MISTAKES:
    - Only testing the "happy path" and never testing failure cases.
    - Not running tests before pushing code -- make it a class habit.

QUICK EXERCISE:
    Write a test that creates a Comment and asserts str(comment) is not
    empty.
"""


# ------------------------------------------------------------------------------
# TOPIC: Queryset Optimization (select_related / prefetch_related)
# file: 02_queryset_optimization.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    The "N+1 problem": if you loop over 100 posts and access post.author
    for each, Django by default runs 1 query for the posts + 100 MORE
    queries for the authors = 101 queries! select_related/prefetch_related
    fix this by fetching related data upfront.

WHY IT MATTERS:
    This is one of the most common real-world Django performance bugs.
    Knowing this instantly makes a junior look senior.

CODE EXAMPLE:
    # BAD -- N+1 problem
    posts = Post.objects.all()
    # then in template: post.author.username  -> extra query PER post

    # GOOD -- one JOIN query (ForeignKey / OneToOne)
    posts = Post.objects.select_related('author').all()

    # GOOD -- for Many-to-Many / reverse FK
    posts = Post.objects.prefetch_related('tags').all()

RULE OF THUMB TO TEACH:
    select_related  -> "One-to-One" and ForeignKey (JOIN, single query)
    prefetch_related -> Many-to-Many & reverse FK (separate query, joined
                         in Python)

COMMON MISTAKES:
    - Using select_related on a Many-to-Many field (wrong tool -- use
      prefetch_related instead).
    - Never noticing the N+1 problem because it's invisible until the
      dataset grows.

QUICK EXERCISE:
    Rewrite `Post.objects.all()` to also fetch author and tags in the
    fewest possible queries.
"""


# ------------------------------------------------------------------------------
# TOPIC: Caching Strategies
# file: 03_caching_strategies.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    Caching = storing an already-computed answer somewhere fast (RAM) so
    you don't have to redo the expensive work (like a DB query) next time.

WHY IT MATTERS:
    Crucial once an app has real traffic -- caching is one of the cheapest
    ways to make an app feel dramatically faster.

CODE EXAMPLE (cache a whole view):
    from django.views.decorators.cache import cache_page

    @cache_page(60 * 15)   # cache for 15 minutes
    def post_list_view(request):
        ...

CODE EXAMPLE (low-level cache API):
    from django.core.cache import cache

    def get_expensive_data():
        data = cache.get('my_expensive_key')
        if not data:
            data = perform_expensive_calculation()
            cache.set('my_expensive_key', data, 3600)  # 1 hour
        return data

COMMON MISTAKES:
    - Caching data that changes often (users see stale info).
    - Forgetting to invalidate/clear cache after data updates.

QUICK EXERCISE:
    Explain in your own words: why is Redis usually preferred over the
    local memory cache in production?
"""


# ------------------------------------------------------------------------------
# TOPIC: Security Hardening
# file: 04_security_hardening.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    A checklist of settings and practices that make a Django app safe to
    put on the real internet.

WHY IT MATTERS:
    A student's first deployed app is often insecure by default if they
    never learn this checklist -- it should be taught before any real
    deployment.

TERMINAL COMMANDS:
    python manage.py check --deploy

KEY SETTINGS TO TEACH (as a checklist):
    DEBUG = False                     # NEVER True in production
    ALLOWED_HOSTS = ['yourdomain.com']
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

BUILT-IN PROTECTIONS TO EXPLAIN:
    - SQL Injection: Django ORM auto-protects you (avoid raw SQL).
    - XSS: templates auto-escape HTML (avoid the `|safe` filter unless sure).
    - CSRF: {% csrf_token %} required on every POST form.

COMMON MISTAKES:
    - Committing SECRET_KEY to Git -- use environment variables instead
      (e.g. python-dotenv or django-environ).
    - Leaving DEBUG = True in production (leaks internal details to
      attackers).

QUICK EXERCISE:
    Run `python manage.py check --deploy` on a project and read through
    every warning it produces together as a class.
"""


# ##############################################################################
# #M2   MODULE 2 — SYSTEM DESIGN & ARCHITECTURE   [05_expert_topics/]
# ##############################################################################
"""
NOTE: This module is conceptual/non-coding. Teach with diagrams and
discussion rather than live code.
"""

# ------------------------------------------------------------------------------
# TOPIC: Introduction to System Design
# file: 00_system_design_intro.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    System design is planning HOW to build a large application BEFORE
    writing code -- like an architect's blueprint before construction.

WHY IT MATTERS:
    Backend developers who understand system design write code that
    scales, stays reliable, and doesn't need painful rewrites later.

KEY IDEAS TO TEACH:
    - Functional requirements ("what it does") vs Non-Functional
      requirements ("how well it does it": scalability, availability,
      latency, security, cost).
    - The process: Requirements -> High-Level Design -> Low-Level Design
      -> Scalability planning -> Security review -> Iterate.
    - EVERY design involves TRADE-OFFS (e.g. Performance vs Cost,
      Consistency vs Availability). There is no "perfect" system.

QUICK EXERCISE:
    Ask students: "What are 3 non-functional requirements for a
    ride-hailing app like Bolt/Uber?" (expect: low latency, high
    availability, strong data security).
"""


# ------------------------------------------------------------------------------
# TOPIC: Monolithic Architecture
# file: 03_monolithic_architecture.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    A monolith is ONE single application containing everything (UI,
    business logic, database access) running as one unit/process.

WHY IT MATTERS:
    Nearly every Django app students build in this course IS a monolith
    -- and that's usually the RIGHT starting choice, not a bad one.

TEACHING POINTS:
    - Pros: simple to build, deploy, and debug; great for small teams and
      early-stage products (this course's own practicals are monoliths).
    - Cons: harder to scale ONE piece independently; large teams can step
      on each other's toes; one bug can affect the whole app.

QUICK EXERCISE:
    Ask: "Is the Django blog app we built in Module 1 a monolith? Why?"
"""


# ------------------------------------------------------------------------------
# TOPIC: Microservices Architecture
# file: 04_microservices_architecture.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    Instead of one big app, microservices split the system into many
    small, independent services (e.g. a "payments service", a "users
    service") that talk to each other over the network.

WHY IT MATTERS:
    Common in large companies -- students should recognize the term and
    know when it's overkill for a small project (most beginner projects
    should NOT start as microservices).

TEACHING POINTS:
    - Pros: independent scaling, teams can use different tech per service,
      faster releases for large orgs.
    - Cons: much more operational complexity, harder debugging across
      services, higher infrastructure cost.

QUICK EXERCISE:
    Ask: "Would a student portfolio project need microservices? Why or
    why not?" (Expected answer: no -- monolith is simpler and sufficient.)
"""


# ------------------------------------------------------------------------------
# TOPIC: Other Architectural Styles (SOA, Serverless, Event-Driven)
# file: 05_other_architectural_styles.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION (brief overview only, per repo):
    - SOA (Service-Oriented Architecture): services share business
      functionality, similar to microservices but more coarse-grained.
    - Serverless: you write functions; a cloud provider runs them without
      you managing servers.
    - Event-Driven Architecture: services react to "events" (things that
      happened) rather than direct calls -- good for high-volume,
      asynchronous workflows.

WHY IT MATTERS:
    Students should recognize these terms in job descriptions / interviews
    even if they don't build with them yet.

TEACHING POINTS (event-driven, from repo):
    Pros: handles high-volume data well, decouples services.
    Cons: harder to debug, "eventual consistency" (data isn't updated
    everywhere instantly), tricky error handling.

QUICK EXERCISE:
    Match each style to a real example: "Uber's trip-matching" (event-
    driven), "AWS Lambda contact-form handler" (serverless).
"""


# ------------------------------------------------------------------------------
# TOPIC: Making Architectural Decisions
# file: 06_architectural_decisions.md
# ------------------------------------------------------------------------------
"""
SIMPLE EXPLANATION:
    There is no single "best" architecture -- only the best FIT for your
    project's specific goals, team size, budget, and timeline.

WHY IT MATTERS:
    Teaches students to justify decisions instead of copying trends --
    a key interview and real-job skill.

KEY IDEAS TO TEACH:
    - Context matters: business goals, team size/skill, budget, deadline.
    - ADR (Architectural Decision Record): a short written doc capturing
      Title / Status / Context / Decision / Consequences -- good habit to
      introduce even for student projects.
    - "Monolith First" principle (Martin Fowler): start simple, evolve to
      microservices ONLY when real pain points appear.
    - Strangler Fig Pattern: gradually replace parts of an old monolith
      with new services instead of a risky full rewrite.

QUICK EXERCISE:
    Have students write a 4-line ADR for "should our class project use
    SQLite or PostgreSQL?" (Title/Status/Context/Decision/Consequence).
"""


# ==============================================================================
# END OF GUIDE
# ==============================================================================
"""
REMINDER: Sections not yet built out in the source repo (mentioned only in
its outline, no lesson files found):
    - Web Hosting / Server Configuration (Nginx, Apache2)
    - Distributed Systems
    - Continuous Integration (CI) Pipelines
Check the repo again later in case these get added, and re-scan before
teaching them.
"""



