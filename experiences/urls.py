from django.urls import path
from . import views


urlpatterns = [
    path("", views.Experiences.as_view()),
    path("<int:pk>", views.ExperienceDetail.as_view()),
    path("<int:pk>/photos/", views.ExperiencePhotos.as_view()),
    path("<int:pk>/video/", views.ExperienceVideo.as_view()),
    path("contents/", views.Contents.as_view()),
    path("contents/<int:pk>", views.ContentDetail.as_view()),
]
