"""
DJANGO REST FRAMEWORK — JWT & TOKEN AUTHENTICATION
=================================================

BASIC TEACHING GUIDE

1. WHAT IS AUTHENTICATION?
--------------------------
Authentication answers:

    "Who are you?"

A user normally provides a username/email and password.
If the details are correct, the user is authenticated.


2. SESSION VS TOKEN AUTHENTICATION
----------------------------------
Traditional Django websites often use sessions and cookies.

APIs are commonly used by:

    - Mobile applications
    - React applications
    - Other frontend applications
    - Other services

For APIs, token authentication is commonly used.

Simple flow:

    Login
      |
      v
    Server checks username/password
      |
      v
    Server gives the client a token
      |
      v
    Client sends the token with future requests


3. WHAT IS JWT?
---------------
JWT means:

    JSON Web Token

Think of a JWT as a digital ID card.

After login:

    Server -> JWT -> Client

For a protected API request:

    Client -> JWT -> Server

The server checks the token before allowing access.


4. ACCESS TOKEN AND REFRESH TOKEN
---------------------------------
SimpleJWT normally provides two tokens:

    ACCESS TOKEN
        Short-lived token used to access protected APIs.

    REFRESH TOKEN
        Used to obtain a new access token after the access
        token expires.

Simple flow:

    Login
      |
      +----> Access token
      |
      +----> Refresh token


5. INSTALL SIMPLE JWT
---------------------
Run in the terminal:

    pip install djangorestframework-simplejwt

Then update requirements.txt:

    pip freeze > requirements.txt


6. CONFIGURE JWT
----------------
Open settings.py.

Make sure DRF is installed:

    INSTALLED_APPS = [
        ...
        "rest_framework",
    ]

Then add:

    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ),
    }

This tells DRF to use JWT authentication.


7. CREATE TOKEN URLS
--------------------
In urls.py:

    from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )

Add:

    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    )

The two endpoints are:

    POST /api/token/
        Login and get tokens.

    POST /api/token/refresh/
        Get a new access token.


8. GETTING A TOKEN
------------------
Send a POST request to:

    /api/token/

Example JSON:

    {
        "username": "john",
        "password": "mypassword"
    }

A successful response contains:

    {
        "refresh": "......",
        "access": "......"
    }


9. USING THE ACCESS TOKEN
-------------------------
A protected API request normally sends:

    Authorization: Bearer <access_token>

Example:

    Authorization: Bearer eyJhbGciOi...


10. PROTECTING AN API VIEW
--------------------------
Example:

    from rest_framework.permissions import IsAuthenticated
    from rest_framework.views import APIView
    from rest_framework.response import Response


    class ProfileAPIView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request):
            return Response({
                "message": "You are authenticated.",
                "username": request.user.username,
            })

The important line is:

    permission_classes = [IsAuthenticated]

It means only authenticated users can access the endpoint.


11. COMPLETE JWT FLOW
---------------------

    USER
      |
      | username + password
      v
    LOGIN ENDPOINT
      |
      v
    SERVER
      |
      | JWT tokens
      v
    CLIENT
      |
      | access token
      v
    PROTECTED API
      |
      v
    TOKEN CHECK
      |
      +---- valid ----> Allow request
      |
      +---- invalid --> Reject request


12. IMPORTANT TERMS
-------------------

    Authentication
        Checking who the user is.

    Authorization
        Checking what an authenticated user is allowed to do.

    JWT
        JSON Web Token.

    Access Token
        Short-lived token used to access protected resources.

    Refresh Token
        Used to obtain a new access token.

    IsAuthenticated
        DRF permission requiring authentication.

    Bearer
        Authentication scheme used with the Authorization header.


13. EASY CLASSROOM EXAMPLE
--------------------------
Imagine a school.

    Login
        Student shows ID and password.

    Access token
        Student receives a temporary pass.

    Protected classroom
        Only students with a valid pass can enter.

    Refresh token
        Used to get a new temporary pass when the old one expires.

JWT follows the same basic idea.


14. COMMON BEGINNER ERRORS
--------------------------

    ERROR 1
        SimpleJWT has not been installed.

        pip install djangorestframework-simplejwt


    ERROR 2
        JWT authentication was not added to REST_FRAMEWORK.


    ERROR 3
        The access token is missing from the request.


    ERROR 4
        The request uses:

        Authorization: Bearer <access_token>

        but the token is invalid or expired.


    ERROR 5
        An endpoint uses IsAuthenticated but the request is sent
        without a valid token.


15. KEY POINT
-------------

Remember this simple sequence:

    LOGIN
      ↓
    GET TOKENS
      ↓
    SEND ACCESS TOKEN
      ↓
    SERVER VALIDATES TOKEN
      ↓
    ACCESS PROTECTED API

JWT does not replace Django users.

Django still manages users and passwords.
JWT provides a way for the client to prove that it has
authenticated successfully when making API requests.
"""

# QUICK STUDENT SUMMARY
#
# JWT
#     JSON Web Token
#
# Login
#     POST /api/token/
#
# Refresh
#     POST /api/token/refresh/
#
# Protect an endpoint
#     permission_classes = [IsAuthenticated]
#
# Send token
#     Authorization: Bearer <access_token>




