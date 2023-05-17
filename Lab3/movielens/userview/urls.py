from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("genre/<int:pk>", views.GenreView.as_view(), name="index"),
    path("movie/<int:pk>", views.MovieView.as_view(), name="index"),
    path("register", views.register_request, name="register"),
    path("log_in", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("my_ratings", views.my_ratings, name="my_ratings"),
    path("new_rating", views.new_rating, name="new_rating"),
    # path("rating", views.RatingView.as_view(), name="rating")
]