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

movies_dir = 'fixtures/picked_movies'

for filename in os.listdir(movies_dir):
    if filename.endswith('.json'):
        # Read JSON file
        with open(os.path.join(movies_dir, filename), 'r') as file:
            movie_data = json.load(file)

        # Create Movie model instance
        movie = Movie()
        # Set movie attributes excluding the 'image' field
        movie.title = movie_data['title']
        movie.year = movie_data['year']
        movie.director = movie_data['director']
        movie.imdblink = movie_data['imdbLink']
        movie.description = movie_data['description']

        # Split genre names by comma and create Genre instances
        genre_names = movie_data['genre'].split(',')
        genres = []
        for genre_name in genre_names:
            genre, _ = Genre.objects.get_or_create(name=genre_name.strip())
            genres.append(genre)

        # Save the movie model to the database
        movie.save()
        # Assign genres to the movie
        movie.genres.set(genres)