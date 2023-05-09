from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("genre/<int:pk>", views.GenreView.as_view(), name="index"),
    path("movie/<int:pk>", views.MovieView.as_view(), name="index"),
]