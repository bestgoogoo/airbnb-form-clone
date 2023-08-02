from django.urls import path
from .views import Contents, ContentDetail


urlpatterns = [
    path("contents/", Contents.as_view()),
    path("contents/<int:pk>", ContentDetail.as_view()),
]
