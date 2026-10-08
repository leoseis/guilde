"""
DJANGO REST FRAMEWORK — 20 OBJECTIVE QUESTIONS

Topics: Django, DRF, serializers, ModelSerializer, APIView,
GET, POST, request.data, validation, save(), URLs and 404.

Choose A, B, C or D for each question.
"""

# ================================================================
# QUESTIONS
# ================================================================

# 1. What is the main purpose of Django REST Framework?
# A. Create desktop applications
# B. Build APIs with Django
# C. Replace Python
# D. Create operating systems


# 2. Which package is added to INSTALLED_APPS for DRF?
# A. django_api
# B. rest_framework
# C. django_rest
# D. api_framework


# 3. Which file normally contains Django database models?
# A. views.py
# B. urls.py
# C. models.py
# D. serializers.py


# 4. Which file normally contains URL routes for an app?
# A. urls.py
# B. models.py
# C. admin.py
# D. serializers.py


# 5. What is an API mainly used for?
# A. Allowing different applications to communicate
# B. Formatting Python files
# C. Creating database tables only
# D. Installing VS Code extensions


# 6. What is the main purpose of a DRF serializer?
# A. Start the Django server
# B. Convert and validate data for API use
# C. Create URL routes
# D. Create HTML pages only


# 7. Which serializer is especially useful when working with a Django model?
# A. ModelSerializer
# B. DatabaseSerializer
# C. DjangoSerializer
# D. ModelAPI


# 8. In a ModelSerializer, what does model = Post indicate?
# A. The serializer uses the Post model
# B. It creates a new database
# C. It deletes Post
# D. It creates a URL called Post


# 9. What does the fields option in a ModelSerializer control?
# A. Which model fields are included
# B. Which URL the API uses
# C. Which server port Django uses
# D. Which Python version is installed


# 10. Which import is correct for DRF serializers?
# A. from django import serializers
# B. from rest_framework import serializers
# C. from django.rest import serializer
# D. import django_serializer


# 11. Which class is commonly used for a class-based DRF API view?
# A. APIView
# B. APIClass
# C. DjangoAPI
# D. RestView


# 12. What does Post.objects.all() do?
# A. Deletes all posts
# B. Gets all Post objects from the database
# C. Creates one Post
# D. Converts Post objects to JSON


# 13. Why is many=True used here?
# LIVE CODE:
# serializer = PostSerializer(posts, many=True)
# A. One object is being serialized
# B. Multiple objects are being serialized
# C. The database has many tables
# D. POST requests require many=True


# 14. Which method handles a GET request in APIView?
# A. fetch()
# B. read()
# C. get()
# D. retrieve()


# 15. What does Response(serializer.data) normally do?
# A. Sends serialized data back to the client
# B. Deletes the database
# C. Creates a migration
# D. Starts the development server


# 16. What does request.data contain during a POST request?
# A. Data sent by the client
# B. All Django models
# C. All URL patterns
# D. The settings file


# 17. What is the purpose of serializer.is_valid()?
# LIVE CODE:
# serializer = PostSerializer(data=request.data)
# if serializer.is_valid():
#     serializer.save()
# A. Checks whether submitted data passes validation
# B. Starts the Django server
# C. Creates a URL
# D. Deletes invalid records


# 18. What does serializer.save() do after validation?
# A. Saves the validated data
# B. Starts Postman
# C. Creates a URL
# D. Stops Django

# 19. Which HTTP status code normally means a resource was created?
# A. 200
# B. 201
# C. 404
# D. 500


# 20. What is the purpose of get_object_or_404()?
# LIVE CODE:
# post = get_object_or_404(Post, id=post_id)
# A. Creates a Post automatically
# B. Finds the object or returns 404 if it does not exist
# C. Deletes the object
# D. Converts the object into JSON



# ================================================================
# ANSWER KEY
# ================================================================
# Remove this section before giving the file to students if you
# want them to complete the questions without seeing the answers.




































ANSWER_KEY = {
    1: "B",
    2: "B",
    3: "C",
    4: "A",
    5: "A",
    6: "B",
    7: "A",
    8: "A",
    9: "A",
    10: "B",
    11: "A",
    12: "B",
    13: "B",
    14: "C",
    15: "A",
    16: "A",
    17: "A",
    18: "A",
    19: "B",
    20: "B",
}
