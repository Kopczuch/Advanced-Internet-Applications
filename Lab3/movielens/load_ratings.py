import os
import json
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movielens.settings')
# Initialize Django
django.setup()

from django.contrib.auth.hashers import make_password
from userview.models import Movie, Image, Genre, Comment, Rating
from django.contrib.auth.models import User
from django.core.files import File

with open('fixtures/picked_ratings.json', 'r') as file:
    ratings_data = json.load(file)

for rating_data in ratings_data:
    # Find the associated Movie and User models
    try:
        movie = Movie.objects.get(pk=rating_data['movie_id'])
        user = User.objects.get(pk=rating_data['user_id'])
    except (Movie.DoesNotExist, User.DoesNotExist):
        continue

    # Create Rating model instance
    rating = Rating()
    rating.movie = movie
    rating.user = user
    rating.value = rating_data['rating']

    # Save the rating model to the database
    rating.save()