from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    path("jwt-login", views.JWTLogIn.as_view()),  # JWT login using username, password
    path("token-login", obtain_auth_token),  # authToken login using username, password
    path("log-in", views.LogIn.as_view()),  # cookie login using username, password
    path("github", views.GithubLogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    path("@<str:username>", views.PublicUser.as_view()),
]
