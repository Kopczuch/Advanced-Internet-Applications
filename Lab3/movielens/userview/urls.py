from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("genre/<int:pk>", views.GenreView.as_view(), name="index"),
    path("movie/<int:pk>", views.MovieView.as_view(), name="movie"),
    path("register", views.register_request, name="register"),
    path("log_in", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("my_ratings", views.my_ratings, name="my_ratings"),
    path("new_rating", views.new_rating, name="new_rating"),
    # path("rating", views.RatingView.as_view(), name="rating"),
    path("comment/<int:pk>", views.CommentView.as_view(), name="comment"),
    path("movie/<int:movie_id>/gallery", views.movie_gallery, name="movie_gallery"),
    path("movie/<movie_id>/rate", views.new_rating, name="rate_movie"),
    path("movie/<movie_id>/add_comment", views.add_comment, name="add_comment"),
    path("search", views.search, name="search"),
    path("new_movie", views.new_movie, name="new_movie"),
    path('movie/<int:movie_id>/add_image', views.add_image, name='add_image'),
    path('movie/<int:movie_id>/edit_movie', views.edit_movie, name='edit_movie'),
    # path('iframe', views.iframe, name='iframe'),
    # path('video', views.video, name='video'),
    # path('video_embed', views.video_embed, name='video_embed'),
]